"""
Text-to-image generation endpoints
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
import os
import time

from services.flux_service import FluxService

router = APIRouter()

# Initialize FLUX service
flux_service = FluxService()


class GenerateRequest(BaseModel):
    prompt: str
    style: str = "cinematic"
    steps: int = 20
    width: int = 1024
    height: int = 1024
    seed: Optional[int] = None


class GenerateResponse(BaseModel):
    image_path: str
    prompt_id: str
    seed: int
    generation_time: float


@router.post("/generate", response_model=GenerateResponse)
async def generate_image(request: GenerateRequest):
    """
    Generate image from text prompt using FLUX

    This will call the flux_generate.py script
    """

    try:
        start_time = time.time()

        # Call FLUX generation service
        result = await flux_service.generate_image(
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            seed=request.seed,
            style=request.style
        )

        generation_time = time.time() - start_time

        # Wait for generation to complete (with timeout)
        max_wait = 120  # 2 minutes
        elapsed = 0
        while elapsed < max_wait:
            status = await flux_service.get_generation_status(result['prompt_id'])

            if status['status'] == 'completed':
                # Get the first image path
                image_path = status['images'][0]['path'] if status.get('images') else "output/unknown.png"

                return {
                    "image_path": image_path,
                    "prompt_id": result['prompt_id'],
                    "seed": result['seed'],
                    "generation_time": time.time() - start_time
                }

            elif status['status'] == 'error':
                raise HTTPException(status_code=500, detail=f"Generation failed: {status.get('error', 'Unknown error')}")

            # Still processing, wait a bit
            await asyncio.sleep(2)
            elapsed += 2

        # Timeout
        raise HTTPException(status_code=504, detail="Generation timeout")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket for real-time progress updates
@router.websocket("/ws/generate/{prompt_id}")
async def generate_progress(websocket: WebSocket, prompt_id: str):
    """
    WebSocket endpoint for real-time generation progress
    """
    await websocket.accept()

    try:
        # TODO: Implement actual progress tracking
        # For now, simulate progress
        for i in range(0, 101, 10):
            await websocket.send_json({
                "prompt_id": prompt_id,
                "percent": i,
                "step": i // 5,
                "total_steps": 20,
                "message": f"Generating... {i}%"
            })
            await asyncio.sleep(0.2)

        await websocket.close()
    except WebSocketDisconnect:
        print(f"Client disconnected from progress stream: {prompt_id}")
