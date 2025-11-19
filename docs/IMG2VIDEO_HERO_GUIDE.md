# 🎬 Image-to-Video Hero Character Guide

## Using Your Generated Image as Starting Point

You've created a great character in [arcane_panel_00007_.png](output/arcane_panel_00007_.png). Now let's bring them to life with motion!

---

## 🚀 Quick Start

### Step 1: Load the Workflow

1. Open ComfyUI: http://127.0.0.1:8188
2. Click **"Load"** button
3. Select: **arcane_img2video_hero.json**

### Step 2: Verify Settings

The workflow is pre-configured to use your hero image:

- **LoadImage node**: `arcane_panel_00007_.png` (already set)
- **Denoise strength**: 0.75 (good balance)
- **Steps**: 20
- **CFG**: 8.0
- **Seed**: 42
- **AnimateDiff model**: v3_sd15_mm.ckpt

### Step 3: Generate Your First Video

Click **"Queue Prompt"** - your hero will come to life!

**Expected time:** ~8-12 minutes for 16 frames
**Output:** `output/arcane_hero_00001.mp4`

---

## 🎨 How It Works

### Image-to-Video Pipeline

```
Your Image (arcane_panel_00007_.png)
    ↓
VAEEncode (converts to latent space)
    ↓
AnimateDiff (adds motion)
    ↓
KSampler (denoise: 0.75 = amount of change)
    ↓
VAEDecode (converts back to pixels)
    ↓
Video Export (MP4, 24fps)
```

### Key Parameter: Denoise Strength

This controls how much your character can change:

- **0.5-0.6**: Minimal change, character stays very similar
  - Use for: Subtle movements (breathing, hair flow, cloth movement)
  - Character consistency: HIGH

- **0.75**: Good balance (DEFAULT)
  - Use for: Normal actions (turning head, shifting weight, gestures)
  - Character consistency: MEDIUM-HIGH

- **0.8-0.9**: More creative motion
  - Use for: Walking, reaching, dynamic actions
  - Character consistency: MEDIUM

- **1.0**: Maximum change
  - Use for: Complex actions, major pose changes
  - Character consistency: LOW (may drift from original)

---

## 🎬 Motion Prompts

### Current Prompt (in workflow):
```
arcane style, character in motion, smooth camera movement,
cinematic animation, painterly motion, dramatic lighting,
ODESZA aesthetic
```

### Recommended Motion Prompts:

**Subtle Motion (denoise 0.5-0.6):**
```
arcane style, character standing, gentle breathing,
hair flowing in wind, cloth movement, ambient lighting shifts
```

**Character Movement (denoise 0.75):**
```
arcane style, character turning head slowly,
looking around, subtle body movement, smooth motion
```

**Dynamic Action (denoise 0.8-0.9):**
```
arcane style, character walking forward confidently,
arm reaching out, smooth character animation
```

**Camera Movement (denoise 0.6-0.7):**
```
arcane style, character standing, camera slowly pushing in,
cinematic movement, dramatic reveal
```

**Combination (denoise 0.75-0.85):**
```
arcane style, character turning and reaching toward viewer,
camera orbiting around character, dynamic lighting changes
```

---

## ⚙️ Adjusting Settings

### For Different Lengths:

In the **KSampler** node, the latent comes from **VAEEncode** which creates a single latent from your image. To make longer videos, you need to change the workflow:

**Current setup**: Single image → Single latent → 16 frames of that latent animated

**For longer sequences**, you'd need to modify the workflow to use a different approach:
- Use AnimateDiff's context options for longer sequences
- Or generate multiple 16-frame clips and combine them

**Recommended approach**: Keep 16-frame clips, generate multiple variations, combine in video editor

### For Higher Resolution:

Your source image is likely at IMAX resolution (4096×2156). The workflow will:
1. Encode at that resolution
2. Process in latent space
3. Decode back to original resolution

**Note**: Higher resolution = much longer generation time
- 768×404: ~8-12 minutes
- 1024×538: ~20-25 minutes
- 4096×2156: ~60-90 minutes per 16-frame clip

**Recommendation**: Generate at 768×404 first, test motion, then upscale

### For More Motion Variation:

Change the **seed** in KSampler:
- Seed 42: Version A
- Seed 45: Version B (slightly different motion)
- Seed 48: Version C
- etc.

Generate 3-5 versions, pick the one with best motion!

---

## 🎯 Workflow Strategies

### Strategy 1: Multiple Motion Clips

Generate several 16-frame clips with different motions:

1. **Clip 1**: Character idle (denoise 0.6)
2. **Clip 2**: Character looks left (denoise 0.7)
3. **Clip 3**: Character looks right (denoise 0.7)
4. **Clip 4**: Character steps forward (denoise 0.85)

