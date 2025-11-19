#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Cliff Fall Sequence Generator
Generates all 33 prompts across multiple seeds using ComfyUI API
"""

import json
import os
import sys
import time
import requests
from pathlib import Path
import re

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# ============================================================================
# CONFIGURATION
# ============================================================================

COMFYUI_URL = "http://127.0.0.1:8188"
# Use the single-seed IP-Adapter workflow (1 KSampler, we'll change seed + save path each time)
WORKFLOW_PATH = Path(__file__).parent / "cliff_fall_ipadapter_single.json"  # UI format - script converts to API

# Prompt variants - choose which one to use
PROMPT_VARIANTS = {
    'original': Path(__file__).parent / "prompts" / "ALL_PROMPTS_cliff_fall.txt",
    'enhanced': Path(__file__).parent / "prompts" / "ALL_PROMPTS_cliff_fall_PURPLE_RIM.txt"
}

# Set which variant to use (change this to 'enhanced' to run purple rim version)
ACTIVE_VARIANT = 'enhanced'  # Change to: 'original' or 'enhanced'

# Cleanplate ID (1-5) - which IP-Adapter reference image to use
CLEANPLATE_ID = 5  # Change to: 1, 2, 3, 4, or 5

PROMPTS_FILE = PROMPT_VARIANTS[ACTIVE_VARIANT]
OUTPUT_BASE = Path(r"D:\ComfyUI_lizz\output\fall") / f"cleanplate_{CLEANPLATE_ID:02d}" / ACTIVE_VARIANT

# Seeds to generate (your proven winners)
SEEDS = [51, 42, 50, 43]

# Cleanplate filename based on ID
CLEANPLATE_FILENAME = f"cliff_cleanplate_{CLEANPLATE_ID:02d}.png"

# Generation settings
SETTINGS = {
    "resolution": [1024, 720],
    "steps": 20,
    "cfg": 1.0,
    "sampler": "euler",
    "scheduler": "simple",
    "denoise": 1.0,
    "lora_strength": 0.85,
    "ipadapter_weight": 0.45
}

# ============================================================================
# PROMPT PARSER
# ============================================================================

def parse_prompts_file(filepath):
    """Parse the ALL_PROMPTS_cliff_fall.txt file and extract all frame prompts."""

    prompts = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find negative prompt
    negative_match = re.search(r'NEGATIVE PROMPT.*?:\s*\n\n(.*?)\n\n', content, re.DOTALL)
    negative_prompt = negative_match.group(1).strip() if negative_match else ""

    # Extract all frame prompts
    # Pattern: Frame_XX_XXXXX followed by blank line then the prompt
    frame_pattern = r'(Frame_\d+_(?:START|MIDDLE|END)) - (.*?)\n\n(.*?)(?=\n\n----|Frame_\d+_|NEGATIVE PROMPT|GENERATION ORDER|$)'

    matches = re.finditer(frame_pattern, content, re.DOTALL)

    for match in matches:
        frame_id = match.group(1)
        frame_name = match.group(2)
        prompt_text = match.group(3).strip()

        prompts.append({
            'id': frame_id,
            'name': frame_name,
            'prompt': prompt_text,
            'negative': negative_prompt
        })

    print(f" Parsed {len(prompts)} frame prompts")
    print(f" Negative prompt: {negative_prompt[:50]}...")

    return prompts, negative_prompt

# ============================================================================
# COMFYUI API CLIENT
# ============================================================================

class ComfyUIClient:
    def __init__(self, url):
        self.url = url
        self.client_id = "cliff_fall_generator"

    def queue_prompt(self, workflow):
        """Queue a prompt workflow to ComfyUI."""
        try:
            response = requests.post(
                f"{self.url}/prompt",
                json={"prompt": workflow, "client_id": self.client_id}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f" Error queuing prompt: {e}")
            # Print more details if available
            try:
                error_detail = response.json()
                print(f"   Error details: {error_detail}")
            except:
                pass
            return None

    def get_queue(self):
        """Get current queue status."""
        try:
            response = requests.get(f"{self.url}/queue")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f" Error getting queue: {e}")
            return None

    def get_history(self, prompt_id):
        """Get history for a specific prompt."""
        try:
            response = requests.get(f"{self.url}/history/{prompt_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

    def wait_for_completion(self, prompt_id, timeout=300):
        """Wait for a prompt to complete. Returns (success, error_msg)."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)

            if history and prompt_id in history:
                status = history[prompt_id].get('status', {})
                if status.get('completed', False):
                    # Check if there were any errors
                    if 'messages' in status:
                        errors = [msg for msg in status['messages'] if msg[0] == 'execution_error']
                        if errors:
                            return (False, str(errors[0][1]) if errors else "Unknown error")
                    return (True, None)
                elif status.get('status_str') == 'error':
                    # Get error details
                    error_msg = status.get('messages', ['Unknown error'])[0]
                    return (False, str(error_msg))

            queue = self.get_queue()
            if queue:
                running = queue.get('queue_running', [])
                pending = queue.get('queue_pending', [])

                # Check if our prompt is still in queue
                is_running = any(item[1] == prompt_id for item in running)
                is_pending = any(item[1] == prompt_id for item in pending)

                if not is_running and not is_pending:
                    # Prompt finished but not in history - this is suspicious
                    # Wait a bit more to see if history updates
                    time.sleep(2)
                    history = self.get_history(prompt_id)
                    if history and prompt_id in history:
                        continue  # Re-check with updated history
                    else:
                        # Still no history - something went wrong
                        return (False, "Prompt disappeared from queue without entering history")

            time.sleep(2)

        return (False, "Timeout")

