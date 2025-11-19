from huggingface_hub import hf_hub_download
import os

models_dir = r"C:\Users\User\Desktop\ComfyUI_lizz\models\diffusion_models"

print("Downloading Hunyuan Video Text-to-Video BF16 model...")
print("=" * 60)
print("Size: ~25.6GB")
print("This will take a while with your internet connection...")
print("")

try:
    file_path = hf_hub_download(
        repo_id="Comfy-Org/HunyuanVideo_repackaged",
        filename="hunyuan_video_t2v_720p_bf16.safetensors",
        local_dir=models_dir
    )
    print(f"\n[SUCCESS] Downloaded to: {file_path}")
except Exception as e:
    print(f"\n[ERROR] Download failed: {str(e)}")
    print("\nTrying alternative source...")

    # Try Kijai repo as backup
    try:
        file_path = hf_hub_download(
            repo_id="Kijai/HunyuanVideo_comfy",
            filename="hunyuan_video_720_bf16.safetensors",
            local_dir=models_dir
        )
        print(f"[SUCCESS] Downloaded from alternative source: {file_path}")
    except Exception as e2:
        print(f"[ERROR] Alternative download also failed: {str(e2)}")

print("=" * 60)
