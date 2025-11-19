@echo off
echo ============================================
echo   Launching ComfyUI from D:\ComfyUI_lizz
echo ============================================
echo.

cd /d "D:\ComfyUI_lizz"

echo Starting ComfyUI server...
echo Access at: http://127.0.0.1:8188
echo.

python main.py --listen 0.0.0.0 --port 8188

pause
