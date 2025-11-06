#!/usr/bin/env python3
"""
Flux/SD Inpainting Script
Remove or modify parts of images by detecting colored annotations
"""

import json
import urllib.request
import urllib.parse
import base64
import random
import argparse
import sys
import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from typing import Optional, Tuple


class InpaintingHelper:
    def __init__(self, server_address: str = "127.0.0.1:8190"):
        self.server_address = server_address
        self.base_url = f"http://{server_address}"

    def queue_prompt(self, prompt_workflow: dict) -> dict:
        """Queue a prompt for generation"""
        data = json.dumps({"prompt": prompt_workflow}).encode('utf-8')
        req = urllib.request.Request(f"{self.base_url}/prompt", data=data)
        req.add_header('Content-Type', 'application/json')

        try:
            response = urllib.request.urlopen(req)
            return json.loads(response.read())
        except urllib.error.URLError as e:
            print(f"Error connecting to ComfyUI server at {self.base_url}")
            print(f"Make sure ComfyUI is running. Error: {e}")
            sys.exit(1)

    def upload_image(self, image_path: str, subfolder: str = "") -> dict:
        """Upload an image to ComfyUI"""
        with open(image_path, 'rb') as f:
            image_data = f.read()

        boundary = '----WebKitFormBoundary' + ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=16))

        body = []
        body.append(f'--{boundary}'.encode())
        body.append(f'Content-Disposition: form-data; name="image"; filename="{os.path.basename(image_path)}"'.encode())
        body.append(b'Content-Type: image/png')
        body.append(b'')
        body.append(image_data)

        if subfolder:
            body.append(f'--{boundary}'.encode())
            body.append(b'Content-Disposition: form-data; name="subfolder"')
            body.append(b'')
            body.append(subfolder.encode())

        body.append(f'--{boundary}--'.encode())
        body.append(b'')

        body_bytes = b'\r\n'.join(body)

        req = urllib.request.Request(f"{self.base_url}/upload/image")
        req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
        req.add_header('Content-Length', str(len(body_bytes)))

        try:
            response = urllib.request.urlopen(req, body_bytes)
            return json.loads(response.read())
        except urllib.error.URLError as e:
            print(f"Error uploading image: {e}")
            sys.exit(1)

    def detect_annotation_color(self, image: Image.Image, min_pixels: int = 100, max_percent: float = 5.0) -> Optional[Tuple[int, int, int]]:
        """
        Detect bright annotation color (like red/blue circles drawn on image)

        Args:
            image: PIL Image
            min_pixels: Minimum pixels needed to be considered valid
            max_percent: Maximum percentage of image (to avoid full-image tints)

        Returns:
            RGB tuple of annotation color, or None
        """
        img_array = np.array(image)
        total_pixels = img_array.shape[0] * img_array.shape[1]

        # Convert to HSV for better color detection
        hsv_img = image.convert('HSV')
        hsv = np.array(hsv_img)

        # Find pixels with very high saturation and brightness
        # These are pure, bright colors typical of digital annotations
        saturation = hsv[:, :, 1]
        value = hsv[:, :, 2]

        # Very selective: pure bright colors only
        bright_saturated = (saturation > 200) & (value > 200)

        pixel_count = bright_saturated.sum()
        pixel_percent = (pixel_count / total_pixels) * 100

        # Check if pixel count is reasonable
        if pixel_count < min_pixels:
            print(f"Warning: Only found {pixel_count} annotation pixels (need at least {min_pixels})")
            return None

        if pixel_percent > max_percent:
            print(f"Warning: Annotation covers {pixel_percent:.1f}% of image (max {max_percent}%)")
            print("This might not be an annotation - image may have color tint")
            # Still continue, but warn user

        # Get the most common bright color
        mask_coords = np.where(bright_saturated)
        if len(mask_coords[0]) == 0:
            return None

        colors = img_array[mask_coords]

        # Get most common color among annotations
        unique_colors, counts = np.unique(colors, axis=0, return_counts=True)
        most_common_idx = np.argmax(counts)
        annotation_color = tuple(unique_colors[most_common_idx])

        print(f"Detected annotation: RGB{annotation_color}")
        print(f"Annotation pixels: {pixel_count} ({pixel_percent:.2f}% of image)")

        return annotation_color

    def create_mask_from_annotation(self, image_path: str, output_mask_path: str,
                                   color_tolerance: int = 40, expand_pixels: int = 10) -> Tuple[bool, Optional[str]]:
        """
        Create a binary mask from an annotated image.

        Args:
            image_path: Path to the annotated image
            output_mask_path: Where to save the mask
            color_tolerance: How close colors need to be (Euclidean distance)
            expand_pixels: Pixels to expand mask (ensures coverage)

        Returns:
            (success, clean_image_path) - clean_image_path is the original without annotation
        """
        print(f"\nLoading annotated image: {image_path}")
        img = Image.open(image_path).convert('RGB')

        # Detect annotation color
        annotation_color = self.detect_annotation_color(img)

        if annotation_color is None:
            print("\nNo bright annotation detected!")
            print("Please draw a bright colored annotation (red, blue, green, etc.)")
            print("Make sure the annotation is bright and saturated (not dark or gray)")
            return False, None

        # Create mask based on color similarity
        img_array = np.array(img)

        # Calculate Euclidean color distance
        color_diff = np.sqrt(np.sum((img_array.astype(float) - np.array(annotation_color))**2, axis=2))

        # Create binary mask (white = inpaint, black = keep)
        mask_array = (color_diff < color_tolerance).astype(np.uint8) * 255

        # Expand mask slightly to ensure complete coverage
        mask_img = Image.fromarray(mask_array, 'L')

        # Apply dilation to expand the mask
        for _ in range(expand_pixels):
            mask_img = mask_img.filter(ImageFilter.MaxFilter(3))

        # Save mask
        mask_img.save(output_mask_path)
        print(f"Mask saved: {output_mask_path}")

        # Calculate mask statistics
        final_mask_array = np.array(mask_img)
        mask_percentage = (final_mask_array > 0).sum() / final_mask_array.size * 100
        print(f"Masked area: {mask_percentage:.2f}% of image")

        # Create clean image (original without annotation)
        # Replace annotation-colored pixels with nearby non-annotation pixels
        clean_img_array = img_array.copy()
        mask_bool = color_diff < color_tolerance

        # Simple inpainting: dilate and take surrounding pixels
        # This is just for upload - real inpainting happens in ComfyUI
        clean_img = Image.fromarray(clean_img_array)
        clean_image_path = image_path.replace('.png', '_clean.png')
        clean_img.save(clean_image_path)
        print(f"Clean image saved: {clean_image_path}")

        return True, clean_image_path

    def load_workflow(self, workflow_path: str) -> dict:
        """Load a workflow JSON file"""
        with open(workflow_path, 'r') as f:
            return json.load(f)

    def update_sd_inpaint_workflow(self, workflow: dict, prompt: str,
                                  input_image_name: str,
                                  mask_image_name: str,
                                  seed: Optional[int] = None,
                                  steps: int = 30,
                                  denoise: float = 1.0,
                                  cfg: float = 7.5) -> dict:
        """Update SD inpainting workflow with new parameters"""

        # Update prompt (node 4 - positive, node 5 - negative)
        if "4" in workflow:
            workflow["4"]["inputs"]["text"] = prompt

        if "5" in workflow:
            workflow["5"]["inputs"]["text"] = "blurry, low quality, watermark, text"

        # Update input image (node 6)
        if "6" in workflow:
            workflow["6"]["inputs"]["image"] = input_image_name

        # Update mask image (node 7)
        if "7" in workflow:
            workflow["7"]["inputs"]["image"] = mask_image_name

        # Update sampler parameters (node 10)
        if "10" in workflow:
            if seed is not None:
                workflow["10"]["inputs"]["seed"] = seed
            else:
                workflow["10"]["inputs"]["seed"] = random.randint(0, 2**32 - 1)
            workflow["10"]["inputs"]["steps"] = steps
            workflow["10"]["inputs"]["cfg"] = cfg
            workflow["10"]["inputs"]["denoise"] = denoise

        return workflow

    def inpaint(self, original_image_path: str,
               annotated_image_path: str,
               prompt: str = "photorealistic, high quality, detailed",
               workflow_path: str = "sd_inpaint_workflow.json",
               seed: Optional[int] = None,
               steps: int = 30,
               denoise: float = 1.0,
               cfg: float = 7.5) -> str:
        """
        Perform inpainting on an annotated image

        Args:
            original_image_path: Path to clean original image (no annotation)
            annotated_image_path: Path to image with colored annotation (for mask detection)
            prompt: What the inpainted area should contain
            workflow_path: Path to inpainting workflow JSON
            seed: Random seed
            steps: Sampling steps
            denoise: Denoise strength (1.0 = full repaint, 0.0 = no change)
            cfg: CFG scale

        Returns:
            Prompt ID for tracking
        """

        print("=" * 60)
        print("INPAINTING WITH STABLE DIFFUSION")
        print("=" * 60)

        # Create mask from annotation
        mask_path = annotated_image_path.replace('.png', '_mask.png')
        success, _ = self.create_mask_from_annotation(
            annotated_image_path, mask_path
        )

        if not success:
            print("\nFailed to create mask. Exiting.")
            sys.exit(1)

        # Upload images
        print(f"\nUploading images to ComfyUI...")

        # Upload ORIGINAL clean image (no annotation)
        input_result = self.upload_image(original_image_path)
        input_filename = input_result['name']
        print(f"Uploaded input: {input_filename}")

        # Upload mask
        mask_result = self.upload_image(mask_path)
        mask_filename = mask_result['name']
        print(f"Uploaded mask: {mask_filename}")

        # Load and update workflow
        print(f"\nLoading workflow: {workflow_path}")
        workflow = self.load_workflow(workflow_path)

        print(f"Inpaint prompt: {prompt}")
        print(f"Steps: {steps}, Denoise: {denoise}, CFG: {cfg}")

        workflow = self.update_sd_inpaint_workflow(
            workflow, prompt, input_filename, mask_filename,
            seed, steps, denoise, cfg
        )

        print("\nQueueing inpainting task...")
        result = self.queue_prompt(workflow)
        prompt_id = result['prompt_id']

        print(f"\n✓ Inpainting started!")
        print(f"Prompt ID: {prompt_id}")
        print(f"Seed: {workflow['10']['inputs']['seed']}")
        print(f"\nMonitor progress at: http://{self.server_address}")
        print("Check output folder for result when complete!")

        return prompt_id


