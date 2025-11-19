"""
ComfyUI Inpainting Node for The Foundry's Nuke
===============================================

This Python script creates a Nuke node that sends images and masks to ComfyUI
for AI-powered inpainting, then retrieves and displays the results.

Requirements:
- Nuke 11+ (Python 2.7) or Nuke 13+ (Python 3)
- ComfyUI server running
- requests library (pip install requests)

Installation:
1. Copy this file to your .nuke folder or a custom plugin path
2. Add to your menu.py:
   import comfyui_inpaint
   comfyui_inpaint.add_to_menu()

Usage:
1. Connect your image to the 'img' input
2. Connect your mask to the 'mask' input (white = inpaint area)
3. Configure ComfyUI server address and inpainting parameters
4. Click 'Execute Inpaint' to process

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


class ComfyUIInpaintNode:
    """
    Main class for ComfyUI Inpainting integration with Nuke.
    """

    def __init__(self):
        self.server_address = "127.0.0.1:8188"
        self.client_id = str(uuid.uuid4())

    def create_node(self):
        """Create the Nuke node with all necessary knobs."""
        if not IN_NUKE:
            print("Cannot create node outside of Nuke")
            return None

        # Create a Group node to hold our inpainting setup
        node = nuke.createNode('Group', inpanel=False)
        node.setName('ComfyUI_Inpaint')

        # Begin group editing
        node.begin()

        # Create input nodes
        input_img = nuke.createNode('Input', inpanel=False)
        input_img.setName('img')
        input_img['name'].setValue('img')

        input_mask = nuke.createNode('Input', inpanel=False)
        input_mask.setName('mask')
        input_mask['name'].setValue('mask')

        # Create output
        output = nuke.createNode('Output', inpanel=False)
        output.setName('Output1')

        # Create a Read node to hold the result (will be updated after inpainting)
        result_read = nuke.createNode('Read', inpanel=False)
        result_read.setName('InpaintResult')
        result_read['file'].setValue('')

        # Connect output to result
        output.setInput(0, result_read)

        node.end()

        # Add custom knobs to the group
        tab = nuke.Tab_Knob('comfyui_tab', 'ComfyUI Inpaint')
        node.addKnob(tab)

        # Server settings
        divider1 = nuke.Text_Knob('divider1', '', '<b>Server Settings</b>')
        node.addKnob(divider1)

        server_knob = nuke.String_Knob('server_address', 'Server Address')
        server_knob.setValue('127.0.0.1:8188')
        node.addKnob(server_knob)

        # Model settings
        divider2 = nuke.Text_Knob('divider2', '', '<b>Model Settings</b>')
        node.addKnob(divider2)

        checkpoint_knob = nuke.String_Knob('checkpoint', 'Checkpoint')
        checkpoint_knob.setValue('sd_xl_base_1.0.safetensors')
        checkpoint_knob.setTooltip('Name of the checkpoint file in ComfyUI models/checkpoints folder')
        node.addKnob(checkpoint_knob)

        # Prompt settings
        divider3 = nuke.Text_Knob('divider3', '', '<b>Prompt Settings</b>')
        node.addKnob(divider3)

        positive_knob = nuke.Multiline_Eval_String_Knob('positive_prompt', 'Positive Prompt')
        positive_knob.setValue('high quality, detailed, photorealistic')
        node.addKnob(positive_knob)

        negative_knob = nuke.Multiline_Eval_String_Knob('negative_prompt', 'Negative Prompt')
        negative_knob.setValue('blurry, low quality, artifacts, distorted')
        node.addKnob(negative_knob)

        # Sampling settings
        divider4 = nuke.Text_Knob('divider4', '', '<b>Sampling Settings</b>')
        node.addKnob(divider4)

        steps_knob = nuke.Int_Knob('steps', 'Steps')
        steps_knob.setValue(20)
        steps_knob.setRange(1, 100)
        node.addKnob(steps_knob)

        cfg_knob = nuke.Double_Knob('cfg', 'CFG Scale')
        cfg_knob.setValue(7.0)
        cfg_knob.setRange(1.0, 20.0)
        node.addKnob(cfg_knob)

        denoise_knob = nuke.Double_Knob('denoise', 'Denoise Strength')
        denoise_knob.setValue(1.0)
        denoise_knob.setRange(0.0, 1.0)
        denoise_knob.setTooltip('1.0 = full inpaint, lower values blend with original')
        node.addKnob(denoise_knob)

        seed_knob = nuke.Int_Knob('seed', 'Seed')
        seed_knob.setValue(0)
        seed_knob.setTooltip('Base seed value (behavior depends on Seed Mode)')
        node.addKnob(seed_knob)

        seed_mode_knob = nuke.Enumeration_Knob('seed_mode', 'Seed Mode', [
            'fixed', 'random', 'per_frame', 'base_plus_frame'
        ])
        seed_mode_knob.setValue('fixed')
        seed_mode_knob.setTooltip(
            'fixed: Use seed value as-is\n'
            'random: Generate random seed each execution\n'
            'per_frame: Use current frame number as seed\n'
            'base_plus_frame: Seed + frame number (for animatable variations)'
        )
        node.addKnob(seed_mode_knob)

        sampler_knob = nuke.Enumeration_Knob('sampler', 'Sampler', [
            'euler', 'euler_ancestral', 'heun', 'dpm_2', 'dpm_2_ancestral',
            'lms', 'dpm_fast', 'dpm_adaptive', 'dpmpp_2s_ancestral',
            'dpmpp_sde', 'dpmpp_2m', 'dpmpp_2m_sde', 'ddim', 'uni_pc'
        ])
        sampler_knob.setValue('dpmpp_2m_sde')
        node.addKnob(sampler_knob)

        scheduler_knob = nuke.Enumeration_Knob('scheduler', 'Scheduler', [
            'normal', 'karras', 'exponential', 'sgm_uniform', 'simple', 'ddim_uniform'
        ])
        scheduler_knob.setValue('karras')
        node.addKnob(scheduler_knob)

        # Mask settings
        divider5 = nuke.Text_Knob('divider5', '', '<b>Mask Settings</b>')
        node.addKnob(divider5)

        grow_mask_knob = nuke.Int_Knob('grow_mask', 'Grow Mask (px)')
        grow_mask_knob.setValue(6)
        grow_mask_knob.setRange(0, 64)
        node.addKnob(grow_mask_knob)

        # Execute button
        divider6 = nuke.Text_Knob('divider6', '', '')
        node.addKnob(divider6)

        execute_knob = nuke.PyScript_Knob('execute', 'Execute Inpaint')
        execute_knob.setValue('comfyui_inpaint.execute_inpaint(nuke.thisNode())')
        node.addKnob(execute_knob)

        # Status
        status_knob = nuke.Text_Knob('status', 'Status', 'Ready')
        node.addKnob(status_knob)

        return node

    def generate_workflow(self, image_name, mask_name, params):
        """
        Generate the ComfyUI workflow JSON for inpainting.

        Args:
            image_name: Uploaded image filename in ComfyUI
            mask_name: Uploaded mask filename in ComfyUI
            params: Dictionary of inpainting parameters

        Returns:
            dict: ComfyUI workflow/prompt dictionary
        """
        seed = params.get('seed', 0)
        if seed == 0:
            import random
            seed = random.randint(0, 2**32 - 1)

        workflow = {
            # Load Checkpoint
            "1": {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": params.get('checkpoint', 'sd_xl_base_1.0.safetensors')
                }
            },
            # Load Image
            "2": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": image_name
                }
            },
            # Load Mask (from alpha or as separate image)
            "3": {
                "class_type": "LoadImage",
                "inputs": {
                    "image": mask_name
                }
            },
            # Convert loaded mask image to mask format
            "4": {
                "class_type": "ImageToMask",
                "inputs": {
                    "image": ["3", 0],
                    "channel": "red"
                }
            },
            # Positive prompt encoding
            "5": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": params.get('positive_prompt', 'high quality'),
                    "clip": ["1", 1]
                }
            },
            # Negative prompt encoding
            "6": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": params.get('negative_prompt', 'low quality'),
                    "clip": ["1", 1]
                }
            },
            # VAE Encode for Inpaint
            "7": {
                "class_type": "VAEEncodeForInpaint",
                "inputs": {
                    "pixels": ["2", 0],
                    "vae": ["1", 2],
                    "mask": ["4", 0],
                    "grow_mask_by": params.get('grow_mask', 6)
                }
            },
            # KSampler
            "8": {
                "class_type": "KSampler",
                "inputs": {
                    "model": ["1", 0],
                    "positive": ["5", 0],
                    "negative": ["6", 0],
                    "latent_image": ["7", 0],
                    "seed": seed,
                    "steps": params.get('steps', 20),
                    "cfg": params.get('cfg', 7.0),
                    "sampler_name": params.get('sampler', 'dpmpp_2m_sde'),
                    "scheduler": params.get('scheduler', 'karras'),
                    "denoise": params.get('denoise', 1.0)
                }
            },
            # VAE Decode
            "9": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["8", 0],
                    "vae": ["1", 2]
                }
            },
            # Save Image
            "10": {
                "class_type": "SaveImage",
                "inputs": {
                    "images": ["9", 0],
                    "filename_prefix": "nuke_inpaint"
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


def export_nuke_image_to_png(node, input_name, output_path):
    """
    Export a Nuke node's output to a PNG file.

    Args:
        node: Nuke group node
        input_name: Name of the input ('img' or 'mask')
        output_path: Path to save the PNG
    """
    if not IN_NUKE:
        raise Exception("Not running in Nuke")

    # Get the input node
    input_node = node.input(0 if input_name == 'img' else 1)
    if not input_node:
        raise Exception(f"No input connected to '{input_name}'")

    # Create a Write node to export
    write_node = nuke.createNode('Write', inpanel=False)
    write_node['file'].setValue(output_path)
    write_node['file_type'].setValue('png')
    write_node['channels'].setValue('rgba')
    write_node.setInput(0, input_node)

    # Execute the write
    frame = nuke.frame()
    nuke.execute(write_node, frame, frame)

    # Clean up
    nuke.delete(write_node)


def execute_inpaint(node):
    """
    Main execution function called by the Execute button.

    Args:
        node: The ComfyUI_Inpaint group node
    """
    if not IN_NUKE:
        print("Cannot execute outside of Nuke")
        return

    # Update status
    node['status'].setValue('Processing...')

    try:
        # Calculate seed based on seed mode
        import random
        base_seed = int(node['seed'].value())
        seed_mode = node['seed_mode'].value()
        current_frame = nuke.frame()

        if seed_mode == 'fixed':
            final_seed = base_seed
        elif seed_mode == 'random':
            final_seed = random.randint(0, 2**32 - 1)
        elif seed_mode == 'per_frame':
            final_seed = current_frame
        elif seed_mode == 'base_plus_frame':
            final_seed = base_seed + current_frame
        else:
            final_seed = base_seed

        # Get parameters from knobs
        params = {
            'checkpoint': node['checkpoint'].value(),
            'positive_prompt': node['positive_prompt'].value(),
            'negative_prompt': node['negative_prompt'].value(),
            'steps': int(node['steps'].value()),
            'cfg': float(node['cfg'].value()),
            'denoise': float(node['denoise'].value()),
            'seed': final_seed,
            'sampler': node['sampler'].value(),
            'scheduler': node['scheduler'].value(),
            'grow_mask': int(node['grow_mask'].value())
        }

        server_address = node['server_address'].value()

        # Create temporary directory for image export
        temp_dir = tempfile.mkdtemp(prefix='nuke_comfyui_')

        # Export image and mask from Nuke
        image_path = os.path.join(temp_dir, 'input_image.png')
        mask_path = os.path.join(temp_dir, 'input_mask.png')

        node['status'].setValue('Exporting image...')
        export_nuke_image_to_png(node, 'img', image_path)

        node['status'].setValue('Exporting mask...')
        export_nuke_image_to_png(node, 'mask', mask_path)

        # Create inpainter instance
        inpainter = ComfyUIInpaintNode()
        inpainter.server_address = server_address

        # Upload images to ComfyUI
        node['status'].setValue('Uploading to ComfyUI...')

        image_result = inpainter.upload_image(image_path, server_address)
        mask_result = inpainter.upload_image(mask_path, server_address)

        image_name = image_result.get('name', 'input_image.png')
        mask_name = mask_result.get('name', 'input_mask.png')

        # Generate workflow
        workflow = inpainter.generate_workflow(image_name, mask_name, params)

        # Queue the prompt
        node['status'].setValue('Queuing inpaint job...')
        prompt_id = inpainter.queue_prompt(workflow, server_address)

        if not prompt_id:
            raise Exception("Failed to queue prompt - no prompt_id returned")

        # Wait for completion
        node['status'].setValue('Processing in ComfyUI...')
        result = inpainter.wait_for_completion(prompt_id, server_address)

        # Get output image
        outputs = result.get('outputs', {})

        # Find the SaveImage node output (node "10")
        save_output = outputs.get('10', {})
        images = save_output.get('images', [])

        if not images:
            raise Exception("No output images found")

        # Download the result
        output_info = images[0]
        output_filename = output_info.get('filename')
        output_subfolder = output_info.get('subfolder', '')

        node['status'].setValue('Downloading result...')

        image_data = inpainter.download_image(
            output_filename,
            server_address,
            output_subfolder
        )

        # Save result locally
        result_path = os.path.join(temp_dir, 'inpaint_result.png')
        with open(result_path, 'wb') as f:
            f.write(image_data)

        # Update the Read node inside the group
        node.begin()
        result_node = nuke.toNode('InpaintResult')
        if result_node:
            result_node['file'].setValue(result_path)
            result_node['reload'].execute()
        node.end()

        node['status'].setValue(f'Complete! Seed: {final_seed}')

        # Trigger viewer update
        nuke.updateUI()

    except Exception as e:
        error_msg = str(e)
        node['status'].setValue(f'Error: {error_msg}')
        if IN_NUKE:
            nuke.message(f"ComfyUI Inpaint Error:\n{error_msg}")


def add_to_menu():
    """Add ComfyUI Inpaint to Nuke's menu."""
    if not IN_NUKE:
        print("Cannot add menu outside of Nuke")
        return

    toolbar = nuke.toolbar('Nodes')
    comfy_menu = toolbar.addMenu('ComfyUI', icon='')
    comfy_menu.addCommand('Inpaint', 'comfyui_inpaint.create_inpaint_node()')


def create_inpaint_node():
    """Create a new ComfyUI Inpaint node."""
    inpainter = ComfyUIInpaintNode()
    return inpainter.create_node()


# For testing outside Nuke
if __name__ == '__main__':
    print("ComfyUI Inpainting Node for Nuke")
    print("=" * 40)
    print("\nThis script must be run from within Nuke.")
    print("\nInstallation:")
    print("1. Copy this file to your .nuke folder")
    print("2. Add to menu.py:")
    print("   import comfyui_inpaint")
    print("   comfyui_inpaint.add_to_menu()")
    print("\nUsage:")
    print("1. In Nuke, go to Nodes > ComfyUI > Inpaint")
    print("2. Connect your image and mask inputs")
    print("3. Configure settings and click Execute")
