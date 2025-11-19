# 🎬 Video Generation Guide - Arcane/ODESZA Animation

## 🎯 Your Goal
Create a 42-second animation from 7 panels in IMAX 4096×2156 resolution

## 📊 Three Approaches to Video

### ⭐ Option 1: AnimateDiff (INSTALLED - Best for Animation)
**What it does:** Creates smooth motion directly in ComfyUI
**Pros:** Native integration, good quality, ControlNet compatible
**Cons:** Requires AnimateDiff motion model download (~1.8GB)

### ⭐ Option 2: Frame Interpolation (Recommended for Your Project)
**What it does:** Generate keyframes → Interpolate between them
**Pros:** High quality, IMAX resolution support, fastest workflow
**Cons:** Requires external tool (RIFE or FILM)

### Option 3: SVD (Stable Video Diffusion)
**What it does:** Text/image to video generation
**Pros:** Latest tech, impressive results
**Cons:** Max 1024×576 resolution, slow for IMAX

---

## 🚀 RECOMMENDED WORKFLOW: Frame Interpolation

This is the best approach for your IMAX Arcane project.

### Phase 1: Generate Keyframes (ComfyUI)

**For each of 7 panels:**

1. **Generate 3-5 keyframe variations per panel**
   - Panel 1: 5 keyframes (6 seconds = ~144 frames)
   - Panel 2: 5 keyframes (6 seconds = ~144 frames)
   - ...and so on

2. **Settings per keyframe:**
   ```
   Resolution: 4096×2156
   Seed: Change slightly for motion (42, 45, 48, 51, 54)
   Same prompt, vary slightly for motion cues
   ```

3. **Total images to generate:**
   - 7 panels × 5 keyframes = **35 images**
   - At 2.5 min/image = **~87 minutes total**

### Phase 2: Frame Interpolation (RIFE)

**Install RIFE for frame interpolation:**

1. Download RIFE: https://github.com/hzwer/Practical-RIFE
2. Or use online: https://github.com/nihui/rife-ncnn-vulkan (faster, standalone)

**Interpolate between keyframes:**
```
Input: 5 keyframes per panel
Output: 144 frames per panel (24fps × 6 seconds)
RIFE multiplier: ~28x interpolation
```

**Expected time:**
- ~5-10 minutes per panel
- Total: ~1 hour for all interpolation

### Phase 3: Compile in Video Editor

Use DaVinci Resolve or Premiere Pro:
1. Import all 1008 frames (7 panels × 144 frames)
2. Set timeline to 24fps
3. Add ODESZA soundtrack
4. Color grade for consistency
5. Export as 4K video

---

## 🎨 Option 1 Setup: AnimateDiff (Native ComfyUI)

### Step 1: Download AnimateDiff Motion Model

You need to download the motion model:

```bash
# Navigate to models folder
cd C:\Users\User\Desktop\ComfyUI_lizz\models

# Create animatediff folder if not exists
mkdir animatediff

# Download motion module (choose one):
```

**Motion Models to download:**

1. **v3_sd15_mm.ckpt** (Recommended - 1.8GB)
   - Link: https://huggingface.co/guoyww/animatediff/blob/main/v3_sd15_mm.ckpt
   - Location: `models/animatediff/`

2. **v2_lora_PanRight.ckpt** (Optional - for camera pans)
   - Link: https://huggingface.co/guoyww/animatediff/blob/main/v2_lora_PanRight.ckpt
   - Location: `models/loras/`

### Step 2: Restart ComfyUI

After downloading models, restart ComfyUI to load AnimateDiff nodes.

### Step 3: AnimateDiff Workflow

**New nodes will appear:**
- AnimateDiff Loader
- Video Combine
- Context Options
- Sample Settings

**Basic AnimateDiff workflow:**
```
CheckpointLoader → AnimateDiffLoader → KSampler → VAEDecode → VideoCombi ne
```

**Settings for your panels:**
```
Frames: 24-48 per panel (1-2 seconds)
Resolution: Start at 768×404 (scaled from IMAX ratio)
Context: 16 frames
FPS: 24
```

**Note:** AnimateDiff at full IMAX 4096×2156 will be VERY slow. Recommended:
1. Generate at 768×404 (IMAX ratio maintained)
2. Upscale to 4096×2156 afterwards

---

## 📋 Detailed Workflow Comparison

| Method | Quality | Speed | IMAX Support | Complexity |
|--------|---------|-------|--------------|------------|
| Frame Interpolation (RIFE) | ⭐⭐⭐⭐⭐ | Fast | ✅ Yes | Easy |
| AnimateDiff | ⭐⭐⭐⭐ | Slow | ⚠️ Lower res | Medium |
| SVD | ⭐⭐⭐⭐ | Very Slow | ❌ No | Hard |

---

## 🎯 RECOMMENDED STEPS FOR YOUR PROJECT

### Week 1: Keyframe Generation

**Day 1-2: Generate all 35 keyframes**
```bash
# Using optimized workflow
# 7 panels × 5 keyframes = 35 images
# Time: ~90 minutes
```

**Per panel keyframe strategy:**
```
Panel 1: Cityscape
- Keyframe 1: Wide shot, dusk lighting
- Keyframe 2: Zoom in slightly, lights brighten
- Keyframe 3: Focus shift to specific building
- Keyframe 4: Neon colors intensify
- Keyframe 5: Transition setup for Panel 2

Seeds: 42, 45, 48, 51, 54
```

### Week 2: Interpolation & Assembly

