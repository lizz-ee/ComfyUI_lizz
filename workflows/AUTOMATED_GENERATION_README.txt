================================================================================
AUTOMATED CLIFF FALL GENERATION - PYTHON SCRIPT
================================================================================

🎯 GOAL: Fully automated generation of all 33 prompts × 4 seeds = 132 images
🐍 SCRIPT: generate_cliff_fall.py
⚡ NO MANUAL WORK: Just run the script and walk away!

================================================================================
WHAT IT DOES
================================================================================

1. ✅ Reads all 33 prompts from ALL_PROMPTS_cliff_fall.txt
2. ✅ Loops through all 4 seeds (51, 42, 50, 43)
3. ✅ Sends each job to ComfyUI API automatically
4. ✅ Waits for each to complete before moving to next
5. ✅ Tracks progress and shows status
6. ✅ Saves all images with proper naming

TOTAL: 132 images generated automatically! 🎨

================================================================================
HOW TO USE
================================================================================

STEP 1: Make sure ComfyUI is running
  - Open ComfyUI at http://127.0.0.1:8188
  - Keep it running in background

STEP 2: Open terminal/command prompt
  - Navigate to: D:\ComfyUI_lizz\workflows\

STEP 3: Run the script

  🐌 SINGLE MODE (Safer, recommended for RTX 3090):
  python generate_cliff_fall.py --single

  ⚡ PARALLEL MODE (Faster, needs more VRAM):
  python generate_cliff_fall.py --parallel


STEP 4: Walk away!
  - Script runs automatically
  - Shows progress for each frame
  - Estimated time: 30-60 minutes total

================================================================================
MODES EXPLAINED
================================================================================

🐌 SINGLE MODE (--single or default):
  - Generates ONE seed at a time
  - Frame 01 Seed 51 → wait → Frame 01 Seed 42 → wait → etc.
  - Safer for VRAM (each seed ~30-60 seconds)
  - Total time: ~60 minutes for all 132 images

⚡ PARALLEL MODE (--parallel):
  - Generates ALL 4 seeds simultaneously
  - Frame 01 (all 4 seeds at once) → wait → Frame 02 (all 4 seeds) → etc.
  - Faster but needs more VRAM
  - Total time: ~30 minutes for all 132 images

Use SINGLE mode if you're unsure or get VRAM errors!

================================================================================
EXAMPLE OUTPUT
================================================================================

$ python generate_cliff_fall.py --single

╔════════════════════════════════════════════════════════════════════════╗
║         CLIFF FALL SEQUENCE - AUTOMATED BATCH GENERATOR               ║
╚════════════════════════════════════════════════════════════════════════╝

🐌 Running in SINGLE mode (one seed at a time)

📖 Reading prompts...
✅ Found 33 prompts
🎲 Seeds: [51, 42, 50, 43]
📊 Total generations: 132

🔧 Loading workflow template...
✅ Loaded: cliff_fall_ipadapter_multiseed.json

🔌 Testing ComfyUI connection...
✅ Connected to ComfyUI

🚀 Starting generation...
================================================================================

[1/33] Frame_01_START - Pure Landscape
  🎲 Seed 51... ✅
  🎲 Seed 42... ✅
  🎲 Seed 50... ✅
  🎲 Seed 43... ✅

[2/33] Frame_01_END - Cliff Edge Revealed
  🎲 Seed 51... ✅
  🎲 Seed 42... ✅
  ...

================================================================================
🎉 GENERATION COMPLETE!
================================================================================
✅ Successfully generated: 132
❌ Failed: 0
⏱️  Total time: 45.2 minutes
📊 Average per image: 20.5 seconds

📁 Check output in: D:\ComfyUI_lizz\output\

================================================================================
UPDATING PROMPTS OR SEEDS
================================================================================

Want to regenerate with changes?

TO CHANGE PROMPTS:
1. Edit: prompts/ALL_PROMPTS_cliff_fall.txt
2. Modify any frame prompts you want
3. Run script again - it reads the file fresh each time!

TO CHANGE SEEDS:
1. Edit: generate_cliff_fall.py
2. Find line: SEEDS = [51, 42, 50, 43]
3. Change to: SEEDS = [51, 42, 100, 200]  # or whatever seeds you want
4. Run script again!

TO CHANGE SETTINGS:
1. Edit: generate_cliff_fall.py
2. Find the SETTINGS dictionary:
   SETTINGS = {
       "steps": 20,           # Change to 25 for more detail
       "ipadapter_weight": 0.45,  # Change to 0.5 for stronger scene lock
       ...
   }
3. Run script again!

================================================================================
TROUBLESHOOTING
================================================================================

❌ "Cannot connect to ComfyUI"
  → Make sure ComfyUI is running at http://127.0.0.1:8188
  → Check the URL in your browser first

❌ "Module not found: requests"
  → Install: pip install requests

❌ VRAM errors / Out of memory
  → Use --single mode instead of --parallel
  → Close other GPU-heavy apps

❌ Images not generating
  → Check ComfyUI console for errors
  → Verify cliff_cleanplate.png exists in D:\ComfyUI_lizz\input\
  → Check that lizzchar_lora.safetensors is in models/loras/

❌ Script freezes / timeout
  → Normal for slow generations
  → Default timeout is 120 seconds per seed
  → Script will mark as failed and continue

================================================================================
OUTPUT FILES
================================================================================

Files are saved to: D:\ComfyUI_lizz\output\

Naming format:
  cliff_Frame_01_START_seed51_00001_.png
  cliff_Frame_01_START_seed42_00002_.png
  cliff_Frame_01_START_seed50_00003_.png
  cliff_Frame_01_START_seed43_00004_.png
  ...

Each frame gets 4 versions (one per seed)!

================================================================================
ADVANCED: BATCH REGENERATE SPECIFIC FRAMES
================================================================================

Want to regenerate just a few frames?

1. Edit generate_cliff_fall.py

2. Find the generate_all() function

3. Add this filter after parsing prompts:

   # Only generate specific frames
   prompts = [p for p in prompts if p['id'] in ['Frame_05_START', 'Frame_05_END']]

4. Run script - it will only generate those frames!

================================================================================

READY TO AUTOMATE! 🚀

1. Make sure ComfyUI is running
2. Run: python generate_cliff_fall.py --single
3. Go get coffee ☕
4. Come back to 132 beautiful images! 🎨

NO MISTAKES, JUST HAPPY LITTLE AUTOMATED BATCHES!

================================================================================
