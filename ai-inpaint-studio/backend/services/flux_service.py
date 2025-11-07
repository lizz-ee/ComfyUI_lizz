"""
Service for FLUX text-to-image generation
Wraps the flux_generate.py script
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Add parent directory to path to import flux_generate
# Path structure: ComfyUI_lizz/ai-inpaint-studio/backend/services/flux_service.py
# We need to go up to ComfyUI_lizz/ where flux_generate.py is located
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from flux_generate import FluxGenerator


class FluxService:
    def __init__(self, comfyui_address: str = "127.0.0.1:8190"):
        self.generator = FluxGenerator(comfyui_address)
        self.workflow_path = str(root_dir / "flux_txt2img_workflow.json")

    async def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        steps: int = 20,
        seed: Optional[int] = None,
        style: str = "photorealistic"
    ) -> dict:
        """
        Generate an image from a text prompt

        Args:
            prompt: Text description
            width: Image width
            height: Image height
            steps: Sampling steps
            seed: Random seed
            style: Style preset (adds to prompt)

        Returns:
            dict with prompt_id, seed, and output info
        """

        # Apply style presets
        style_prompts = {
            "photorealistic": "photorealistic, highly detailed, 8k, professional photography",
            "artistic": "artistic, painterly, creative, expressive",
            "cinematic": "cinematic, dramatic lighting, movie scene, high quality",
            "anime": "anime style, vibrant colors, detailed illustration",
            "sketch": "pencil sketch, hand drawn, artistic, detailed linework"
        }

        # Enhance prompt with style
        if style in style_prompts:
            enhanced_prompt = f"{prompt}, {style_prompts[style]}"
        else:
            enhanced_prompt = prompt

        # Generate filename prefix based on style
        filename_prefix = f"flux_{style}"

        # Queue generation
        prompt_id = self.generator.generate(
            prompt=enhanced_prompt,
            width=width,
            height=height,
            steps=steps,
            seed=seed,
            workflow_path=self.workflow_path,
            filename_prefix=filename_prefix
        )

        # Get the actual seed used
        workflow = self.generator.load_workflow(self.workflow_path)
        actual_seed = workflow.get("25", {}).get("inputs", {}).get("noise_seed", seed or 0)

        # Get output path (ComfyUI saves to output directory)
        output_dir = root_dir / "output"

        return {
            "prompt_id": prompt_id,
            "seed": actual_seed,
            "output_dir": str(output_dir),
            "filename_prefix": filename_prefix,
            "status": "queued"
        }

    async def get_generation_status(self, prompt_id: str) -> dict:
        """
        Check the status of a generation

        Args:
            prompt_id: The prompt ID returned from generate_image

        Returns:
            dict with status and output info if completed
        """
        history = self.generator.get_history(prompt_id)

        if prompt_id not in history:
            return {"status": "unknown", "prompt_id": prompt_id}

        prompt_info = history[prompt_id]

        if 'outputs' in prompt_info:
            # Extract output image info
            output_images = []
            for node_id, output in prompt_info['outputs'].items():
                if 'images' in output:
                    for img in output['images']:
                        filename = img.get('filename', '')
                        subfolder = img.get('subfolder', '')
                        output_images.append({
                            "filename": filename,
                            "subfolder": subfolder,
                            "path": os.path.join('output', subfolder, filename) if subfolder else os.path.join('output', filename)
                        })

            return {
                "status": "completed",
                "prompt_id": prompt_id,
                "images": output_images
            }

        if 'status' in prompt_info:
            status_info = prompt_info['status']
            if 'exception_message' in status_info:
                return {
                    "status": "error",
                    "prompt_id": prompt_id,
                    "error": status_info['exception_message']
                }

        return {
            "status": "processing",
            "prompt_id": prompt_id
        }