**Day 3: Install RIFE**
```bash
# Option A: RIFE GUI (easiest)
Download: https://github.com/nihui/rife-ncnn-vulkan/releases

# Option B: Flowframes (Windows GUI)
Download: https://nmkd.itch.io/flowframes
```

**Day 4-5: Interpolate all panels**
```
Input: 5 keyframes per panel
Settings:
- FPS output: 24
- Target frames: 144 per panel
- Quality: High
- Model: RIFE 4.6

Time per panel: ~10 minutes
Total: ~70 minutes
```

**Day 6-7: Video editing**
```
1. Import frames to DaVinci Resolve
2. Timeline: 24fps, 4096×2156
3. Add soundtrack (ODESZA - 42 seconds)
4. Color grade for consistency
5. Add sound effects
6. Export as ProRes 4K or H.265
```

---

## 💻 RIFE Installation (Recommended)

### Option 1: Flowframes (GUI - Easiest)

1. Download: https://nmkd.itch.io/flowframes
2. Install and launch
3. Import your 5 keyframes per panel
4. Set:
   - FPS: 24
   - Interpolation factor: Auto (will calculate)
   - AI Model: RIFE 4.6
5. Click "Start"

### Option 2: RIFE-ncnn-vulkan (CLI - Fastest)

```bash
# Download from releases
https://github.com/nihui/rife-ncnn-vulkan/releases

# Usage:
rife-ncnn-vulkan.exe -i input_folder -o output_folder -n 144 -f 24
```

### Option 3: ComfyUI Video Helper (Integrated)

**VideoHelperSuite is already installed!**

After restart, you'll have nodes:
- Load Images
- VHS Video Combine
- Frame Interpolation nodes

This lets you do everything in ComfyUI!

---

## 🎬 Example Timeline Breakdown

**42-second animation at 24fps = 1008 frames total**

| Panel | Duration | Frames | Keyframes | Interpolation |
|-------|----------|--------|-----------|---------------|
| 1: Cityscape | 6s | 144 | 5 | 28x |
| 2: Artist Window | 6s | 144 | 5 | 28x |
| 3: Glitch Graffiti | 6s | 144 | 5 | 28x |
| 4: Alley Chase | 6s | 144 | 5 | 28x |
| 5: Memory Mural | 6s | 144 | 5 | 28x |
| 6: Identity Merge | 6s | 144 | 5 | 28x |
| 7: Final Fade | 6s | 144 | 5 | 28x |
| **Total** | **42s** | **1008** | **35** | **973 interpolated** |

---

## 🚀 Quick Start: Frame Interpolation Method

### Step 1: Generate Keyframes (Today)

Use your current ComfyUI workflow:
1. Load `arcane_imax_optimized.json`
2. Generate 5 variations per panel
3. Change seed: 42 → 45 → 48 → 51 → 54
4. Slightly vary prompts for motion cues

### Step 2: Install Flowframes (Tomorrow)

1. Download Flowframes
2. Import Panel 1 keyframes (5 images)
3. Generate 144 frames
4. Preview result

### Step 3: Scale Up (After testing)

1. Process all 7 panels
2. Combine in video editor
3. Add soundtrack
4. Export final video

---

## 💡 Pro Tips

### For Keyframe Generation:
- **Motion cues in prompts:** Add "camera slowly pushing in" or "gentle pan right"
- **Consistent seed progression:** 42, 45, 48, 51, 54 (gaps of 3)
- **Same LoRA/style strength:** Keep 0.7-0.8 across all
- **Generate extras:** Make 7 keyframes, pick best 5

### For Interpolation:
- **RIFE 4.6** is the latest and best
- **Don't over-interpolate:** 28-30x is the max for quality
- **GPU acceleration:** RIFE uses GPU, much faster than CPU
- **Batch process:** Do all panels overnight

### For Final Assembly:
- **Color grade in DaVinci Resolve:** Free and powerful
- **Match colors between panels:** Use color wheels
- **Add motion blur:** For smoother movement
- **Sound design:** Layer atmospheric sounds with ODESZA track

---

## 📦 What You Need to Download

### For AnimateDiff Method:
- [ ] v3_sd15_mm.ckpt (1.8GB) - AnimateDiff motion model
- [ ] Optional: LoRA motion modules

### For Frame Interpolation Method:
- [ ] Flowframes GUI (~500MB)
- [ ] OR RIFE-ncnn-vulkan (~50MB)

### For Video Editing:
- [ ] DaVinci Resolve (Free)
- [ ] OR Adobe Premiere Pro

---

## ⏱️ Time Estimates

### Method 1: Frame Interpolation (Recommended)
- Keyframe generation: 90 minutes
- RIFE interpolation: 70 minutes
- Video editing: 3-4 hours
- **Total: 6-7 hours**

### Method 2: AnimateDiff
- Setup and model download: 30 minutes
- Generate 7 panel videos @ 768×404: 4-5 hours
- Upscale to IMAX: 2-3 hours
- Video editing: 2-3 hours
- **Total: 9-12 hours**

---

## 🎬 Ready to Start!

**Recommended next steps:**

1. **Today:** Generate all 35 keyframes using current workflow (~2 hours)
2. **Tomorrow:** Install Flowframes and test Panel 1 interpolation
3. **This week:** Process all panels and assemble video

You already have:
- ✅ ComfyUI optimized for IMAX
- ✅ AnimateDiff extension installed
- ✅ VideoHelperSuite installed
- ✅ All models downloaded

**Just need:** Restart ComfyUI to load new video nodes!

Want me to create an AnimateDiff workflow JSON, or continue with the frame interpolation approach?