# ============================================================================
# WORKFLOW GENERATOR
# ============================================================================

def load_base_workflow(workflow_path):
    """Load the base workflow JSON."""
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_workflow_to_api_format(workflow):
    """Convert UI export format to API format.

    UI format: {"nodes": [...], "links": [...], ...}
    API format: {"1": {node_data}, "2": {node_data}, ...}
    """
    if 'nodes' not in workflow:
        # Already in API format
        return workflow

    # Build link lookup: link_id -> (source_node_id, source_slot)
    link_map = {}
    for node in workflow['nodes']:
        if 'outputs' in node:
            for slot_idx, output in enumerate(node['outputs']):
                if output and 'links' in output and output['links']:
                    for link_id in output['links']:
                        if link_id:
                            link_map[link_id] = (str(node['id']), slot_idx)

    # Convert nodes array to API format
    api_workflow = {}

    # Node type to input field mapping
    node_input_mappings = {
        'UNETLoader': ['unet_name', 'weight_dtype'],
        'LoraLoaderModelOnly': ['lora_name', 'strength_model'],
        'DualCLIPLoader': ['clip_name1', 'clip_name2', 'type'],
        'CLIPTextEncode': ['text'],
        'EmptySD3LatentImage': ['width', 'height', 'batch_size'],
        'KSampler': ['seed', 'control_after_generate', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise'],
        'VAELoader': ['vae_name'],
        'VAEDecode': [],
        'SaveImage': ['filename_prefix'],
        'LoadImage': ['image', 'upload'],
        'IPAdapterFluxLoader': ['ipadapter', 'clip_vision', 'provider'],
        'ApplyIPAdapterFlux': ['weight', 'start_percent', 'end_percent'],
    }

    for node in workflow['nodes']:
        node_id = str(node['id'])
        class_type = node['type']

        # Build inputs dict
        inputs = {}

        # Process widget values (parameters)
        if 'widgets_values' in node and node['widgets_values']:
            field_names = node_input_mappings.get(class_type, [])
            for idx, value in enumerate(node['widgets_values']):
                if idx < len(field_names):
                    inputs[field_names[idx]] = value

        # Process input connections (from other nodes via links)
        if 'inputs' in node:
            for input_def in node['inputs']:
                if 'link' in input_def and input_def['link']:
                    link_id = input_def['link']
                    if link_id in link_map:
                        source_node_id, source_slot = link_map[link_id]
                        inputs[input_def['name']] = [source_node_id, source_slot]

        # Build API node
        api_node = {
            'class_type': class_type,
            'inputs': inputs
        }

        # Preserve mode (0 = normal, 2 = bypass)
        if 'mode' in node and node['mode'] == 2:
            api_node['_meta'] = {'mode': 2}

        api_workflow[node_id] = api_node

    return api_workflow

def create_workflow_for_seed(base_workflow, prompt, negative_prompt, seed, frame_id):
    """Create a workflow for a specific seed."""

    # Deep copy the workflow
    workflow = json.loads(json.dumps(base_workflow))

    # Find and update the prompt nodes (Node 4 = positive, Node 5 = negative)
    for node in workflow.get('nodes', []):
        if node.get('type') == 'CLIPTextEncode':
            # Positive prompt
            if 'PASTE YOUR PROMPT' in str(node.get('widgets_values', [])):
                node['widgets_values'] = [prompt]
            # Negative prompt
            elif 'blurry' in str(node.get('widgets_values', [])):
                node['widgets_values'] = [negative_prompt]

        # Update the specific KSampler for this seed
        if node.get('type') == 'KSampler':
            current_seed = node.get('widgets_values', [0])[0]
            if current_seed == seed:
                # Update filename prefix for this seed
                pass  # Seed already set correctly

        # Update SaveImage nodes with frame-specific prefix
        if node.get('type') == 'SaveImage':
            current_prefix = node.get('widgets_values', [''])[0]
            if f'seed{seed}' in current_prefix:
                node['widgets_values'] = [f"cliff_fall_{frame_id}_seed{seed}"]

    return workflow

# ============================================================================
# VERSION MANAGEMENT
# ============================================================================

def get_next_version_for_seed(seed):
    """Get the next version number for a seed by checking existing folders with actual content."""
    seed_folder = OUTPUT_BASE / f"Seed_{seed}"

    if not seed_folder.exists():
        return 1

    # Find all existing version folders
    version_folders = [d for d in seed_folder.iterdir() if d.is_dir() and d.name.startswith('v')]

    if not version_folders:
        return 1

    # Extract version numbers from folders that contain image files
    version_numbers = []
    for folder in version_folders:
        try:
            ver_num = int(folder.name[1:])  # Remove 'v' prefix
            # Check if folder actually has image files
            has_images = any(f.suffix.lower() in ['.png', '.jpg', '.jpeg'] for f in folder.glob('*'))
            if has_images:
                version_numbers.append(ver_num)
        except ValueError:
            continue

    if not version_numbers:
        return 1

    return max(version_numbers) + 1

def create_output_folder_for_seed(seed, version):
    """Create output folder structure for a seed and version in ComfyUI's output directory."""
    # ComfyUI's output directory is D:\ComfyUI_lizz\output
    # Our target is D:\ComfyUI_lizz\output\fall\cleanplate_XX\original\Seed_XX\vYYY\
    comfyui_output = Path(r"D:\ComfyUI_lizz\output")

    # Build the relative path from ComfyUI's output dir
    # This matches what we put in filename_prefix: "fall/cleanplate_01/original/Seed_51/v001/..."
    relative_path = f"fall/cleanplate_{CLEANPLATE_ID:02d}/{ACTIVE_VARIANT}/Seed_{seed}/v{version:03d}"

    full_path = comfyui_output / relative_path
    full_path.mkdir(parents=True, exist_ok=True)

    return full_path

# ============================================================================
# BATCH GENERATION
# ============================================================================

def generate_all(mode='single'):
    """
    Generate all frames for all seeds.

    mode:
        'single' - Generate one seed at a time (safer, less VRAM)
        'parallel' - Generate all 4 seeds at once (faster, more VRAM)
    """

    print("=" * 80)
    print(" CLIFF FALL SEQUENCE - AUTOMATED BATCH GENERATION")
    print(f" VARIANT: {ACTIVE_VARIANT.upper()}")
    print("=" * 80)
    print()

    # Parse prompts
    print(f" Reading prompts from {ACTIVE_VARIANT} variant...")
    prompts, negative_prompt = parse_prompts_file(PROMPTS_FILE)

    if not prompts:
        print(" No prompts found! Check the prompts file.")
        return

    print(f" Found {len(prompts)} prompts")
    print(f" Seeds: {SEEDS}")
    print(f" Total generations: {len(prompts) * len(SEEDS)}")
    print()

    # Load base workflow
    print(" Loading workflow template...")
    base_workflow = load_base_workflow(WORKFLOW_PATH)
    print(f" Loaded: {WORKFLOW_PATH.name}")
    print()

    # Initialize ComfyUI client
    client = ComfyUIClient(COMFYUI_URL)

    # Test connection
    print(" Testing ComfyUI connection...")
    queue = client.get_queue()
    if queue is None:
        print(f" Cannot connect to ComfyUI at {COMFYUI_URL}")
        print("   Make sure ComfyUI is running!")
        return
    print(" Connected to ComfyUI")
    print()

    # Determine version numbers for each seed
    print(" Checking for existing versions...")
    seed_versions = {}
    for seed in SEEDS:
        version = get_next_version_for_seed(seed)
        seed_versions[seed] = version
        output_folder = create_output_folder_for_seed(seed, version)
        print(f"  Seed {seed}: v{version:03d}  {output_folder}")
    print()

    # Generate!
    total_generated = 0
    total_failed = 0
    start_time = time.time()

    print(" Starting generation...")
    print("=" * 80)
    print()

    if mode == 'single':
        # Single mode: queue everything, then wait at the end
        all_prompt_ids = []

        # Queue all frames and seeds (no waiting)
        for i, prompt_data in enumerate(prompts, 1):
            frame_id = prompt_data['id']
            frame_name = prompt_data['name']
            prompt_text = prompt_data['prompt']

            print(f"[{i}/{len(prompts)}] {frame_id} - {frame_name}")

            for seed in SEEDS:
                version_num = seed_versions[seed]
                print(f"   Queuing seed {seed} v{version_num:03d}...", end=' ', flush=True)

                # Create workflow for this specific seed
                workflow = create_single_seed_workflow(
                    base_workflow,
                    prompt_text,
                    negative_prompt,
                    seed,
                    frame_id,
                    version_num
                )

                # Debug: Save first workflow to inspect
                if i == 1 and seed == SEEDS[0]:
                    debug_path = Path(__file__).parent / "debug_workflow.json"
                    with open(debug_path, 'w', encoding='utf-8') as f:
                        json.dump(workflow, f, indent=2)
                    print(f"DEBUG saved, ", end='', flush=True)

                # Queue it (don't wait)
                result = client.queue_prompt(workflow)

                if result and 'prompt_id' in result:
                    all_prompt_ids.append((frame_id, seed, result['prompt_id']))
                    print("queued")
                else:
                    print("failed")
                    total_failed += 1

            print()

        # Now wait for everything to complete
        print()
        print(f" All {len(all_prompt_ids)} renders queued! Waiting for completion...")
        print("=" * 80)

        for frame_id, seed, prompt_id in all_prompt_ids:
            print(f" Waiting for {frame_id} seed {seed}...", end=' ', flush=True)
            success, error = client.wait_for_completion(prompt_id, timeout=120)
            if success:
                print("done")
                total_generated += 1
            else:
                print(f"FAILED: {error}")
                total_failed += 1

        print()

    else:
        # Parallel mode: all seeds at once
        for i, prompt_data in enumerate(prompts, 1):
            frame_id = prompt_data['id']
            frame_name = prompt_data['name']
            prompt_text = prompt_data['prompt']

            print(f"[{i}/{len(prompts)}] {frame_id} - {frame_name}")
            print(f"   Generating all {len(SEEDS)} seeds in parallel...", end=' ', flush=True)

            # Create workflow with all seeds
            workflow = create_parallel_workflow(
                base_workflow,
                prompt_text,
                negative_prompt,
                frame_id,
                seed_versions
            )

            # Queue it
            result = client.queue_prompt(workflow)

            if result and 'prompt_id' in result:
                prompt_id = result['prompt_id']

                # Wait for completion (all 4 seeds)
                success = client.wait_for_completion(prompt_id, timeout=240)

                if success:
                    print("")
                    total_generated += len(SEEDS)
                else:
                    print(" timeout")
                    total_failed += len(SEEDS)
            else:
                print(" failed to queue")
                total_failed += len(SEEDS)

            print()

    # Summary
    elapsed_time = time.time() - start_time

    print()
    print("=" * 80)
    print(" GENERATION COMPLETE!")
    print("=" * 80)
    print(f" Successfully generated: {total_generated}")
    print(f" Failed: {total_failed}")
    print(f"  Total time: {elapsed_time/60:.1f} minutes")
    if total_generated > 0:
        print(f" Average per image: {elapsed_time/total_generated:.1f} seconds")
    print()
    print(f" Check output in: {OUTPUT_BASE}")
    print(f" Variant: {ACTIVE_VARIANT}")
    print()

def create_single_seed_workflow(base_workflow, prompt, negative_prompt, seed, frame_id, version_num):
    """Create a workflow for a single seed (simple - just update seed + prompts + save path)."""

    workflow = json.loads(json.dumps(base_workflow))

    # Build output path: fall/cleanplate_XX/original/Seed_XX/vYYY/
    # This is relative to ComfyUI's output directory (D:\ComfyUI_lizz\output)
    output_subfolder = f"fall/cleanplate_{CLEANPLATE_ID:02d}/{ACTIVE_VARIANT}/Seed_{seed}/v{version_num:03d}"

    # Update nodes - much simpler now!
    for node in workflow.get('nodes', []):
        # Update prompts
        if node.get('type') == 'CLIPTextEncode':
            widgets = node.get('widgets_values', [])
            if widgets and (len(str(widgets[0])) > 200 or 'PASTE YOUR PROMPT' in str(widgets) or 'lizzchar' in str(widgets[0])):
                # Positive prompt
                node['widgets_values'] = [prompt]
            elif widgets and 'blurry' in str(widgets[0]):
                # Negative prompt
                node['widgets_values'] = [negative_prompt]

        # Update KSampler seed
        if node.get('type') == 'KSampler':
            widgets = node.get('widgets_values', [])
            if widgets and len(widgets) >= 7:
                # Keep all other settings, just change seed (position 0)
                widgets[0] = seed
                node['widgets_values'] = widgets

        # Update LoadImage to use the correct cleanplate
        if node.get('type') == 'LoadImage':
            node['widgets_values'] = [CLEANPLATE_FILENAME, 'image']

        # Update SaveImage path
        if node.get('type') == 'SaveImage':
            node['widgets_values'] = [f"{output_subfolder}/cliff_{seed}_{frame_id}_v{version_num:03d}"]

    # Convert to API format and return
    return convert_workflow_to_api_format(workflow)

def create_parallel_workflow(base_workflow, prompt, negative_prompt, frame_id, seed_versions):
    """Create a workflow that runs all seeds in parallel with version-aware naming."""

    workflow = json.loads(json.dumps(base_workflow))

    # UI format: iterate over nodes array
    for node in workflow.get('nodes', []):
        if node.get('type') == 'CLIPTextEncode':
            widgets = node.get('widgets_values', [])
            if widgets and (len(str(widgets[0])) > 200 or 'PASTE YOUR PROMPT' in str(widgets)):
                node['widgets_values'] = [prompt]
            elif widgets:
                node['widgets_values'] = [negative_prompt]

        # Update SaveImage nodes with seed-specific versioned paths
        if node.get('type') == 'SaveImage':
            current_prefix = node.get('widgets_values', [''])[0] if node.get('widgets_values') else ''

            # Determine which seed based on naming
            for seed in SEEDS:
                if f'seed{seed}' in current_prefix or f'{seed}' in current_prefix:
                    version_num = seed_versions[seed]
                    output_subfolder = f"Seed_{seed}/v{version_num:03d}"
                    filename = f"{output_subfolder}/cliff_{seed}_{frame_id}_v{version_num:03d}"
                    node['widgets_values'] = [filename]
                    break

    # Convert to API format and return
    return convert_workflow_to_api_format(workflow)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    print()
    print("="*80)
    print("    CLIFF FALL SEQUENCE - AUTOMATED BATCH GENERATOR")
    print("="*80)
    print()

    # Check mode argument
    mode = 'single'
    if len(sys.argv) > 1:
        if sys.argv[1] == '--parallel':
            mode = 'parallel'
            print(" Running in PARALLEL mode (all 4 seeds at once)")
        elif sys.argv[1] == '--single':
            mode = 'single'
            print(" Running in SINGLE mode (one seed at a time)")
        else:
            print(f"Usage: {sys.argv[0]} [--single|--parallel]")
            print()
            print("  --single   : Generate one seed at a time (default, safer)")
            print("  --parallel : Generate all 4 seeds at once (faster, more VRAM)")
            sys.exit(1)
    else:
        print(" Running in SINGLE mode (default)")
        print("   Use --parallel for faster generation (requires more VRAM)")

    print()

    try:
        generate_all(mode=mode)
    except KeyboardInterrupt:
        print()
        print("  Generation interrupted by user")
        print()
    except Exception as e:
        print()
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
        print()
