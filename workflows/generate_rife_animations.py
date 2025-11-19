#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate RIFE-interpolated Animations from Cliff Fall Frames
Processes all cleanplate/variant/seed combinations and creates smooth 30fps videos
Uses RIFE 4.7 for 4x frame interpolation (33 frames -> 132 frames @ 30fps)
"""

import sys
import io
# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import json
import requests
import time
import uuid
from pathlib import Path

# Configuration
COMFY_URL = "http://127.0.0.1:8188"
WORKFLOW_PATH = Path(__file__).parent / "cliff_fall_rife_animation.json"
OUTPUT_BASE = Path(r"D:\ComfyUI_lizz\output\fall")
CLEANPLATES = [1, 2, 3, 4, 5]
VARIANTS = ['original', 'enhanced']
SEEDS = [51, 42, 50, 43]

# RIFE Configuration
RIFE_MODEL = "rife47.pth"
RIFE_MULTIPLIER = 4  # 33 frames * 4 = 132 frames
FRAME_RATE = 30  # 132 frames @ 30fps = 4.4 seconds
VIDEO_CRF = 20  # Quality (lower = better, 18-23 is visually lossless)

def load_workflow():
    """Load the base workflow JSON."""
    with open(WORKFLOW_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_workflow_for_sequence(workflow, cleanplate_id, variant, seed):
    """Update workflow parameters for a specific sequence."""
    # Update input directory
    input_dir = OUTPUT_BASE / f"cleanplate_{cleanplate_id:02d}" / variant / f"Seed_{seed}" / "v001"
    workflow["1"]["inputs"]["directory"] = str(input_dir)

    # Update output filename
    output_prefix = f"cliff_fall_cp{cleanplate_id:02d}_{variant}_seed{seed}_rife"
    workflow["3"]["inputs"]["filename_prefix"] = output_prefix

    # Update RIFE settings
    workflow["2"]["inputs"]["ckpt_name"] = RIFE_MODEL
    workflow["2"]["inputs"]["multiplier"] = RIFE_MULTIPLIER

    # Update video settings
    workflow["3"]["inputs"]["frame_rate"] = FRAME_RATE
    workflow["3"]["inputs"]["crf"] = VIDEO_CRF

    return workflow

def queue_prompt(workflow):
    """Submit workflow to ComfyUI queue."""
    prompt_id = str(uuid.uuid4())
    payload = {
        "prompt": workflow,
        "client_id": prompt_id
    }

    response = requests.post(f"{COMFY_URL}/prompt", json=payload)

    if response.status_code == 200:
        return prompt_id
    else:
        raise Exception(f"Failed to queue prompt: {response.status_code} - {response.text}")

def check_queue_status():
    """Check current queue status."""
    response = requests.get(f"{COMFY_URL}/queue")
    if response.status_code == 200:
        data = response.json()
        queue_running = len(data.get("queue_running", []))
        queue_pending = len(data.get("queue_pending", []))
        return queue_running, queue_pending
    return 0, 0

def wait_for_completion(prompt_id, check_interval=5):
    """Wait for a specific prompt to complete."""
    print(f"   Waiting for completion (checking every {check_interval}s)...")

    while True:
        try:
            response = requests.get(f"{COMFY_URL}/history/{prompt_id}")
            if response.status_code == 200:
                history = response.json()
                if prompt_id in history:
                    # Prompt completed
                    result = history[prompt_id]
                    if "outputs" in result:
                        return True
                    else:
                        print(f"   WARNING: Prompt completed but no outputs found")
                        return False
        except Exception as e:
            print(f"   Error checking status: {e}")

        time.sleep(check_interval)

def generate_animation(cleanplate_id, variant, seed, sequence_num, total_sequences):
    """Generate a single RIFE-interpolated animation."""
    print()
    print("=" * 80)
    print(f" SEQUENCE {sequence_num}/{total_sequences}")
    print(f" Cleanplate: {cleanplate_id:02d} | Variant: {variant.upper()} | Seed: {seed}")
    print("=" * 80)
    print()

    # Load and update workflow
    print(f" Loading workflow template...")
    workflow = load_workflow()
    workflow = update_workflow_for_sequence(workflow, cleanplate_id, variant, seed)

    # Queue the workflow
    print(f" Submitting to ComfyUI...")
    try:
        prompt_id = queue_prompt(workflow)
        print(f" Queued with ID: {prompt_id}")
    except Exception as e:
        print(f" ERROR: Failed to queue workflow: {e}")
        return False

    # Wait for completion
    start_time = time.time()
    success = wait_for_completion(prompt_id)
    elapsed = time.time() - start_time

    if success:
        print()
        print(f" ✓ Animation completed in {elapsed/60:.1f} minutes")
        return True
    else:
        print()
        print(f" ✗ Animation failed after {elapsed/60:.1f} minutes")
        return False

def main():
    """Generate all RIFE animations."""
    print()
    print("=" * 80)
    print("  CLIFF FALL - RIFE ANIMATION GENERATION")
    print("=" * 80)
    print()
    print(" Configuration:")
    print(f"   Cleanplates: {len(CLEANPLATES)}")
    print(f"   Variants: {len(VARIANTS)} (original, enhanced)")
    print(f"   Seeds per variant: {len(SEEDS)}")
    print(f"   Total sequences: {len(CLEANPLATES) * len(VARIANTS) * len(SEEDS)}")
    print()
    print(" RIFE Settings:")
    print(f"   Model: {RIFE_MODEL}")
    print(f"   Interpolation: {RIFE_MULTIPLIER}x (33 -> 132 frames)")
    print(f"   Output FPS: {FRAME_RATE}")
    print(f"   Video duration: ~{(33 * RIFE_MULTIPLIER) / FRAME_RATE:.1f} seconds per video")
    print(f"   Video quality (CRF): {VIDEO_CRF}")
    print()

    # Check if ComfyUI is running
    print(" Checking ComfyUI connection...")
    try:
        response = requests.get(f"{COMFY_URL}/queue")
        if response.status_code != 200:
            print(f" ERROR: ComfyUI not responding at {COMFY_URL}")
            print(" Please start ComfyUI and try again.")
            return
        print(f" ✓ Connected to ComfyUI at {COMFY_URL}")
    except Exception as e:
        print(f" ERROR: Cannot connect to ComfyUI: {e}")
        print(" Please start ComfyUI and try again.")
        return

    print()
    print(" Starting animation generation in 3 seconds...")
    time.sleep(3)

    overall_start = time.time()
    sequence_num = 0
    total_sequences = len(CLEANPLATES) * len(VARIANTS) * len(SEEDS)
    completed = 0
    failed = 0

    # Loop through all combinations
    for cleanplate_id in CLEANPLATES:
        for variant in VARIANTS:
            for seed in SEEDS:
                sequence_num += 1

                success = generate_animation(cleanplate_id, variant, seed, sequence_num, total_sequences)

                if success:
                    completed += 1
                else:
                    failed += 1
                    response = input("\n Continue with next sequence? (y/n): ")
                    if response.lower() != 'y':
                        break

            if failed and response.lower() != 'y':
                break

        if failed and response.lower() != 'y':
            break

    # Final summary
    overall_elapsed = time.time() - overall_start

    print()
    print("=" * 80)
    print("  ANIMATION GENERATION COMPLETE!")
    print("=" * 80)
    print(f" Completed: {completed}/{total_sequences}")
    print(f" Failed: {failed}")
    print(f" Total time: {overall_elapsed/3600:.2f} hours")
    print()
    print(f" Output location: {OUTPUT_BASE}")
    print(" Videos are saved in ComfyUI/output/ directory")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("  Animation generation interrupted by user")
        print()
