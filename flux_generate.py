#!/usr/bin/env python3
"""
FLUX Text-to-Image Generation Script
Generate images from text prompts using FLUX models
"""

import json
import urllib.request
import urllib.parse
import random
import argparse
import sys
import os
from typing import Optional


class FluxGenerator:
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

    def get_history(self, prompt_id: str) -> dict:
        """Get the history/status of a prompt"""
        try:
            req = urllib.request.Request(f"{self.base_url}/history/{prompt_id}")
            response = urllib.request.urlopen(req)
            return json.loads(response.read())
        except urllib.error.URLError as e:
            return {}

    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> bool:
        """Wait for a prompt to complete, with status updates"""
        import time

        print(f"\nWaiting for generation to complete...")
        print("(This may take 10-30 seconds depending on your GPU)")

        start_time = time.time()
        last_status = ""

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)

            if prompt_id in history:
                prompt_info = history[prompt_id]

                # Check for completion
                if 'outputs' in prompt_info:
                    print(f"\n✓ Generation completed successfully!")

                    # Show output files
                    for node_id, output in prompt_info['outputs'].items():
                        if 'images' in output:
                            for img in output['images']:
                                filename = img.get('filename', 'unknown')
                                subfolder = img.get('subfolder', '')
                                full_path = os.path.join('output', subfolder, filename) if subfolder else os.path.join('output', filename)
                                print(f"  Output: {full_path}")

                    return True

                # Check for errors
                if 'status' in prompt_info:
                    status = prompt_info['status']
                    if 'status_str' in status and status['status_str'] != last_status:
                        last_status = status['status_str']
                        print(f"  Status: {last_status}")

                    if status.get('completed', False):
                        print(f"\n✓ Task completed!")
                        return True

                    if 'exception_message' in status:
                        print(f"\n✗ Error: {status['exception_message']}")
                        return False

            # Show progress dots
            print(".", end="", flush=True)
            time.sleep(2)

        print(f"\n✗ Timeout after {timeout}s")
        return False

    def load_workflow(self, workflow_path: str) -> dict:
        """Load a workflow JSON file"""
        with open(workflow_path, 'r') as f:
            return json.load(f)

    def update_workflow(self, workflow: dict, prompt: str,
                       width: int = 1024,
                       height: int = 1024,
                       steps: int = 20,
                       seed: Optional[int] = None,
                       filename_prefix: str = "flux") -> dict:
        """Update FLUX workflow with new parameters"""

        # Update prompt (node 6 - text encode)
        if "6" in workflow:
            workflow["6"]["inputs"]["text"] = prompt

        # Update seed (node 25 - random noise)
        if "25" in workflow:
            if seed is not None:
                workflow["25"]["inputs"]["noise_seed"] = seed
            else:
                workflow["25"]["inputs"]["noise_seed"] = random.randint(0, 2**32 - 1)

        # Update steps (node 17 - scheduler)
        if "17" in workflow:
            workflow["17"]["inputs"]["steps"] = steps

        # Update dimensions (node 27 - empty latent, node 30 - model sampling)
        if "27" in workflow:
            workflow["27"]["inputs"]["width"] = width
            workflow["27"]["inputs"]["height"] = height

        if "30" in workflow:
            workflow["30"]["inputs"]["width"] = width
            workflow["30"]["inputs"]["height"] = height

        # Update output filename prefix (node 9 - save image)
        if "9" in workflow:
            workflow["9"]["inputs"]["filename_prefix"] = filename_prefix

        return workflow

    def generate(self, prompt: str,
                width: int = 1024,
                height: int = 1024,
                steps: int = 20,
                seed: Optional[int] = None,
                workflow_path: str = "flux_txt2img_workflow.json",
                filename_prefix: str = "flux") -> str:
        """
        Generate an image from a text prompt

        Args:
            prompt: Text description of desired image
            width: Image width in pixels
            height: Image height in pixels
            steps: Sampling steps (more = better quality, slower)
            seed: Random seed for reproducibility
            workflow_path: Path to FLUX workflow JSON
            filename_prefix: Prefix for output filename

        Returns:
            Prompt ID for tracking
        """

        print("=" * 60)
        print("FLUX TEXT-TO-IMAGE GENERATION")
        print("=" * 60)

        # Load and update workflow
        print(f"\nLoading workflow: {workflow_path}")
        workflow = self.load_workflow(workflow_path)

        print(f"Prompt: {prompt}")
        print(f"Size: {width}x{height}")
        print(f"Steps: {steps}")

        workflow = self.update_workflow(
            workflow, prompt, width, height, steps, seed, filename_prefix
        )

        print("\nQueueing generation task...")
        result = self.queue_prompt(workflow)
        prompt_id = result['prompt_id']

        print(f"\n✓ Generation queued!")
        print(f"Prompt ID: {prompt_id}")
        print(f"Seed: {workflow['25']['inputs']['noise_seed']}")

        # Wait for completion and show status
        success = self.wait_for_completion(prompt_id)

        if not success:
            print(f"\n✗ Generation failed or timed out")
            print(f"Check ComfyUI console for errors: http://{self.server_address}")

        return prompt_id


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using FLUX models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "a beautiful sunset over mountains"
  %(prog)s "portrait of a cat" --steps 30 --width 512 --height 512
  %(prog)s "futuristic city" --seed 42
        """
    )

    parser.add_argument('prompt', help='Text description of desired image')
    parser.add_argument('--width', type=int, default=1024,
                       help='Image width in pixels (default: 1024)')
    parser.add_argument('--height', type=int, default=1024,
                       help='Image height in pixels (default: 1024)')
    parser.add_argument('--steps', type=int, default=20,
                       help='Sampling steps (default: 20)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--server', default='127.0.0.1:8190',
                       help='ComfyUI server address')
    parser.add_argument('-w', '--workflow', default='flux_txt2img_workflow.json',
                       help='Path to FLUX workflow JSON')
    parser.add_argument('--prefix', default='flux',
                       help='Output filename prefix')

    args = parser.parse_args()

    generator = FluxGenerator(args.server)

    try:
        generator.generate(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            seed=args.seed,
            workflow_path=args.workflow,
            filename_prefix=args.prefix
        )

        print("\n✓ Generation queued successfully!")

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
