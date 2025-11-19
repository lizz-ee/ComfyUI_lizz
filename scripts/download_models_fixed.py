from huggingface_hub import hf_hub_download
import os

models_dir = r"C:\Users\User\Desktop\ComfyUI_lizz\models"
diffusion_models_dir = os.path.join(models_dir, "diffusion_models")
vae_dir = os.path.join(models_dir, "vae")

print("Downloading video generation models...")
print("=" * 60)

# Download Mochi-1 model (Kijai repo)
print("\n[1/3] Downloading Mochi-1 model (~10.3GB)...")
print("This will take a while...")
try:
    mochi_path = hf_hub_download(
        repo_id="Kijai/Mochi_preview_comfy",
        filename="mochi_preview_dit_fp8_e4m3fn.safetensors",
        local_dir=diffusion_models_dir
    )
    print(f"[OK] Mochi-1 downloaded successfully")
except Exception as e:
    print(f"[ERROR] Mochi-1 download failed: {str(e)}")

# Download Hunyuan Video model (Kijai repo)
print("\n[2/3] Downloading Hunyuan Video model (~13.2GB)...")
print("This will take a while...")
try:
    hunyuan_path = hf_hub_download(
        repo_id="Kijai/HunyuanVideo_comfy",
        filename="hunyuan_video_720_cfgdistill_fp8_e4m3fn.safetensors",
        local_dir=diffusion_models_dir
    )
    print(f"[OK] Hunyuan Video downloaded successfully")
except Exception as e:
    print(f"[ERROR] Hunyuan Video download failed: {str(e)}")

# Download Hunyuan VAE
print("\n[3/3] Downloading Hunyuan Video VAE (~493MB)...")
try:
    hunyuan_vae_path = hf_hub_download(
        repo_id="Kijai/HunyuanVideo_comfy",
        filename="hunyuan_video_vae_bf16.safetensors",
        local_dir=vae_dir
    )
    print(f"[OK] Hunyuan VAE downloaded successfully")
except Exception as e:
    print(f"[ERROR] Hunyuan VAE download failed: {str(e)}")

print("\n" + "=" * 60)
print("Download process complete!")
print("Check the messages above to see which files downloaded successfully.")
