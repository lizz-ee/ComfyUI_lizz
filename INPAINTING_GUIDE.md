# ComfyUI Inpainting Guide

Remove or modify parts of images using AI-powered inpainting.

## Quick Start

### 1. Setup

**Required Models:**
- SD 1.5 Inpainting Model (download automatically or manually from Hugging Face)
  - Place in: `models/checkpoints/sd-v1-5-inpainting.safetensors`

**Required Files:**
- `flux_inpaint.py` - Inpainting script
- `sd_inpaint_workflow.json` - ComfyUI workflow for inpainting

### 2. Basic Usage

**From Chat (Recommended):**
1. Take a screenshot or open an image
2. Draw a bright colored circle/annotation around what you want to remove (use red, blue, cyan, etc.)
3. Save the annotated image
4. Send to Claude with instruction: "remove this car" or "remove this object"

**From Command Line:**
```bash
# Basic usage
python3 flux_inpaint.py annotated_image.png

# With custom prompt
python3 flux_inpaint.py car_circled.png --prompt "empty wet street, night scene"

# Fine-tune parameters
python3 flux_inpaint.py object_marked.png --steps 40 --cfg 8.0 --denoise 1.0
```

### 3. How It Works

1. **Annotation Detection**: Script automatically detects bright colored annotations
2. **Mask Creation**: Creates a binary mask from the annotation
3. **Inpainting**: Uses SD 1.5 inpainting model to fill the masked area
4. **Result**: Saves completed image with object removed

## Parameters

### --prompt (string)
What the inpainted area should contain.

**Examples:**
- `"empty street, realistic"` - For removing cars/objects
- `"brick wall texture"` - For removing graffiti
- `"clear sky"` - For removing power lines
- `"grass and flowers"` - For removing unwanted objects from landscape

**Default:** `"photorealistic, high quality, detailed"`

### --steps (int)
Number of denoising steps. More steps = better quality but slower.

**Range:** 20-50
**Default:** 30
**Recommended:**
- Quick test: 20
- Good quality: 30
- Best quality: 40-50

### --denoise (float)
How much to change the masked area.

**Range:** 0.0-1.0
**Default:** 1.0 (full repaint)
**Recommended:**
- Remove object completely: 1.0
- Subtle modification: 0.6-0.8
- Small touch-up: 0.4-0.6

### --cfg (float)
Classifier-Free Guidance scale. How strictly to follow the prompt.

**Range:** 1.0-20.0
**Default:** 7.5
**Recommended:**
- Creative freedom: 5.0-7.0
- Balanced: 7.5
- Strict adherence: 9.0-12.0

### --seed (int)
Random seed for reproducibility.

**Default:** Random
**Usage:** Set to specific number to get same result

## Tips for Best Results

### 1. Annotation Quality
- Use **bright, saturated colors** (red, blue, cyan, green)
- Draw slightly **outside** the object you want to remove
- Make sure annotation is **clearly visible**
- Avoid colors that appear naturally in the image

### 2. Prompt Writing
- Describe the **background** that should replace the object
- Match the **style and context** of the original image
- Be specific about **lighting, texture, and atmosphere**

**Good Examples:**
- Removing car from street: `"empty wet asphalt street, neon reflections, night scene, urban environment"`
- Removing person from beach: `"sandy beach, ocean waves, sunny day, natural lighting"`
- Removing text from sign: `"clean metal sign, weathered texture, outdoor lighting"`

**Bad Examples:**
- Too vague: `"background"`
- Wrong context: `"grass"` (when removing car from city street)
- Too specific: `"exactly matching the surrounding pixels"` (model doesn't understand this)

### 3. Troubleshooting

**Problem: Mask not detected**
- Solution: Use brighter, more saturated annotation color
- Check: Annotation must have high saturation (not gray/dark)

**Problem: Too much masked**
- Solution: Use more precise annotation, avoid colors present in image
- Check: Script will warn if mask covers >5% of image

**Problem: Inpainted area doesn't match**
- Solution: Improve prompt to better describe the background
- Try: Increase CFG scale (9-12) for stricter following of prompt

**Problem: Visible seams/artifacts**
- Solution: Increase steps (40-50), ensure annotation slightly overlaps object edges
- Try: Lower denoise (0.9) for better blending

## Advanced Usage

### Custom Workflows

You can modify `sd_inpaint_workflow.json` to:
- Use different models (SDXL inpainting)
- Add ControlNet for better structure preservation
- Chain multiple inpainting operations

### Batch Processing

Process multiple images:
```bash
for img in annotated_*.png; do
    python3 flux_inpaint.py "$img" --prompt "clean background"
done
```

### Integration

Import as module:
```python
from flux_inpaint import InpaintingHelper

helper = InpaintingHelper("127.0.0.1:8190")
prompt_id = helper.inpaint(
    annotated_image_path="test.png",
    prompt="empty street scene",
    steps=30,
    cfg=7.5
)
```

## Examples

### Example 1: Remove Car from Street
```bash
# Annotate car with red circle
python3 flux_inpaint.py street_car.png --prompt "empty wet asphalt street, urban night scene, neon reflections"
```

### Example 2: Remove Person from Photo
```bash
python3 flux_inpaint.py tourist.png --prompt "ancient stone wall, historical architecture, natural lighting" --steps 40
```

### Example 3: Remove Watermark
```bash
python3 flux_inpaint.py watermarked.png --prompt "clean photo, matching background texture" --cfg 9.0
```

### Example 4: Remove Power Lines
```bash
python3 flux_inpaint.py power_lines.png --prompt "clear blue sky, natural clouds" --denoise 1.0
```

## Model Information

**SD 1.5 Inpainting Model:**
- Specifically trained for inpainting tasks
- Better at preserving untouched areas than base SD 1.5
- Optimized for removing objects and filling masked regions
- Size: ~4 GB
- VRAM: 4-6 GB recommended

## Workflow Details

The `sd_inpaint_workflow.json` workflow:
1. Loads SD 1.5 inpainting checkpoint
2. Encodes positive and negative prompts
3. Loads input image and mask
4. Encodes image with VAEEncodeForInpaint
5. Runs KSampler with inpainting latents
6. Decodes and saves result

## Support

For issues or questions:
- Check console output for error messages
- Ensure ComfyUI is running (http://127.0.0.1:8190)
- Verify model file exists in `models/checkpoints/`
- Test with simple annotated image first
