@echo off
echo Starting ComfyUI with IMAX optimizations...
echo.
echo Optimizations enabled:
echo - HIGH_VRAM mode (uses all 24GB)
echo - xFormers attention (faster processing)
echo - CUDA optimization
echo.
cd /d "C:\Users\User\Desktop\ComfyUI_lizz"
python main.py --highvram
pause
