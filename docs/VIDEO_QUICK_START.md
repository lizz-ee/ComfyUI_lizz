# 🎬 Video Generation - Quick Start

## ✅ Everything is Ready!

**ComfyUI is running at:** http://127.0.0.1:8188

**Extensions loaded:**
- ✅ AnimateDiff-Evolved (video motion)
- ✅ VideoHelperSuite (video export)
- ✅ Motion model: v3_sd15_mm.ckpt (1.6GB)

---

## 🚀 Generate Your First Video Sequence

### Step 1: Load the Video Workflow

1. Open ComfyUI: http://127.0.0.1:8188
2. Click **"Load"** button
3. Select: **arcane_video_animatediff.json**

### Step 2: Configure Settings

**Pre-configured for you:**
- Resolution: 768×404 (IMAX ratio, optimized for speed)
- Frames: 16 (2/3 second @ 24fps)
- Motion Model: v3_sd15_mm.ckpt
- Sampler: euler_a (fast)
- Steps: 25
- Seed: 42

### Step 3: Generate!

Click **"Queue Prompt"** - your first video sequence will generate!

**Expected time:** ~8-12 minutes for 16 frames

**Output:**
- Location: `output/arcane_video_00001.mp4`
- Format: MP4 (H.264)
- FPS: 24
- Ready to view!

---

## 🎨 Workflow for All 7 Panels

**For each panel:**

1. **Update the LoadImage node:**
   - Panel 1: `panel1_scribble_cityscape.png`
   - Panel 2: `panel2_openpose_standing.png`
   - Panel 3: `panel3_openpose_reaching.png` (default)
   - Panel 4: `panel4_openpose_running.png`
   - Panel 5: `panel5_openpose_hand.png`
   - Panel 6: `panel6_scribble_city_face.png`
   - Panel 7: `panel7_openpose_face.png`

2. **Update the ControlNet:**
   - OpenPose panels (2,3,4,5,7): `control_v11p_sd15_openpose.pth`
   - Scribble panels (1,6): `control_v11p_sd15_scribble.pth`

3. **Update the prompt** (from PROMPTS.txt)

4. **Keep seed at 42** for consistency

5. **Generate!**

---

## ⚙️ Adjusting Settings

### For Longer Sequences:

In **EmptyLatentImage** node, change batch size:
- 16 frames = ~0.67 seconds
- 24 frames = 1 second
- 32 frames = ~1.3 seconds
- 48 frames = 2 seconds
- 144 frames = 6 seconds (SLOW but makes full panel)

### For Different Resolutions:

**Current (recommended):** 768×404
- Fast generation (~12 min for 16 frames)
- Good quality
- IMAX 1.90:1 ratio maintained

**Higher res:** 1024×538
- Slower (~25 min for 16 frames)
- Better quality
- Still maintains IMAX ratio

**IMAX full res:** 4096×2156
- VERY slow (~2-3 hours per 16 frames)
- Not recommended for AnimateDiff
- Better to generate low res → upscale

### For Better Quality:

- Increase steps: 25 → 30-35
- Increase CFG: 8.0 → 9.0-10.0
- Use different sampler: try `dpmpp_2m`

### For Faster Generation:

- Reduce steps: 25 → 20
- Reduce frames: 16 → 12
- Lower CFG: 8.0 → 7.0

---

## 📊 Generation Time Estimates

**Per 16-frame sequence at 768×404:**
- Steps 20: ~8 minutes
- Steps 25: ~10 minutes (current)
- Steps 30: ~12 minutes

**All 7 panels (16 frames each):**
- Total: ~70-90 minutes

**All 7 panels (48 frames each for 2 seconds):**
- Total: ~3-4 hours

**For full 6-second panels (144 frames each):**
- Per panel: ~45-60 minutes
- Total: ~6-7 hours

---

## 🎬 Combining Sequences into Full Video

### Option 1: Video Editor (Recommended)

1. **Generate all 7 panel sequences** (16-48 frames each)
2. **Import to DaVinci Resolve** (free) or Premiere Pro
3. **Timeline settings:**
   - Resolution: 4096×2156
   - FPS: 24
   - Duration: 42 seconds
4. **Arrange clips:**
   - Panel 1: 0-6s
   - Panel 2: 6-12s
   - Panel 3: 12-18s
   - etc.
5. **Add transitions** between panels (optional)
6. **Add ODESZA soundtrack**
7. **Color grade** for consistency
8. **Upscale** (if needed) using video upscaler
9. **Export as 4K**

### Option 2: Frame Interpolation

If your 16-frame sequences are too short:

1. **Export frames** from each video
2. **Use RIFE/Flowframes** to interpolate more frames
3. **Example:** 16 frames → 144 frames (24x interpolation)
4. **Recombine** in video editor

---

## 💡 Pro Tips

### Motion Tips:
- **Add motion keywords** to prompts:
  - "camera slowly pushing in"
  - "gentle pan right"
  - "camera orbiting around subject"
  - "slow zoom out"

- **For smooth motion:** Keep seed consistent
- **For varied motion:** Change seed between sequences

### Quality Tips:
- **Generate 2-3 variations** per panel (different seeds)
- **Pick the best** with smoothest motion
- **Increase context_length** for smoother longer sequences

### VRAM Tips:
- **16 frames at 768×404:** Uses ~12-15GB VRAM
- **48 frames at 768×404:** Uses ~18-20GB VRAM
- **Monitor** your Task Manager GPU usage

### Speed Optimization:
- **Batch panels overnight:** Queue all 7 panels
- **Use scheduler:** Generate while you sleep
- **Start with short sequences:** Test with 12-16 frames first

---

## 🎯 Recommended Workflow

### Day 1: Test & Learn
1. Generate Panel 3 (16 frames) - ~10 min
2. Watch the result
3. Adjust settings if needed
4. Generate Panel 3 again with tweaks

### Day 2: Generate All Panels
1. Panel 1 (16 frames) - ~10 min
2. Panel 2 (16 frames) - ~10 min
3. Panel 3 (16 frames) - ~10 min
4. Panel 4 (16 frames) - ~10 min
5. Panel 5 (16 frames) - ~10 min
6. Panel 6 (16 frames) - ~10 min
7. Panel 7 (16 frames) - ~10 min

**Total: ~90 minutes**

### Day 3: Extend & Compile
1. Extend sequences if needed (interpolation)
2. Import to video editor
3. Add soundtrack
4. Color grade
5. Export final video

---

## 📁 Output Files

**Videos saved to:** `C:\Users\User\Desktop\ComfyUI_lizz\output\`

**File naming:**
- arcane_video_00001.mp4 (Panel 1)
- arcane_video_00002.mp4 (Panel 2)
- etc.

**Format:** MP4 (H.264), 24fps

---

## 🚀 You're Ready!

1. Open http://127.0.0.1:8188
2. Load **arcane_video_animatediff.json**
3. Click **Queue Prompt**
4. Watch your first Arcane video sequence generate!

**The style you love + smooth motion = Awesome video!** 🎬✨
