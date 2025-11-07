"""
AI Inpaint Studio - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from routers import generate, inpaint, health

app = FastAPI(
    title="AI Inpaint Studio API",
    description="Backend API for AI image generation and inpainting",
    version="0.1.0"
)

# CORS middleware - allows Electron frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for serving generated images
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(generate.router, prefix="/api", tags=["generate"])
app.include_router(inpaint.router, prefix="/api", tags=["inpaint"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Inpaint Studio API",
        "version": "0.1.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
