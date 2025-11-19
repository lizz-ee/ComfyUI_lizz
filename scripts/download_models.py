from huggingface_hub import hf_hub_download
import os

models_dir = r"C:\Users\User\Desktop\ComfyUI_lizz\models"

print("Downloading video generation models...")
print("=" * 60)

# Download Mochi-1 model
print("\n[1/3] Downloading Mochi-1 model (~17GB)...")
try:
    mochi_path = hf_hub_download(
        repo_id="Comfy-Org/mochi_preview_repackaged",
        filename="split_files/diffusion_models/mochi_preview_dit_fp8_e4m3fn.safetensors",
        local_dir=models_dir,
        local_dir_use_symlinks=False
    )
    print(f"✓ Mochi-1 downloaded to: {mochi_path}")
except Exception as e:
    print(f"✗ Mochi-1 download failed: {e}")

# Download Hunyuan Video model
print("\n[2/3] Downloading Hunyuan Video model (~30GB)...")
try:
    hunyuan_path = hf_hub_download(
        repo_id="Comfy-Org/HunyuanVideo_repackaged",
        filename="split_files/diffusion_models/hunyuan_video_720_cfgdistill_fp8_e4m3fn.safetensors",
        local_dir=models_dir,
        local_dir_use_symlinks=False
    )
    print(f"✓ Hunyuan Video downloaded to: {hunyuan_path}")
except Exception as e:
    print(f"✗ Hunyuan Video download failed: {e}")

# Download LTX VAE
print("\n[3/3] Downloading LTX VAE model...")
try:
    ltx_vae_path = hf_hub_download(
        repo_id="Lightricks/LTX-Video",
        filename="vae_diffusion_pytorch_model.safetensors",
        local_dir=os.path.join(models_dir, "vae"),
        local_dir_use_symlinks=False
    )
    print(f"✓ LTX VAE downloaded to: {ltx_vae_path}")
except Exception as e:
    print(f"✗ LTX VAE download failed: {e}")

print("\n" + "=" * 60)
print("Download complete!")
