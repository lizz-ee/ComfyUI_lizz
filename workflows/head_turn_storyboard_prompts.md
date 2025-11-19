# Lizzchar Head Turn - IMAX Storyboard Sequence
**Resolution**: 2048×1433 (IMAX Digital 2K - 1.43:1 aspect ratio)
**LoRA**: lizzchar_lora.safetensors @ 0.85 strength
**Style**: Arcane animation, painterly, cinematic

## Storyboard Frame Prompts

### Frame 1: Starting Position (Full Left Profile)
```
FRAME 1: lizzchar woman with purple streaks in dark hair, full left side profile, looking to the left, Arcane animation style, dramatic rim lighting, detailed facial features, cinematic IMAX composition, high quality, painterly
```

### Frame 2: Beginning Turn (30° rotation)
```
FRAME 2: lizzchar woman with purple streaks in dark hair, three-quarter left profile, head beginning to turn toward camera, smooth motion, Arcane animation style, dramatic rim lighting, detailed facial features, cinematic IMAX composition, high quality, painterly
```

### Frame 3: Mid Turn (60° rotation)
```
FRAME 3: lizzchar woman with purple streaks in dark hair, partial side view turning toward camera, head rotation midpoint, smooth motion, Arcane animation style, dramatic rim lighting, detailed facial features, cinematic IMAX composition, high quality, painterly
```

### Frame 4: Three-Quarter View (75° rotation)
```
FRAME 4: lizzchar woman with purple streaks in dark hair, three-quarter front view, nearly facing camera, smooth head rotation, Arcane animation style, dramatic rim lighting, detailed facial features, cinematic IMAX composition, high quality, painterly
```

### Frame 5: Final Position (Direct Camera)
```
FRAME 5: lizzchar woman with purple streaks in dark hair, looking directly at camera, front facing, eyes meeting viewer, Arcane animation style, dramatic rim lighting, detailed facial features, cinematic IMAX composition, high quality, painterly
```

## Negative Prompt (Use for all frames)
```
blurry, low quality, distorted face, watermark, text, multiple heads, bad anatomy, motion blur, duplicate
```

## Workflow Instructions

1. **Load Workflow**: Open `lizzchar_flux_imax_storyboard.json` in ComfyUI
2. **For Each Frame**:
   - Change the positive prompt (node 4) to the corresponding frame prompt
   - Change the seed (node 7) to get variation if needed
   - Queue the prompt
   - Wait for generation (~30-60 seconds per frame)
   - Images save to `ComfyUI/output/lizzchar_imax_storyboard_*.png`

3. **Settings**:
   - Steps: 20 (good balance of quality/speed)
   - CFG Scale: 1.0 (FLUX works best at 1.0)
   - Sampler: euler
   - Scheduler: simple

## Animation Interpolation Tools

Once you have all 5 frames, use one of these tools to animate between them:

### Option 1: Frame Interpolation (Recommended)
- **FILM** (Frame Interpolation for Large Motion)
- **RIFE** (Real-Time Intermediate Flow Estimation)
- **Depth-Aware Video Frame Interpolation (DAIN)**

### Option 2: AI Animation Tools
- **Runway Gen-2/Gen-3** - Upload keyframes, generates smooth motion
- **Pika Labs** - Good for character animation
- **Kaiber** - Supports keyframe animation
- **TemporalKit** - Open source frame interpolation

### Option 3: Traditional Tools
- **After Effects** with Pixel Motion Blur
- **Blender** with interpolation plugins
- **DaVinci Resolve Fusion** - Speed warp interpolation

## Recommended Workflow

1. Generate all 5 storyboard frames (2048×1433)
2. Import into frame interpolation tool (e.g., RIFE or FILM)
3. Set target framerate (24fps recommended)
4. Generate interpolated frames between each keyframe
5. Export as video sequence

**Total frames needed**:
- 5 keyframes → 24fps @ 2 seconds = 48 total frames
- Interpolate: 9-10 frames between each keyframe pair

## Tips

- Keep lighting consistent across all frames
- Use the same seed for similar composition (change only for variety)
- Preview each frame before moving to next
- Maintain consistent background/environment
- The Arcane style should help maintain visual consistency
