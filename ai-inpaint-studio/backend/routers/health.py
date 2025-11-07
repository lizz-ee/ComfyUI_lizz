"""
Health check endpoints
"""

from fastapi import APIRouter
import urllib.request
import json

# Make torch and psutil optional
try:
    import torch
    TORCH_AVAILABLE = True
except Exception:
    # Catch ImportError, OSError (DLL issues), and any other import problems
    TORCH_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Check backend and ComfyUI health status
    """

    # Check if CUDA/GPU is available
    gpu_available = False
    gpu_name = "N/A"
    vram_used = "N/A"
    vram_total = "N/A"

    if TORCH_AVAILABLE:
        gpu_available = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if gpu_available else "N/A"

        # Get VRAM usage
        if gpu_available:
            vram_used_bytes = torch.cuda.memory_allocated(0)
            vram_total_bytes = torch.cuda.get_device_properties(0).total_memory
            vram_used = f"{vram_used_bytes / 1024**3:.2f} GB"
            vram_total = f"{vram_total_bytes / 1024**3:.2f} GB"

    # Check if ComfyUI is running
    comfyui_running = False
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8190", timeout=1)
        comfyui_running = response.status == 200
    except:
        pass

    # Get system RAM
    ram_used = "N/A"
    ram_total = "N/A"
    if PSUTIL_AVAILABLE:
        ram = psutil.virtual_memory()
        ram_used = f"{ram.used / 1024**3:.2f} GB"
        ram_total = f"{ram.total / 1024**3:.2f} GB"

    return {
        "status": "ok",
        "backend": {
            "running": True,
            "version": "0.1.0"
        },
        "comfyui": {
            "running": comfyui_running,
            "url": "http://127.0.0.1:8190"
        },
        "hardware": {
            "gpu_available": gpu_available,
            "gpu_name": gpu_name,
            "vram_used": vram_used,
            "vram_total": vram_total,
            "ram_used": ram_used,
            "ram_total": ram_total
        }
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong"}
