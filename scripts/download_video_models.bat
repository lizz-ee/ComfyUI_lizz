@echo off
echo Downloading Video Generation Models
echo =====================================
echo.
echo This will download 3 video models (~56GB total):
echo 1. LTX Video (9GB) - Fast, LoRA friendly
echo 2. Mochi-1 (17GB) - High quality
echo 3. Hunyuan Video (30GB) - Highest quality
echo.
echo Models will be saved to: models\diffusion_models\
echo.
pause

cd /d "%~dp0"

echo.
echo [1/3] Downloading LTX Video (~9GB)...
curl -L "https://huggingface.co/Lightricks/LTX-Video/resolve/main/ltx-video-2b-v0.9.1.safetensors" -o "models\diffusion_models\ltx-video-2b-v0.9.1.safetensors"

echo.
echo [2/3] Downloading Mochi-1 (~17GB)...
curl -L "https://huggingface.co/Comfy-Org/mochi_preview_repackaged/resolve/main/split_files/diffusion_models/mochi_preview_dit_fp8_e4m3fn.safetensors" -o "models\diffusion_models\mochi_preview_dit_fp8_e4m3fn.safetensors"

echo.
echo [3/3] Downloading Hunyuan Video (~30GB)...
curl -L "https://huggingface.co/Comfy-Org/HunyuanVideo_repackaged/resolve/main/split_files/diffusion_models/hunyuan_video_720_cfgdistill_fp8_e4m3fn.safetensors" -o "models\diffusion_models\hunyuan_video_720_cfgdistill_fp8_e4m3fn.safetensors"

echo.
echo =====================================
echo Download complete!
echo Models saved to: models\diffusion_models\
echo.
pause
