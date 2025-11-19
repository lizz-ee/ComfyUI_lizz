#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Runner for All Cleanplate Variants
Runs generate_cliff_fall.py for all 5 cleanplates × 2 variants = 10 batches
Total: 1,320 images (33 frames × 4 seeds × 5 cleanplates × 2 variants)
"""

import subprocess
import sys
from pathlib import Path
import time

# Configuration
CLEANPLATES = [1, 2, 3, 4, 5]
VARIANTS = ['original', 'enhanced']
SCRIPT_PATH = Path(__file__).parent / "generate_cliff_fall.py"

def update_script_config(cleanplate_id, variant):
    """Update the generate_cliff_fall.py configuration."""
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update CLEANPLATE_ID
    content = content.replace(
        f"CLEANPLATE_ID = {cleanplate_id - 1}  # Change to:",
        f"CLEANPLATE_ID = {cleanplate_id}  # Change to:"
    )
    # Handle initial case
    for i in range(1, 6):
        content = content.replace(
            f"CLEANPLATE_ID = {i}  # Change to:",
            f"CLEANPLATE_ID = {cleanplate_id}  # Change to:"
        )

    # Update ACTIVE_VARIANT
    other_variant = 'enhanced' if variant == 'original' else 'original'
    content = content.replace(
        f"ACTIVE_VARIANT = '{other_variant}'  # Change to:",
        f"ACTIVE_VARIANT = '{variant}'  # Change to:"
    )

    with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def run_batch(cleanplate_id, variant, batch_num, total_batches):
    """Run a single batch generation."""
    print()
    print("=" * 80)
    print(f" BATCH {batch_num}/{total_batches}")
    print(f" Cleanplate: {cleanplate_id:02d} | Variant: {variant.upper()}")
    print(f" Images in this batch: 132 (33 frames × 4 seeds)")
    print("=" * 80)
    print()

    # Update configuration
    print(f" Updating configuration to cleanplate_{cleanplate_id:02d} / {variant}...")
    update_script_config(cleanplate_id, variant)

    # Run the script
    print(f" Starting batch generation...")
    print()

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH)],
            check=True,
            text=True
        )

        elapsed = time.time() - start_time
        print()
        print(f" Batch {batch_num} completed in {elapsed/60:.1f} minutes")
        return True

    except subprocess.CalledProcessError as e:
        print()
        print(f" ERROR: Batch {batch_num} failed with exit code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print()
        print(" User interrupted batch processing")
        return False

def main():
    """Run all batches sequentially."""
    print()
    print("=" * 80)
    print("  CLIFF FALL - FULL BATCH GENERATION")
    print("=" * 80)
    print()
    print(" Configuration:")
    print(f"   Cleanplates: {len(CLEANPLATES)}")
    print(f"   Variants: {len(VARIANTS)} (original, enhanced)")
    print(f"   Frames per batch: 33")
    print(f"   Seeds per frame: 4")
    print(f"   Images per batch: 132")
    print(f"   Total batches: {len(CLEANPLATES) * len(VARIANTS)}")
    print(f"   TOTAL IMAGES: {len(CLEANPLATES) * len(VARIANTS) * 33 * 4:,}")
    print()

    # Estimate time
    avg_time_per_image = 30  # seconds
    total_images = len(CLEANPLATES) * len(VARIANTS) * 33 * 4
    estimated_hours = (total_images * avg_time_per_image) / 3600
    print(f" Estimated time: ~{estimated_hours:.1f} hours")
    print(f"   (assuming {avg_time_per_image}s per image)")
    print()

    # Skip confirmation - start immediately
    print(" Starting batch generation in 3 seconds...")
    time.sleep(3)

    overall_start = time.time()
    batch_num = 0
    total_batches = len(CLEANPLATES) * len(VARIANTS)
    completed = 0
    failed = 0

    # Loop through all combinations
    for cleanplate_id in CLEANPLATES:
        for variant in VARIANTS:
            batch_num += 1

            success = run_batch(cleanplate_id, variant, batch_num, total_batches)

            if success:
                completed += 1
            else:
                failed += 1
                print()
                response = input(" Continue with next batch? (y/n): ")
                if response.lower() != 'y':
                    break

        if failed and response.lower() != 'y':
            break

    # Final summary
    overall_elapsed = time.time() - overall_start

    print()
    print("=" * 80)
    print("  BATCH GENERATION COMPLETE!")
    print("=" * 80)
    print(f" Completed batches: {completed}/{total_batches}")
    print(f" Failed batches: {failed}")
    print(f" Total time: {overall_elapsed/3600:.2f} hours")
    print(f" Expected images: {completed * 132:,}")
    print()
    print(" Output location: D:\\ComfyUI_lizz\\output\\fall\\")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("  Batch generation interrupted by user")
        print()