Combine in video editor for complete sequence!

### Strategy 2: Camera Movements

Keep character mostly still, move camera:

1. **Clip 1**: "camera pushing in slowly"
2. **Clip 2**: "camera orbiting right around character"
3. **Clip 3**: "camera pulling back revealing environment"

Lower denoise (0.6-0.7) keeps character consistent!

### Strategy 3: Loop Creation

Generate seamless loops:

1. Use denoise 0.5-0.6 for minimal change
2. Generate 24 frames for 1-second loop
3. Add prompt: "smooth looping motion, cyclical movement"
4. Use for ambient background video

---

## 🎨 Using Different Source Images

You have two great images to work with:

### [arcane_panel_00007_.png](output/arcane_panel_00007_.png) (Current)
This is your HERO character. Use this for:
- Main character animations
- Hero shots
- Key dramatic moments

### [arcane_panel_00008_.png](output/arcane_panel_00008_.png)
Your other great image! To use it:
1. Open the workflow in ComfyUI
2. Click the **LoadImage** node
3. Change from `arcane_panel_00007_.png` to `arcane_panel_00008_.png`
4. Generate!

---

## 📊 Generation Time Estimates

**Per 16-frame sequence at source resolution:**

| Resolution | Time per clip | Recommended |
|------------|---------------|-------------|
| 768×404 | ~8-12 min | ✅ YES (test first) |
| 1024×538 | ~20-25 min | ⚠️ If you need better quality |
| 2048×1078 | ~40-50 min | ⚠️ Only for final versions |
| 4096×2156 | ~60-90 min | ❌ Too slow, upscale instead |

**Recommendation**:
1. Generate all motion tests at 768×404
2. Pick the best ones
3. Re-generate winners at higher resolution OR upscale with video upscaler

---

## 💡 Pro Tips

### Maintaining Character Consistency:

1. **Keep denoise ≤ 0.75** for recognizable character
2. **Use same seed** across related clips
3. **Keep prompts consistent** (always include "arcane style")
4. **Shorter clips = better consistency** (16 frames is good)

### Getting Smooth Motion:

1. **Lower CFG (7.0-8.0)** = smoother motion
2. **Add motion keywords**: "smooth", "fluid", "gentle"
3. **Use euler_a sampler** for faster, smoother results
4. **Generate multiple versions** and pick smoothest

### Creating a Full Sequence:

1. **Plan your shots**: Idle → Look → Turn → Walk → Action
2. **Generate each shot separately** (16 frames each)
3. **Keep same denoise within shot type**:
   - Subtle shots: 0.6
   - Normal shots: 0.75
   - Action shots: 0.85
4. **Combine in video editor** (DaVinci Resolve is free!)

### Troubleshooting:

**Character looks different:**
- Lower denoise (try 0.6 or 0.5)
- Check prompt includes "arcane style"
- Try different seed

**Motion is choppy:**
- Lower CFG (try 7.0)
- Change sampler to euler_a
- Add "smooth motion" to prompt

**Video is too short:**
- Generate multiple 16-frame clips
- Combine in video editor
- Or use frame interpolation (RIFE) to extend

---

## 🎬 Example Workflow

### Creating a "Hero Reveal" Sequence

**Shot 1: Idle (0-2 seconds)**
- Denoise: 0.6
- Prompt: "arcane style, character standing confidently, subtle breathing, dramatic lighting"
- Result: 16 frames of subtle idle motion

**Shot 2: Look (2-3 seconds)**
- Denoise: 0.7
- Prompt: "arcane style, character turning head slowly to look left, smooth motion"
- Result: 16 frames of head turn

**Shot 3: Recognition (3-5 seconds)**
- Denoise: 0.75
- Prompt: "arcane style, character's eyes widening, realization, dramatic moment"
- Result: 24 frames of emotional reaction

**Shot 4: Action (5-6 seconds)**
- Denoise: 0.85
- Prompt: "arcane style, character stepping forward determinedly, arm reaching out"
- Result: 16 frames of movement

**Total**: 72 frames = ~3 seconds at 24fps
**Generation time**: ~40-50 minutes
**Assembly**: Import to video editor, add ODESZA soundtrack, export!

---

## 🚀 Ready to Animate!

Your hero from [arcane_panel_00007_.png](output/arcane_panel_00007_.png) is ready to come to life!

**Quick checklist:**
1. ✅ ComfyUI is running
2. ✅ AnimateDiff models downloaded
3. ✅ Workflow created (arcane_img2video_hero.json)
4. ✅ Source image ready (arcane_panel_00007_.png)

**Next steps:**
1. Load the workflow
2. Click "Queue Prompt"
3. Wait ~10 minutes
4. Watch your hero move!

**The character you created + smooth motion = Epic animation!** 🎬✨