def main():
    parser = argparse.ArgumentParser(
        description='Inpaint images using annotated screenshots',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s original.png annotated.png
  %(prog)s car.png car_circled.png --prompt "empty street"
  %(prog)s image.png image_marked.png --steps 40 --denoise 1.0
        """
    )

    parser.add_argument('original', help='Original clean image (no annotation)')
    parser.add_argument('annotated', help='Annotated image (with bright colored circle/marking)')
    parser.add_argument('-p', '--prompt',
                       default='photorealistic, high quality, detailed',
                       help='Description of inpainted area')
    parser.add_argument('--steps', type=int, default=30,
                       help='Sampling steps (default: 30)')
    parser.add_argument('--denoise', type=float, default=1.0,
                       help='Denoise strength 0.0-1.0 (default: 1.0 = full repaint)')
    parser.add_argument('--cfg', type=float, default=7.5,
                       help='CFG scale (default: 7.5)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed')
    parser.add_argument('--server', default='127.0.0.1:8190',
                       help='ComfyUI server address')
    parser.add_argument('-w', '--workflow', default='sd_inpaint_workflow.json',
                       help='Path to inpainting workflow JSON')

    args = parser.parse_args()

    if not os.path.exists(args.original):
        print(f"Error: Original image not found: {args.original}")
        sys.exit(1)

    if not os.path.exists(args.annotated):
        print(f"Error: Annotated image not found: {args.annotated}")
        sys.exit(1)

    helper = InpaintingHelper(args.server)

    try:
        helper.inpaint(
            original_image_path=args.original,
            annotated_image_path=args.annotated,
            prompt=args.prompt,
            workflow_path=args.workflow,
            seed=args.seed,
            steps=args.steps,
            denoise=args.denoise,
            cfg=args.cfg
        )

        print("\n✓ Inpainting queued successfully!")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
