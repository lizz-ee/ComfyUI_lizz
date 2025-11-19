# Lizzchar Video Workflow Guide

## Simple Head Turn with Arcane Style

### Workflow: lizzchar_head_turn_arcane_style.json

This workflow creates a simple video of lizzchar turning her head toward the camera with Arcane animation style.

## Settings:

**Video Output:**
- Resolution: 768x512
- Frames: 121 (5 seconds at 24fps)
- Format: MP4 (H.264)

**Model Settings:**
- Model: LTX-Video 13B
- LoRA: lizzchar_lora.safetensors (strength: 0.85)
- Steps: 25
- CFG: 3.5
- Sampler: euler / simple

**Prompt:**
```
lizzchar, lime green skin character with spiky teal and purple hair, olive green hoodie,
slowly turning head from looking left to looking directly at camera, smooth gentle head rotation,
Arcane animation style, painterly cel-shaded look, dramatic rim lighting, purple and teal color grading,
neon cyberpunk city background with bokeh lights, cinematic depth of field, high quality animation
```

**Negative Prompt:**
```
blurry, low quality, distorted face, double head, bad anatomy, watermark, static, no motion, jittery
```

## How to Use:

1. Open ComfyUI: http://127.0.0.1:8188
2. Load workflow: **workflows/lizzchar_head_turn_arcane_style.json**
3. Click **Queue Prompt**
4. Output saves to: `output/lizzchar_head_turn_arcane_[number].mp4`

## Customization Tips:

### Change Motion:
- "turning head left to right" - Side to side motion
- "nodding slowly" - Up and down nod
- "looking around curiously" - Multiple directions
- "tilting head slightly" - Subtle motion

### Adjust Arcane Style:
- Increase style: Add "thick paint strokes, hand-painted animation"
- More dramatic: Add "high contrast shadows, vibrant colors"
- Softer look: Add "soft lighting, pastel colors"

### Use Reference Image (Advanced):
To use an Arcane image as style reference:
1. Add **IPAdapter** nodes
2. Load Arcane reference image
3. Set IPAdapter strength: 0.6-0.8
4. This will match the exact Arcane aesthetic

### Add ControlNet (Precise Control):
For exact pose/depth control:
1. Create a reference image of the head turn
2. Use **ControlNet Depth** or **Pose** LoRA
3. Load: `ltxv-097-ic-lora-pose-control-comfyui.safetensors`

## Next Steps:

**Upgrade Quality:**
- Use **Spatial Upscaler** LoRA for higher resolution
- Use **Temporal Upscaler** LoRA for smoother motion

**Try Other Styles:**
- Anime style: "anime art style, vibrant colors"
- Realistic: "photorealistic, detailed skin texture"
- Painterly: "oil painting style, impressionist"

Output location: `D:\ComfyUI_lizz\output\`
