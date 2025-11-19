#!/usr/bin/env python
"""
Fix Hunyuan model keys by stripping 'model.model.' prefix
This is needed when the model was downloaded from the official Tencent repo
instead of Kijai's ComfyUI-compatible repo.
"""
import os
from safetensors import safe_open
from safetensors.torch import save_file
import torch

model_path = "models/diffusion_models/hunyuan_video/hunyuan_video_t2v_720p_bf16.safetensors"
output_path = "models/diffusion_models/hunyuan_video/hunyuan_video_t2v_720p_bf16_fixed.safetensors"
backup_path = "models/diffusion_models/hunyuan_video/hunyuan_video_t2v_720p_bf16_orig.safetensors"

print(f"Loading model from: {model_path}")
print("This may take a few minutes...")

# Load the model
state_dict = {}
with safe_open(model_path, framework="pt") as f:
    for key in f.keys():
        state_dict[key] = f.get_tensor(key)

print(f"Loaded {len(state_dict)} keys")

# Check if keys have the 'model.model.' prefix
sample_keys = list(state_dict.keys())[:5]
print(f"\nSample keys before fix:")
for k in sample_keys:
    print(f"  {k}")

# Strip the 'model.model.' prefix
fixed_dict = {}
for key, value in state_dict.items():
    if key.startswith("model.model."):
        new_key = key.replace("model.model.", "", 1)
        fixed_dict[new_key] = value
    else:
        fixed_dict[key] = value

print(f"\nSample keys after fix:")
for k in list(fixed_dict.keys())[:5]:
    print(f"  {k}")

# Save the fixed model
print(f"\nSaving fixed model to: {output_path}")
save_file(fixed_dict, output_path)

print(f"\nDone! Fixed model saved to: {output_path}")
print(f"Original model is still at: {model_path}")
print(f"\nTo use the fixed model, either:")
print(f"1. Rename the files manually:")
print(f"   move \"{model_path}\" \"{backup_path}\"")
print(f"   move \"{output_path}\" \"{model_path}\"")
print(f"2. Or update the workflow to use: hunyuan_video\\\\hunyuan_video_t2v_720p_bf16_fixed.safetensors")
