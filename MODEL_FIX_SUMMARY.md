# Hunyuan Model Fix - Summary

## Problem Identified

The Hunyuan Video model files were downloaded from the official Tencent repository instead of Kijai's ComfyUI-compatible repository. The official models have a `model.model.` prefix on all state dict keys, but ComfyUI-HunyuanVideoWrapper expects keys without this prefix.

**Error encountered:**
```
KeyError: 'img_in.proj.weight'
```

**Root cause:** The code looks for `sd["img_in.proj.weight"]` but the actual key in the file is `model.model.img_in.proj.weight`.

## Solution Applied

Created and ran a Python script ([fix_hunyuan_model_keys.py](fix_hunyuan_model_keys.py)) that:
1. Loaded both model files
2. Stripped the `model.model.` prefix from all keys
3. Saved fixed versions
4. Swapped the files

## Files Fixed

### Text-to-Video Model
- **Original:** `models/diffusion_models/hunyuan_video/hunyuan_video_t2v_720p_bf16.safetensors` (24GB)
  - Now backed up as: `hunyuan_video_t2v_720p_bf16_orig.safetensors`
- **Fixed version:** Now in place as `hunyuan_video_t2v_720p_bf16.safetensors`
  - Keys changed: 856 keys, `model.model.*` → `*`

### Image-to-Video Model
- **Original:** `models/diffusion_models/hunyuan_video/hunyuan_video_image_to_video_720p_bf16.safetensors`
  - Now backed up as: `hunyuan_video_image_to_video_720p_bf16_orig.safetensors`
- **Fixed version:** Now in place as `hunyuan_video_image_to_video_720p_bf16.safetensors`
  - Keys changed: 852 keys, `model.model.*` → `*`

## Next Steps

1. **Restart ComfyUI** to clear any cached model data
2. **Test without LoRA first:** Load [workflows/lizzchar_hyvideo_head_turn_no_lora.json](workflows/lizzchar_hyvideo_head_turn_no_lora.json)
   - This tests if the model loads correctly without the character LoRA
3. **If successful, test with LoRA:** Load [workflows/lizzchar_hyvideo_head_turn.json](workflows/lizzchar_hyvideo_head_turn.json)
   - The lizzchar_lora.safetensors was trained on FLUX, so it may not be compatible with Hunyuan
   - If it fails, we'll need to either:
     - Use the workflow without LoRA for now
     - Train a new LoRA specifically for Hunyuan Video

## Correct Model Source

For future reference, Hunyuan Video models should be downloaded from:
**https://huggingface.co/Kijai/HunyuanVideo_comfy/tree/main**

These models are pre-formatted for ComfyUI compatibility.

## Commands to Restart ComfyUI

Stop the current ComfyUI server and restart it to clear the model cache:
```bash
# The server is running on port 8188
# Kill it and restart
```
