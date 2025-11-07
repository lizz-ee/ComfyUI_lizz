"""
Inpainting endpoints
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
import shutil
import os
import uuid

router = APIRouter()


class InpaintResponse(BaseModel):
    result_path: str
    prompt_id: str
    generation_time: float


@router.post("/inpaint", response_model=InpaintResponse)
async def inpaint_image(
    original_image: UploadFile = File(...),
    annotated_image: UploadFile = File(...),
    prompt: str = Form("photorealistic, high quality"),
    negative_prompt: str = Form(""),
    model: str = Form("sd15"),  # "sd15" or "lama"
    steps: int = Form(30),
    cfg: float = Form(7.5),
    denoise: float = Form(1.0)
):
    """
    Inpaint/remove objects from image

    Args:
        original_image: Clean original image (no annotations)
        annotated_image: Image with colored circle/annotation
        prompt: Description of what should replace masked area
        negative_prompt: What to avoid (e.g., "car, vehicle")
        model: Which model to use ("sd15" or "lama")
        steps: Sampling steps
        cfg: CFG scale
        denoise: Denoise strength
    """

    # Create temp directory for uploads
    temp_dir = "static/temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Generate unique ID
    task_id = str(uuid.uuid4())[:8]

    # Save uploaded files
    original_path = f"{temp_dir}/original_{task_id}.png"
    annotated_path = f"{temp_dir}/annotated_{task_id}.png"

    with open(original_path, "wb") as f:
        shutil.copyfileobj(original_image.file, f)

    with open(annotated_path, "wb") as f:
        shutil.copyfileobj(annotated_image.file, f)

    # TODO: Call inpainting service
    # For now, return mock response

    return {
        "result_path": f"output/inpaint_result_{task_id}.png",
        "prompt_id": task_id,
        "generation_time": 5.2
    }


@router.get("/models")
async def list_models():
    """
    List available inpainting models
    """
    return {
        "models": [
            {
                "id": "sd15",
                "name": "Stable Diffusion 1.5 Inpainting",
                "description": "Good for general inpainting with prompts",
                "available": True
            },
            {
                "id": "lama",
                "name": "LaMa (Resolution-robust Large Mask Inpainting)",
                "description": "Best for pure object removal (no prompts needed)",
                "available": False  # Will be True after Phase 4
            }
        ]
    }
