# FLUX Character Sheet Pipeline - READY!

## What's Installed

### ✅ FLUX.1-dev Model (11GB)
- **Location:** `models/checkpoints/flux1-dev-fp8.safetensors`
- **Type:** FP8 optimized for 24GB VRAM
- **Quality:** High-quality image generation

### ✅ Text Encoders
- **CLIP-L:** `models/clip/clip_l.safetensors` (246MB)
- **T5-XXL FP8:** `models/clip/t5xxl_fp8_e4m3fn.safetensors` (9.5GB)

### ✅ FLUX IP-Adapter
- **Model:** `models/xlabs/ipadapters/flux-ip-adapter.bin` (1.4GB)
- **Extension:** `custom_nodes/ComfyUI-IPAdapter-Flux`
- **Purpose:** Character consistency across multiple angles

### ✅ FLUX ControlNet (4.08GB)
- **Model:** `models/controlnet/flux1-dev-controlnet-union-pro-2.0.safetensors`
- **Type:** Shakker-Labs Union Pro 2.0
- **Supports:** Canny, Soft Edge, Depth, Pose control
- **Purpose:** Precise pose and structure control for character sheets

### ✅ ControlNet Auxiliary Preprocessors
- **Extension:** `custom_nodes/comfyui_controlnet_aux`
- **Includes:** OpenPose, Depth, Canny, and other preprocessors
- **Purpose:** Extract pose/structure from reference images

### ✅ Reference Character
- **Input:** `output/character_only.png` (extracted from Arcane image)
- **Background:** Transparent, red areas removed
- **Ready for:** IP-Adapter reference

---

## What This Enables

### Character Sheet Generation
Transform your single character image into:
- **Multiple angles**: Front, side, back, three-quarter views
- **Different expressions**: Happy, sad, angry, etc.
- **Various poses**: Standing, sitting, action poses
- **Different environments**: While maintaining character consistency

### Key Features
1. **Consistent facial features** across all generations
2. **High-quality FLUX rendering** (better than SD1.5)
3. **Multiple output options** - single sheet or separate images
4. **Style flexibility** - Arcane, Disney, Anime, Pixar, realistic

---

## How to Use

### Step 1: Open ComfyUI
Go to: http://127.0.0.1:8188

### Step 2: Load FLUX Workflow
A workflow will be created that includes:
- FLUX.1-dev checkpoint loader
- IP-Adapter for character consistency
- Your character image as reference
- Prompt for character sheet generation

### Step 3: Generate Character Sheet
**Single Multi-Angle Sheet:**
Prompt: "character turnaround, character sheet, front view side view back view, full body character standing, white background"

**Separate Angle Generations:**
- Front: "full body character, front view, standing, white background" (seed: 1)
- Side: "full body character, side profile, standing, white background" (seed: 2)
- Back: "full body character, back view, standing, white background" (seed: 3)
- 3/4: "full body character, three-quarter view, standing, white background" (seed: 4)

### Step 4: Settings
- **CFG:** 1.0 (FLUX requirement)
- **Steps:** 20-30 (more steps = better quality)
- **Resolution:** 1024×1024 for single character, 1536×1024 for character sheet
- **Sampler:** euler or dpmpp_sde
- **IP-Adapter Weight:** 0.6-0.8 (higher = more similar to reference)

---

## Workflows Available

### 1. Basic FLUX Character Sheet Workflow
**File:** `flux_character_sheet_workflow.json`

This workflow includes:
- FLUX.1-dev model loader
- Dual CLIP text encoders (CLIP-L + T5-XXL)
- IP-Adapter for character consistency from `character_only.png`
- Optimized for 1536×1024 character sheet generation
- Fixed seed (42) for reproducibility

**To use:**
1. Open ComfyUI at http://127.0.0.1:8188
2. Load `flux_character_sheet_workflow.json`
3. Adjust the prompt in the CLIPTextEncode node
4. Click "Queue Prompt" to generate

### 2. Example Workflows
**Location:** `custom_nodes/ComfyUI-IPAdapter-Flux/workflows/`
- `ipadapter_example.json` - Basic IP-Adapter setup
- `multi-ipadapter_example.json` - Multiple IP-Adapters
- `ipadapter_example_start_end_percent.json` - Temporal control

## Next Steps

1. **Load workflow** in ComfyUI (http://127.0.0.1:8188)
2. **Generate test character sheet** with default settings
3. **Adjust settings** based on results
4. **Experiment** with different prompts and angles

---

## Tips for Best Results

### Character Consistency
- Keep the same seed for similar results
- Adjust IP-Adapter weight (0.6 = more creative, 0.8 = more faithful)
- Use detailed prompts describing character features

### Multiple Angles
- Generate separately for more control
- Use consistent lighting/background
- Compile in image editor for final character sheet

### Style Transfer
- Add style keywords: "Arcane style", "Pixar style", "Disney style"
- Use negative prompts to avoid unwanted styles
- Test different FLUX models for different aesthetics

---

## Comparison: FLUX vs SD1.5

| Feature | FLUX.1-dev | Arcane Diffusion (SD1.5) |
|---------|-----------|---------------------------|
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Speed | Medium | Fast |
| VRAM | ~16GB | ~8GB |
| Character Consistency | Excellent with IP-Adapter | Good with IP-Adapter |
| Prompt Following | Excellent | Good |
| Multi-angle Generation | Excellent | Moderate |

---

## Files Installed

### Models
- `models/checkpoints/flux1-dev-fp8.safetensors` - Main FLUX model (11GB)
- `models/clip/clip_l.safetensors` - CLIP text encoder (246MB)
- `models/clip/t5xxl_fp8_e4m3fn.safetensors` - T5 text encoder (9.5GB)
- `models/xlabs/ipadapters/flux-ip-adapter.bin` - Character consistency (1.4GB)
- `models/controlnet/flux1-dev-controlnet-union-pro-2.0.safetensors` - Pose control (4.08GB)
- `models/vae/ae.safetensors` - VAE for FLUX

### Extensions
- `custom_nodes/ComfyUI-IPAdapter-Flux/` - FLUX IP-Adapter support
- `custom_nodes/comfyui_controlnet_aux/` - ControlNet preprocessors

### Workflows
- `flux_character_sheet_workflow.json` - Ready-to-use character sheet workflow
- `character_only.png` - Your extracted reference character

### Total Size: ~26.3GB

---

## Ready to Generate!

Once ComfyUI finishes loading, you'll be able to:
1. Load the FLUX character sheet workflow
2. Generate consistent character designs
3. Create professional character reference sheets
4. Use for animation, game development, or LoRA training
