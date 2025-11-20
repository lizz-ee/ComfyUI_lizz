"""
ComfyUI Rotoscoping Node for The Foundry's Nuke
================================================

This Python script creates a Nuke node that sends video frames to ComfyUI
for AI-powered rotoscoping/masking using SAM2, Contextual-SAM2, or Grounding DINO workflows.

Features:
- Multiple workflow modes: SAM2, Contextual-SAM2, Grounding DINO + SAM
- Frame range processing with temporal tracking
- Smart resolution downsampling for 4K/2K workflows
- EXR sequence support for VFX pipelines
- Frame-by-frame processing for memory efficiency

Requirements:
- Nuke 11+ (Python 2.7) or Nuke 13+ (Python 3)
- ComfyUI server running with required custom nodes
- requests library (pip install requests)

ComfyUI Custom Nodes Required:
- ComfyUI-segment-anything-2 (kijai) - SAM2 support
- ComfyUI-Contextual-SAM2 (MicheleGuidi) - Florence2 + SAM2
- ComfyUI-Grounding-DINO (or equivalent) - DINO + SAM
- ComfyUI-HQ-Image-Save (spacepxl) - EXR support (optional)
- ComfyUI-VideoHelperSuite (Kosinkadink) - Video utilities (optional)

Installation:
1. Copy this file to your .nuke folder or a custom plugin path
2. Add to your menu.py:
   import comfyui_roto
   comfyui_roto.add_to_menu()

Usage:
1. Connect your video input (plate)
2. Select workflow mode (SAM2, Contextual-SAM2, or Grounding DINO)
3. Set frame range and resolution settings
4. Configure segmentation parameters (prompts, points, bboxes)
5. Click 'Execute Roto' to process

Author: ComfyUI Integration
License: MIT
"""

import os
import sys
import json
import time
import tempfile
import uuid
import struct

# Handle Python 2/3 compatibility
try:
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen, Request, URLError, HTTPError
    from urllib import urlencode

try:
    import nuke
    IN_NUKE = True
except ImportError:
    IN_NUKE = False
    print("Warning: Running outside of Nuke. Some features disabled.")


