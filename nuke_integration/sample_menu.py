# Sample menu.py for Nuke
# Copy this to your .nuke folder and rename to menu.py
# Or add these lines to your existing menu.py

import nuke

# Import ComfyUI Inpaint integration
try:
    import comfyui_inpaint
    comfyui_inpaint.add_to_menu()
    print("ComfyUI Inpaint node loaded successfully")
except ImportError as e:
    print(f"Failed to load ComfyUI Inpaint: {e}")
    print("Make sure comfyui_inpaint.py is in your .nuke folder or NUKE_PATH")
