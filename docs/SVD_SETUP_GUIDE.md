# 🎬 Stable Video Diffusion - Image-to-Video Setup

## ✅ What's Installed

**Extension:** stability-ComfyUI-nodes
**Model:** svd_xt.safetensors (9.1GB)
**Location:** `models/checkpoints/svd_xt.safetensors`

---

## 🚀 Two Approaches Ready for You

### Option A: Keyframe Generation (RECOMMENDED)

**Best for controlled head turns and character animation**

**Workflow:** [arcane_keyframe_generator.json](arcane_keyframe_generator.json)

**How it works:**
1. Loads your hero image (arcane_panel_00007_.png)
2. Uses img2img with LOW ControlNet strength (0.3)
3. Generates variations with different head angles
4. You interpolate between keyframes using RIFE

**Steps to create head turn:**

1. **Generate Keyframe 1** (already have): Original image - head forward

2. **Generate Keyframe 2** (slight turn):
   - Load workflow: arcane_keyframe_generator.json
   - Prompt: "character looking slightly to the right, head turned 20 degrees"
   - Seed: 45
   - Generate → saves as keyframe_hero_00001.png

3. **Generate Keyframe 3** (medium turn):
   - Prompt: "character looking to the right, head turned right, three-quarter view"
   - Seed: 48
   - Generate → saves as keyframe_hero_00002.png

4. **Generate Keyframe 4** (full profile):
   - Prompt: "character in profile, head turned right, face in profile view"
   - Seed: 51
   - Denoise: 0.8
   - Generate → saves as keyframe_hero_00003.png

5. **Interpolate with RIFE:**
   - Download Flowframes: https://nmkd.itch.io/flowframes
   - Import your 4 keyframes
   - Set output to 24 frames
   - Generate smooth 1-second head turn!

**Why this works:**
- Low ControlNet (0.3) keeps body, allows head rotation
- Denoise 0.75-0.8 allows significant changes
- Character stays consistent across keyframes
- RIFE creates smooth interpolation

---

### Option B: Stable Video Diffusion (Experimental)

**True AI image-to-video generation**

**Status:** Model downloaded, needs workflow setup

**Pros:**
- Real AI-generated motion from single image
- No keyframes needed
- Smooth natural motion

**Cons:**
- Limited control over motion direction
- Max resolution 1024×576 (lower than your image)
- Slower generation (~5-10 minutes)
- Results can be unpredictable

**To use SVD:**
1. Restart ComfyUI (to load new extension)
2. Look for "SVD" nodes in the node browser
3. Create workflow: LoadImage → SVD_img2vid → VideoCombine

**Note:** SVD doesn't support text prompts for motion direction, so you can't specifically request "turn head right" - it generates automatic motion.

---

## 📊 Comparison

| Method | Control | Quality | Speed | Resolution |
|--------|---------|---------|-------|------------|
| **Keyframe + RIFE** | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Fast | Any |
| **SVD** | ⭐⭐ Low | ⭐⭐⭐⭐ Good | ⭐⭐⭐ Medium | 1024×576 max |
| **AnimateDiff img2img** | ⭐ Very Low | ⭐⭐ Poor | ⭐⭐⭐⭐ Fast | Any |

---

## 🎯 RECOMMENDED WORKFLOW

**For your head turn animation, use Option A:**

### Quick 15-Minute Process:

**Phase 1: Generate Keyframes (10 min)**
1. Open ComfyUI
2. Load arcane_keyframe_generator.json
3. Generate 3 keyframes with different prompts (3-4 min each)

**Phase 2: Interpolate (5 min)**
1. Download Flowframes (if not installed)
2. Import 4 images (original + 3 keyframes)
3. Generate 24-frame sequence
4. Export as MP4

**Result:** Smooth head turn animation with your hero character!

---

## 🔧 Keyframe Generator Settings

**Current configuration:**

```json
ControlNet Strength: 0.3 (low - allows head rotation)
Denoise: 0.75 (allows significant change)
Seed: 45 (change for each keyframe: 45, 48, 51)
Steps: 20
CFG: 7.5
Sampler: euler
```

**To adjust:**
- **More head rotation**: Lower ControlNet to 0.2 or 0.1
- **Keep character identical**: Lower denoise to 0.6-0.7
- **More dramatic changes**: Increase denoise to 0.8-0.9
- **Different variations**: Change seed

---

## 📁 Output Files

**Keyframes:** `output/keyframe_hero_00001.png`, `00002.png`, etc.
**Final video:** Create with Flowframes or video editor

---

## 🚀 Next Steps

**To create your head turn video:**

1. **Load the keyframe generator workflow**
   ```
   ComfyUI → Load → arcane_keyframe_generator.json
   ```

2. **Generate 3 new angles** (change prompt for each)

3. **Download Flowframes** if needed:
   ```
   https://nmkd.itch.io/flowframes
   ```

4. **Interpolate and export!**

**Total time:** ~15 minutes for smooth head turn animation

---

## 💡 Pro Tips

**For best keyframe consistency:**
- Keep same seed family (42, 45, 48, 51)
- Don't change negative prompt
- Keep ControlNet strength consistent (0.3)
- Gradual prompt changes (20° → 45° → 70°)

**For smooth interpolation:**
- RIFE 4.6 model (latest)
- 24-30 fps output
- 6-8 frames between keyframes = smooth motion

**For character consistency:**
- Always include "arcane style" in prompt
- Keep lighting/atmosphere keywords same
- Don't change CFG or steps between keyframes

---

## 🎬 Ready to Go!

Everything is set up for Option A (keyframe generation). This is the best approach for controlled head turns.

If you want to experiment with SVD later, restart ComfyUI first to load the new extension.

**Start with:** Load arcane_keyframe_generator.json and generate your first keyframe!
