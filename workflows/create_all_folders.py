#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-create all output folders for the full batch generation
Creates folder structure for 5 cleanplates × 2 variants × 4 seeds
"""

from pathlib import Path

# Configuration
OUTPUT_BASE = Path(r"D:\ComfyUI_lizz\output\fall")
CLEANPLATES = [1, 2, 3, 4, 5]
VARIANTS = ['original', 'enhanced']
SEEDS = [51, 42, 50, 43]

def create_all_folders():
    """Create all output folder structures."""
    print()
    print("=" * 80)
    print("  PRE-CREATING OUTPUT FOLDERS")
    print("=" * 80)
    print()

    total_folders = 0

    for cleanplate_id in CLEANPLATES:
        for variant in VARIANTS:
            for seed in SEEDS:
                # Create folder path
                folder_path = OUTPUT_BASE / f"cleanplate_{cleanplate_id:02d}" / variant / f"Seed_{seed}" / "v001"
                folder_path.mkdir(parents=True, exist_ok=True)
                total_folders += 1

                print(f" Created: fall/cleanplate_{cleanplate_id:02d}/{variant}/Seed_{seed}/v001/")

    print()
    print(f" Total folders created: {total_folders}")
    print(f" Base path: {OUTPUT_BASE}")
    print()
    print(" Folder structure:")
    print(" fall/")
    print("   cleanplate_01/")
    print("     original/")
    print("       Seed_51/v001/")
    print("       Seed_42/v001/")
    print("       Seed_50/v001/")
    print("       Seed_43/v001/")
    print("     enhanced/")
    print("       Seed_51/v001/")
    print("       ... (same structure)")
    print("   cleanplate_02/")
    print("     ... (same structure)")
    print("   ... (cleanplate_03, 04, 05)")
    print()

if __name__ == "__main__":
    create_all_folders()
    print(" Done! All folders ready for batch generation.")
    print()