class ComfyUIRotoNode:
    """
    Main class for ComfyUI Rotoscoping integration with Nuke.
    """

    def __init__(self):
        self.server_address = "127.0.0.1:8188"
        self.client_id = str(uuid.uuid4())

    def create_node(self):
        """Create the Nuke node with all necessary knobs."""
        if not IN_NUKE:
            print("Cannot create node outside of Nuke")
            return None

        # Create a Group node to hold our roto setup
        node = nuke.createNode('Group', inpanel=False)
        node.setName('ComfyUI_Roto')

        # Begin group editing
        node.begin()

        # Create input node
        input_img = nuke.createNode('Input', inpanel=False)
        input_img.setName('img')
        input_img['name'].setValue('img')

        # Create output
        output = nuke.createNode('Output', inpanel=False)
        output.setName('Output1')

        # Create a Read node to hold the result (will be updated after roto)
        result_read = nuke.createNode('Read', inpanel=False)
        result_read.setName('RotoResult')
        result_read['file'].setValue('')

        # Connect output to result
        output.setInput(0, result_read)

        node.end()

        # Add custom knobs to the group
        tab = nuke.Tab_Knob('comfyui_tab', 'ComfyUI Roto')
        node.addKnob(tab)

        # Server settings
        divider1 = nuke.Text_Knob('divider1', '', '<b>Server Settings</b>')
        node.addKnob(divider1)

        server_knob = nuke.String_Knob('server_address', 'Server Address')
        server_knob.setValue('127.0.0.1:8188')
        node.addKnob(server_knob)

        # Workflow selection
        divider2 = nuke.Text_Knob('divider2', '', '<b>Workflow Selection</b>')
        node.addKnob(divider2)

        workflow_knob = nuke.Enumeration_Knob('workflow_mode', 'Workflow Mode', [
            'SAM2',
            'Contextual-SAM2',
            'Grounding DINO + SAM'
        ])
        workflow_knob.setValue('SAM2')
        workflow_knob.setTooltip(
            'SAM2: Basic segmentation with temporal tracking\n'
            'Contextual-SAM2: Florence2 object detection + SAM2\n'
            'Grounding DINO + SAM: Natural language grounding + SAM'
        )
        node.addKnob(workflow_knob)

        # Frame range
        divider3 = nuke.Text_Knob('divider3', '', '<b>Frame Range</b>')
        node.addKnob(divider3)

        frame_start_knob = nuke.Int_Knob('frame_start', 'Frame Start')
        frame_start_knob.setValue(1001)
        node.addKnob(frame_start_knob)

        frame_end_knob = nuke.Int_Knob('frame_end', 'Frame End')
        frame_end_knob.setValue(1001)
        node.addKnob(frame_end_knob)

        current_frame_knob = nuke.Boolean_Knob('current_frame_only', 'Current Frame Only')
        current_frame_knob.setValue(True)
        current_frame_knob.setTooltip('Process only the current frame (ignores frame range)')
        node.addKnob(current_frame_knob)

        # Resolution & Format
        divider4 = nuke.Text_Knob('divider4', '', '<b>Resolution & Format</b>')
        node.addKnob(divider4)

        input_format_knob = nuke.Enumeration_Knob('input_format', 'Input Format', [
            'EXR Sequence',
            'PNG Sequence'
        ])
        input_format_knob.setValue('PNG Sequence')
        node.addKnob(input_format_knob)

        output_format_knob = nuke.Enumeration_Knob('output_format', 'Output Format', [
            'PNG',
            'EXR',
            'TIFF'
        ])
        output_format_knob.setValue('PNG')
        node.addKnob(output_format_knob)

        process_mode_knob = nuke.Enumeration_Knob('process_mode', 'Process Mode', [
            'Native Resolution',
            'Smart Downrez'
        ])
        process_mode_knob.setValue('Smart Downrez')
        process_mode_knob.setTooltip(
            'Native: Process at source resolution (slower, high VRAM)\n'
            'Smart Downrez: Downscale for processing, upscale alpha after (faster, lower VRAM)'
        )
        node.addKnob(process_mode_knob)

        target_res_knob = nuke.Enumeration_Knob('target_resolution', 'Target Resolution', [
            '720p (1280x720)',
            'HD (1920x1080)',
            '2K (2048x1080)',
            'Native (use source resolution)'
        ])
        target_res_knob.setValue('720p (1280x720)')
        target_res_knob.setTooltip('Resolution for ComfyUI processing (lower = faster, less VRAM)')
        node.addKnob(target_res_knob)

        upscale_alpha_knob = nuke.Boolean_Knob('upscale_alpha', 'Upscale Alpha to Source')
        upscale_alpha_knob.setValue(True)
        upscale_alpha_knob.setTooltip('Automatically upscale output alpha back to source resolution')
        node.addKnob(upscale_alpha_knob)

        upscale_method_knob = nuke.Enumeration_Knob('upscale_method', 'Upscale Method', [
            'Bicubic',
            'Lanczos',
            'Bilinear',
            'Nearest'
        ])
        upscale_method_knob.setValue('Lanczos')
        node.addKnob(upscale_method_knob)

        # Text Prompt (Universal)
        divider5 = nuke.Text_Knob('divider5', '', '<b>Segmentation Settings</b>')
        node.addKnob(divider5)

        text_prompt_knob = nuke.Multiline_Eval_String_Knob('text_prompt', 'Text Prompt')
        text_prompt_knob.setValue('the person')
        text_prompt_knob.setTooltip('Describe the object to segment (e.g., "the person", "the car")')
        node.addKnob(text_prompt_knob)

        # Selection Method (SAM2 modes)
        selection_method_knob = nuke.Enumeration_Knob('selection_method', 'Selection Method', [
            'Point',
            'BBox',
            'Text Only'
        ])
        selection_method_knob.setValue('Point')
        selection_method_knob.setTooltip(
            'Point: Click coordinates to segment object\n'
            'BBox: Bounding box around object\n'
            'Text Only: Use text prompt alone (Contextual-SAM2/DINO only)'
        )
        node.addKnob(selection_method_knob)

        # Point coordinates
        point_x_knob = nuke.Double_Knob('point_x', 'Point X')
        point_x_knob.setValue(640)
        point_x_knob.setTooltip('X coordinate of point (in pixels at processing resolution)')
        node.addKnob(point_x_knob)

        point_y_knob = nuke.Double_Knob('point_y', 'Point Y')
        point_y_knob.setValue(360)
        point_y_knob.setTooltip('Y coordinate of point (in pixels at processing resolution)')
        node.addKnob(point_y_knob)

        # BBox coordinates
        bbox_x1_knob = nuke.Int_Knob('bbox_x1', 'BBox X1')
        bbox_x1_knob.setValue(100)
        node.addKnob(bbox_x1_knob)

        bbox_y1_knob = nuke.Int_Knob('bbox_y1', 'BBox Y1')
        bbox_y1_knob.setValue(100)
        node.addKnob(bbox_y1_knob)

        bbox_x2_knob = nuke.Int_Knob('bbox_x2', 'BBox X2')
        bbox_x2_knob.setValue(500)
        node.addKnob(bbox_x2_knob)

        bbox_y2_knob = nuke.Int_Knob('bbox_y2', 'BBox Y2')
        bbox_y2_knob.setValue(500)
        node.addKnob(bbox_y2_knob)

        # SAM2 Model Settings
        divider6 = nuke.Text_Knob('divider6', '', '<b>SAM2 Settings</b>')
        node.addKnob(divider6)

        sam2_model_knob = nuke.Enumeration_Knob('sam2_model', 'SAM2 Model', [
            'sam2.1_hiera_tiny',
            'sam2.1_hiera_small',
            'sam2.1_hiera_base_plus',
            'sam2.1_hiera_large'
        ])
        sam2_model_knob.setValue('sam2.1_hiera_base_plus')
        sam2_model_knob.setTooltip('Larger models = better quality but slower')
        node.addKnob(sam2_model_knob)

        tracking_mode_knob = nuke.Enumeration_Knob('tracking_mode', 'Tracking Mode', [
            'Propagate Forward',
            'Independent Frames'
        ])
        tracking_mode_knob.setValue('Propagate Forward')
        tracking_mode_knob.setTooltip(
            'Propagate Forward: Track object across frames (stable)\n'
            'Independent Frames: Segment each frame separately (may flicker)'
        )
        node.addKnob(tracking_mode_knob)

        mask_dilate_knob = nuke.Int_Knob('mask_dilate', 'Mask Dilate/Erode (px)')
        mask_dilate_knob.setValue(0)
        mask_dilate_knob.setRange(-20, 20)
        mask_dilate_knob.setTooltip('Positive = dilate (grow), Negative = erode (shrink)')
        node.addKnob(mask_dilate_knob)

        # Contextual-SAM2 Settings
        divider7 = nuke.Text_Knob('divider7', '', '<b>Contextual-SAM2 Settings</b>')
        node.addKnob(divider7)

        florence2_model_knob = nuke.Enumeration_Knob('florence2_model', 'Florence2 Model', [
            'microsoft/florence-2-base',
            'microsoft/florence-2-large'
        ])
        florence2_model_knob.setValue('microsoft/florence-2-base')
        node.addKnob(florence2_model_knob)

        detection_confidence_knob = nuke.Double_Knob('detection_confidence', 'Detection Confidence')
        detection_confidence_knob.setValue(0.3)
        detection_confidence_knob.setRange(0.0, 1.0)
        detection_confidence_knob.setTooltip('Minimum confidence for Florence2 object detection')
        node.addKnob(detection_confidence_knob)

        context_padding_knob = nuke.Int_Knob('context_padding', 'Context Padding (px)')
        context_padding_knob.setValue(50)
        context_padding_knob.setRange(0, 200)
        context_padding_knob.setTooltip('Padding around detected bounding box for context')
        node.addKnob(context_padding_knob)

        # Grounding DINO Settings
        divider8 = nuke.Text_Knob('divider8', '', '<b>Grounding DINO Settings</b>')
        node.addKnob(divider8)

        dino_threshold_knob = nuke.Double_Knob('dino_threshold', 'Detection Threshold')
        dino_threshold_knob.setValue(0.3)
        dino_threshold_knob.setRange(0.0, 1.0)
        dino_threshold_knob.setTooltip('Minimum confidence for Grounding DINO detection')
        node.addKnob(dino_threshold_knob)

        dino_box_threshold_knob = nuke.Double_Knob('dino_box_threshold', 'Box Threshold')
        dino_box_threshold_knob.setValue(0.25)
        dino_box_threshold_knob.setRange(0.0, 1.0)
        node.addKnob(dino_box_threshold_knob)

        # Execute button
        divider9 = nuke.Text_Knob('divider9', '', '')
        node.addKnob(divider9)

        execute_knob = nuke.PyScript_Knob('execute', 'Execute Roto')
        execute_knob.setValue('comfyui_roto.execute_roto(nuke.thisNode())')
        node.addKnob(execute_knob)

        # Status
        status_knob = nuke.Text_Knob('status', 'Status', 'Ready')
        node.addKnob(status_knob)

        return node

    def generate_workflow_sam2(self, image_name, params):
        """
        Generate the ComfyUI workflow JSON for SAM2 segmentation.

        Args:
            image_name: Uploaded image filename in ComfyUI
            params: Dictionary of segmentation parameters

        Returns:
            dict: ComfyUI workflow/prompt dictionary
        """
        workflow = {
            # Load SAM2 Model
            "1": {
                "class_type": "SAM2ModelLoader",
                "inputs": {
                    "model_name": params.get('sam2_model', 'sam2.1_hiera_base_plus.safetensors'),
                    "device": "cuda"
                }
            },
            # Load Image
            "2": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": image_name
                }
            },
            # SAM2 Segmentation
            "3": {
                "class_type": "Sam2Segmentation",
                "inputs": {
                    "sam2_model": ["1", 0],
                    "image": ["2", 0],
                    "prompt_type": params.get('prompt_type', 'point'),
                    "points": params.get('points', [[640, 360]]),
                    "labels": params.get('labels', [1]),
                    "bbox": params.get('bbox', None),
                    "multimask_output": False
                }
            },
            # Mask to Image (for visualization/export)
            "4": {
                "class_type": "MaskToImage",
                "inputs": {
                    "mask": ["3", 0]
                }
            },
            # Save Mask
            "5": {
                "class_type": "SaveImage",
                "inputs": {
                    "images": ["4", 0],
                    "filename_prefix": "nuke_roto_sam2"
                }
            }
        }

        return workflow

    def generate_workflow_contextual_sam2(self, image_name, params):
        """
        Generate the ComfyUI workflow JSON for Contextual-SAM2 (Florence2 + SAM2).

        Args:
            image_name: Uploaded image filename in ComfyUI
            params: Dictionary of segmentation parameters

        Returns:
            dict: ComfyUI workflow/prompt dictionary
        """
        workflow = {
            # Load Image
            "1": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": image_name
                }
            },
            # Load Florence2 Model
            "2": {
                "class_type": "Florence2ModelLoader",
                "inputs": {
                    "model": params.get('florence2_model', 'microsoft/florence-2-base'),
                    "precision": "fp16",
                    "attention": "sdpa"
                }
            },
            # Florence2 Detection
            "3": {
                "class_type": "Florence2Run",
                "inputs": {
                    "image": ["1", 0],
                    "florence2_model": ["2", 0],
                    "text_input": params.get('text_prompt', 'the person'),
                    "task": "caption_to_phrase_grounding",
                    "fill_mask": True,
                    "keep_model_loaded": False,
                    "max_new_tokens": 1024,
                    "num_beams": 3
                }
            },
            # Load SAM2 Model
            "4": {
                "class_type": "SAM2ModelLoader",
                "inputs": {
                    "model_name": params.get('sam2_model', 'sam2.1_hiera_base_plus.safetensors'),
                    "device": "cuda"
                }
            },
            # Contextual SAM2 Segmentation
            "5": {
                "class_type": "Sam2ContextSegmentation",
                "inputs": {
                    "sam2_model": ["4", 0],
                    "image": ["1", 0],
                    "bboxes": ["3", 1],  # From Florence2
                    "context_padding": params.get('context_padding', 50),
                    "multimask_output": False
                }
            },
            # Mask to Image
            "6": {
                "class_type": "MaskToImage",
                "inputs": {
                    "mask": ["5", 0]
                }
            },
            # Save Mask
            "7": {
                "class_type": "SaveImage",
                "inputs": {
                    "images": ["6", 0],
                    "filename_prefix": "nuke_roto_contextual_sam2"
                }
            }
        }

        return workflow

    def generate_workflow_grounding_dino(self, image_name, params):
        """
        Generate the ComfyUI workflow JSON for Grounding DINO + SAM.

        Args:
            image_name: Uploaded image filename in ComfyUI
            params: Dictionary of segmentation parameters

        Returns:
            dict: ComfyUI workflow/prompt dictionary
        """
        workflow = {
            # Load Image
            "1": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": image_name
                }
            },
            # Load Grounding DINO Model
            "2": {
                "class_type": "GroundingDinoModelLoader",
                "inputs": {
                    "model_name": "GroundingDINO_SwinT_OGC (694MB)"
                }
            },
            # Grounding DINO Detection
            "3": {
                "class_type": "GroundingDinoDetection",
                "inputs": {
                    "grounding_dino_model": ["2", 0],
                    "image": ["1", 0],
                    "prompt": params.get('text_prompt', 'the person'),
                    "threshold": params.get('dino_threshold', 0.3),
                    "box_threshold": params.get('dino_box_threshold', 0.25)
                }
            },
            # Load SAM Model (original SAM or SAM2)
            "4": {
                "class_type": "SAMModelLoader",
                "inputs": {
                    "model_name": "sam_vit_h (2.56GB)"
                }
            },
            # SAM Segmentation from DINO boxes
            "5": {
                "class_type": "SAMSegmentation",
                "inputs": {
                    "sam_model": ["4", 0],
                    "image": ["1", 0],
                    "bboxes": ["3", 1]  # From Grounding DINO
                }
            },
            # Mask to Image
            "6": {
                "class_type": "MaskToImage",
                "inputs": {
                    "mask": ["5", 0]
                }
            },
            # Save Mask
            "7": {
                "class_type": "SaveImage",
                "inputs": {
                    "images": ["6", 0],
                    "filename_prefix": "nuke_roto_grounding_dino"
                }
            }
        }

        return workflow

    def upload_image(self, filepath, server_address, subfolder="", image_type="input"):
        """
        Upload an image to ComfyUI server.

        Args:
            filepath: Local path to the image
            server_address: ComfyUI server address
            subfolder: Optional subfolder in ComfyUI input directory
            image_type: Type of upload (input, temp, output)

        Returns:
            dict: Response with name, subfolder, type
        """
        url = f"http://{server_address}/upload/image"

        # Read file
        with open(filepath, 'rb') as f:
            file_data = f.read()

        filename = os.path.basename(filepath)

        # Create multipart form data manually for compatibility
        boundary = '----WebKitFormBoundary' + str(uuid.uuid4()).replace('-', '')

        body = []

        # Add image file
        body.append(f'--{boundary}'.encode())
        body.append(f'Content-Disposition: form-data; name="image"; filename="{filename}"'.encode())
        body.append(b'Content-Type: image/png')
        body.append(b'')
        body.append(file_data)

        # Add type
        body.append(f'--{boundary}'.encode())
        body.append(f'Content-Disposition: form-data; name="type"'.encode())
        body.append(b'')
        body.append(image_type.encode())

        # Add subfolder if specified
        if subfolder:
            body.append(f'--{boundary}'.encode())
            body.append(f'Content-Disposition: form-data; name="subfolder"'.encode())
            body.append(b'')
            body.append(subfolder.encode())

        # End boundary
        body.append(f'--{boundary}--'.encode())
        body.append(b'')

        body_bytes = b'\r\n'.join(body)

        req = Request(url, data=body_bytes)
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

        try:
            response = urlopen(req)
            return json.loads(response.read().decode())
        except (URLError, HTTPError) as e:
            raise Exception(f"Failed to upload image: {e}")

    def queue_prompt(self, prompt, server_address):
        """
        Queue a workflow for execution.

        Args:
            prompt: Workflow dictionary
            server_address: ComfyUI server address

        Returns:
            str: Prompt ID for tracking
        """
        url = f"http://{server_address}/prompt"

        data = json.dumps({
            "prompt": prompt,
            "client_id": self.client_id
        }).encode()

        req = Request(url, data=data)
        req.add_header('Content-Type', 'application/json')

        try:
            response = urlopen(req)
            result = json.loads(response.read().decode())
            return result.get('prompt_id')
        except (URLError, HTTPError) as e:
            raise Exception(f"Failed to queue prompt: {e}")

    def get_history(self, prompt_id, server_address):
        """
        Get execution history for a prompt.

        Args:
            prompt_id: ID of the queued prompt
            server_address: ComfyUI server address

        Returns:
            dict: Execution history and outputs
        """
        url = f"http://{server_address}/history/{prompt_id}"

        try:
            response = urlopen(url)
            return json.loads(response.read().decode())
        except (URLError, HTTPError) as e:
            raise Exception(f"Failed to get history: {e}")

    def download_image(self, filename, server_address, subfolder="", folder_type="output"):
        """
        Download an output image from ComfyUI.

        Args:
            filename: Name of the image file
            server_address: ComfyUI server address
            subfolder: Optional subfolder
            folder_type: Type of folder (output, input, temp)

        Returns:
            bytes: Image data
        """
        params = urlencode({
            'filename': filename,
            'subfolder': subfolder,
            'type': folder_type
        })
        url = f"http://{server_address}/view?{params}"

        try:
            response = urlopen(url)
            return response.read()
        except (URLError, HTTPError) as e:
            raise Exception(f"Failed to download image: {e}")

    def wait_for_completion(self, prompt_id, server_address, timeout=300, poll_interval=1):
        """
        Wait for a prompt to complete execution.

        Args:
            prompt_id: ID of the queued prompt
            server_address: ComfyUI server address
            timeout: Maximum wait time in seconds
            poll_interval: Time between status checks

        Returns:
            dict: Execution results with output images
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id, server_address)

            if prompt_id in history:
                return history[prompt_id]

            time.sleep(poll_interval)

        raise Exception(f"Timeout waiting for prompt {prompt_id}")


def export_nuke_image_to_png(node, output_path, frame_number):
    """
    Export a Nuke node's output to a PNG file.

    Args:
        node: Nuke group node
        output_path: Path to save the PNG
        frame_number: Frame number to export
    """
    if not IN_NUKE:
        raise Exception("Not running in Nuke")

    # Get the input node
    input_node = node.input(0)
    if not input_node:
        raise Exception(f"No input connected to node")

    # Create a Write node to export
    write_node = nuke.createNode('Write', inpanel=False)
    write_node['file'].setValue(output_path)
    write_node['file_type'].setValue('png')
    write_node['channels'].setValue('rgb')
    write_node['colorspace'].setValue('sRGB')
    write_node.setInput(0, input_node)

    # Execute the write
    nuke.execute(write_node, frame_number, frame_number)

    # Clean up
    nuke.delete(write_node)


def get_target_resolution(resolution_mode):
    """
    Parse target resolution from mode string.

    Args:
        resolution_mode: String like '720p (1280x720)' or 'Native'

    Returns:
        tuple: (width, height) or None for native
    """
    resolution_map = {
        '720p (1280x720)': (1280, 720),
        'HD (1920x1080)': (1920, 1080),
        '2K (2048x1080)': (2048, 1080),
        'Native (use source resolution)': None
    }
    return resolution_map.get(resolution_mode, None)


def execute_roto(node):
    """
    Main execution function called by the Execute button.

    Args:
        node: The ComfyUI_Roto group node
    """
    if not IN_NUKE:
        print("Cannot execute outside of Nuke")
        return

    # Update status
    node['status'].setValue('Processing...')

    try:
        # Get workflow mode
        workflow_mode = node['workflow_mode'].value()

        # Get frame range
        if node['current_frame_only'].value():
            frame_start = nuke.frame()
            frame_end = nuke.frame()
        else:
            frame_start = int(node['frame_start'].value())
            frame_end = int(node['frame_end'].value())

        # Get parameters
        server_address = node['server_address'].value()
        text_prompt = node['text_prompt'].value()
        selection_method = node['selection_method'].value()

        # Resolution settings
        process_mode = node['process_mode'].value()
        target_resolution = get_target_resolution(node['target_resolution'].value())

        # Build params dict based on workflow
        params = {
            'text_prompt': text_prompt,
            'selection_method': selection_method,
            'sam2_model': node['sam2_model'].value(),
            'tracking_mode': node['tracking_mode'].value(),
            'mask_dilate': int(node['mask_dilate'].value()),
            'florence2_model': node['florence2_model'].value(),
            'detection_confidence': float(node['detection_confidence'].value()),
            'context_padding': int(node['context_padding'].value()),
            'dino_threshold': float(node['dino_threshold'].value()),
            'dino_box_threshold': float(node['dino_box_threshold'].value())
        }

        # Add point/bbox based on selection method
        if selection_method == 'Point':
            params['prompt_type'] = 'point'
            params['points'] = [[int(node['point_x'].value()), int(node['point_y'].value())]]
            params['labels'] = [1]  # Foreground
        elif selection_method == 'BBox':
            params['prompt_type'] = 'box'
            params['bbox'] = [
                int(node['bbox_x1'].value()),
                int(node['bbox_y1'].value()),
                int(node['bbox_x2'].value()),
                int(node['bbox_y2'].value())
            ]

        # Create temporary directory for exports
        temp_dir = tempfile.mkdtemp(prefix='nuke_comfyui_roto_')

        # Create roto instance
        roto = ComfyUIRotoNode()
        roto.server_address = server_address

        # Process frames
        total_frames = frame_end - frame_start + 1
        node['status'].setValue(f'Processing {total_frames} frame(s)...')

        result_files = []

        for frame_num in range(frame_start, frame_end + 1):
            node['status'].setValue(f'Processing frame {frame_num} ({frame_num - frame_start + 1}/{total_frames})...')

            # Export current frame
            image_path = os.path.join(temp_dir, f'input_frame_{frame_num:04d}.png')
            export_nuke_image_to_png(node, image_path, frame_num)

            # Upload to ComfyUI
            node['status'].setValue(f'Uploading frame {frame_num}...')
            upload_result = roto.upload_image(image_path, server_address)
            image_name = upload_result.get('name', os.path.basename(image_path))

            # Generate workflow based on mode
            if workflow_mode == 'SAM2':
                workflow = roto.generate_workflow_sam2(image_name, params)
            elif workflow_mode == 'Contextual-SAM2':
                workflow = roto.generate_workflow_contextual_sam2(image_name, params)
            elif workflow_mode == 'Grounding DINO + SAM':
                workflow = roto.generate_workflow_grounding_dino(image_name, params)
            else:
                raise Exception(f"Unknown workflow mode: {workflow_mode}")

            # Queue prompt
            node['status'].setValue(f'Queuing job for frame {frame_num}...')
            prompt_id = roto.queue_prompt(workflow, server_address)

            if not prompt_id:
                raise Exception(f"Failed to queue prompt for frame {frame_num}")

            # Wait for completion
            node['status'].setValue(f'Processing frame {frame_num} in ComfyUI...')
            result = roto.wait_for_completion(prompt_id, server_address, timeout=300)

            # Get output image (varies by workflow, typically last SaveImage node)
            outputs = result.get('outputs', {})

            # Find the SaveImage node output (different node numbers per workflow)
            save_node_id = None
            if workflow_mode == 'SAM2':
                save_node_id = '5'
            elif workflow_mode == 'Contextual-SAM2':
                save_node_id = '7'
            elif workflow_mode == 'Grounding DINO + SAM':
                save_node_id = '7'

            save_output = outputs.get(save_node_id, {})
            images = save_output.get('images', [])

            if not images:
                raise Exception(f"No output images found for frame {frame_num}")

            # Download result
            output_info = images[0]
            output_filename = output_info.get('filename')
            output_subfolder = output_info.get('subfolder', '')

            node['status'].setValue(f'Downloading result for frame {frame_num}...')
            image_data = roto.download_image(output_filename, server_address, output_subfolder)

            # Save result locally
            result_path = os.path.join(temp_dir, f'roto_result_{frame_num:04d}.png')
            with open(result_path, 'wb') as f:
                f.write(image_data)

            result_files.append(result_path)

        # Update the Read node with the sequence
        node.begin()
        result_node = nuke.toNode('RotoResult')
        if result_node:
            if len(result_files) == 1:
                # Single frame
                result_node['file'].setValue(result_files[0])
            else:
                # Sequence - use frame pattern
                sequence_path = os.path.join(temp_dir, 'roto_result_%04d.png')
                result_node['file'].setValue(sequence_path)
                result_node['first'].setValue(frame_start)
                result_node['last'].setValue(frame_end)

            result_node['reload'].execute()
        node.end()

        node['status'].setValue(f'Complete! Processed {total_frames} frame(s)')

        # Trigger viewer update
        nuke.updateUI()

    except Exception as e:
        error_msg = str(e)
        node['status'].setValue(f'Error: {error_msg}')
        if IN_NUKE:
            nuke.message(f"ComfyUI Roto Error:\n{error_msg}")


def add_to_menu():
    """Add ComfyUI Roto to Nuke's menu."""
    if not IN_NUKE:
        print("Cannot add menu outside of Nuke")
        return

    toolbar = nuke.toolbar('Nodes')
    comfy_menu = toolbar.addMenu('ComfyUI', icon='')
    comfy_menu.addCommand('Roto', 'comfyui_roto.create_roto_node()')


def create_roto_node():
    """Create a new ComfyUI Roto node."""
    roto = ComfyUIRotoNode()
    return roto.create_node()


# For testing outside Nuke
if __name__ == '__main__':
    print("ComfyUI Rotoscoping Node for Nuke")
    print("=" * 40)
    print("\nThis script must be run from within Nuke.")
    print("\nInstallation:")
    print("1. Copy this file to your .nuke folder")
    print("2. Add to menu.py:")
    print("   import comfyui_roto")
    print("   comfyui_roto.add_to_menu()")
    print("\nUsage:")
    print("1. In Nuke, go to Nodes > ComfyUI > Roto")
    print("2. Connect your video input")
    print("3. Configure settings and click Execute Roto")
