"""
Text-to-image generation endpoints
"""

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
import os

router = APIRouter()


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

    # TODO: Import and call flux_generate service
    # For now, return mock response

    return {
        "image_path": "output/mock_image.png",
        "prompt_id": "mock_123",
        "seed": request.seed or 12345,
        "generation_time": 2.5
    }


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
