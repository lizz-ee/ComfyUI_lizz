# Lizzchar Hunyuan Video Workflow Guide

## Workflow: lizzchar_hunyuan_head_turn.json

This workflow generates high-quality video of lizzchar turning her head with Arcane style using Hunyuan Video.

## Video Output:
- **Resolution**: 1280x720 (720p)
- **Frames**: 129 (5.4 seconds at 24fps)
- **Format**: MP4 (H.264)
- **Quality**: High (25GB model, better than LTX)

## Model Settings:
- **Model**: Hunyuan Video T2V 720p BF16 (25.6GB)
- **LoRA**: lizzchar_lora.safetensors (strength: 0.85)
- **VAE**: hunyuan_video_vae_bf16.safetensors
- **Steps**: 30
- **CFG**: 6.0
- **Denoise**: 1.0
- **Sampler**: ddim

## Prompt:
```
lizzchar, lime green skin character with spiky teal and purple hair, olive green hoodie,
slowly turning head from looking left to looking directly at camera, smooth gentle head rotation,
Arcane animation style, painterly cel-shaded look, dramatic rim lighting, purple and teal color grading,
neon cyberpunk city background with bokeh lights, cinematic depth of field, high quality animation
```

## Negative Prompt:
```
blurry, low quality, distorted face, double head, bad anatomy, watermark, static, no motion, jittery
```

## How to Use:

1. Open ComfyUI: http://127.0.0.1:8188
2. Load workflow: **workflows/lizzchar_hunyuan_head_turn.json**
3. Click **Queue Prompt**
4. **Wait time**: ~5-10 minutes (it's a big model!)
5. Output: `output/lizzchar_hunyuan_head_turn_[number].mp4`

## Why Hunyuan Instead of LTX?

- **Higher Quality**: 25GB vs 5GB model
- **Better Detail**: More parameters = better results
- **Stable**: Fully supported in ComfyUI (LTX has compatibility issues)
- **720p Native**: Better resolution out of the box

## Customization Tips:

### Change Motion:
- "turning head left to right" - Side motion
- "nodding head up and down" - Vertical nod
- "tilting head curiously" - Subtle tilt
- "looking around the environment" - Multiple directions

### Adjust Style:
- **More Arcane**: Add "thick paint strokes, vibrant neon colors, high contrast"
- **Softer**: Add "soft lighting, gentle shadows, pastel tones"
- **Cinematic**: Add "film grain, anamorphic lens, bokeh"

### Video Length:
Change frames in `EmptyHunyuanVideoLatent` node:
- 49 frames = 2 seconds
- 97 frames = 4 seconds
- 129 frames = 5.4 seconds (default)
- 193 frames = 8 seconds

**Note**: Longer videos = longer generation time!

### Resolution:
Available in `EmptyHunyuanVideoLatent`:
- 1280x720 (720p) - Default, fastest
- 1920x1080 (1080p) - Higher quality, slower

## Troubleshooting:

**Out of memory?**
- Reduce resolution to 960x544
- Reduce frames to 97 or 49
- Close other applications

**Generation takes forever?**
- Normal! Hunyuan is slow but high quality
- 30 steps × 129 frames = lots of computation
- Reduce steps to 20 for faster (but lower quality)

**Video looks static?**
- Increase CFG to 7.0 or 8.0 for stronger motion
- Make prompt more specific about the motion
- Try different seed values

Output location: `D:\ComfyUI_lizz\output\`
