# ComfyUI Inpainting Node for Nuke

Bridge AI-powered inpainting from ComfyUI directly into The Foundry's Nuke compositing workflow.

## Overview

This integration allows you to:
- Send images and masks from Nuke to ComfyUI
- Run Stable Diffusion inpainting workflows
- Return results directly into your Nuke comp

## Requirements

- **Nuke**: Version 11+ (Python 2.7) or 13+ (Python 3)
- **ComfyUI**: Running server (default: localhost:8188)
- **Model**: An inpainting-compatible checkpoint (e.g., SD 1.5 inpaint, SDXL)

## Installation

### 1. Copy the Plugin

Copy `comfyui_inpaint.py` to your Nuke plugins folder:

```bash
# Linux
cp comfyui_inpaint.py ~/.nuke/

# macOS
cp comfyui_inpaint.py ~/Library/Application\ Support/Nuke/

# Windows
copy comfyui_inpaint.py %USERPROFILE%\.nuke\
```

### 2. Add to Menu

Add these lines to your `menu.py` (create if it doesn't exist):

```python
import comfyui_inpaint
comfyui_inpaint.add_to_menu()
```

### 3. Restart Nuke

The "ComfyUI" menu will appear in your Nodes toolbar.

## Usage

### Basic Workflow

1. **Start ComfyUI Server**
   ```bash
   cd /path/to/ComfyUI
   python main.py
   ```

2. **Create the Node**
   - In Nuke: `Nodes > ComfyUI > Inpaint`
   - Or press Tab and type "ComfyUI_Inpaint"

3. **Connect Inputs**
   - `img`: Your source image
   - `mask`: White areas = regions to inpaint

4. **Configure Settings**
   - Set your ComfyUI server address
   - Choose your checkpoint model
   - Enter prompts describing the desired fill

5. **Execute**
   - Click "Execute Inpaint"
   - Wait for processing (status updates in node)
   - Result appears at node output

### Node Parameters

#### Server Settings
- **Server Address**: ComfyUI server (default: `127.0.0.1:8188`)

#### Model Settings
- **Checkpoint**: Model file name from `ComfyUI/models/checkpoints/`

#### Prompt Settings
- **Positive Prompt**: Describe what to generate in masked area
- **Negative Prompt**: Describe what to avoid

#### Sampling Settings
- **Steps**: Denoising steps (higher = better quality, slower)
- **CFG Scale**: Prompt adherence (7-8 typical)
- **Denoise Strength**: 1.0 = full inpaint, lower blends with original
- **Seed**: Random seed (0 = random each time)
- **Sampler**: Sampling algorithm
- **Scheduler**: Noise schedule

#### Mask Settings
- **Grow Mask**: Expand mask by pixels for better blending

## Examples

### Remove Object
```
Positive: "clean background, empty floor, consistent lighting"
Negative: "object, person, shadow, artifacts"
Denoise: 1.0
```

### Replace Face
```
Positive: "beautiful face, detailed eyes, natural skin"
Negative: "deformed, bad anatomy, blurry"
Denoise: 0.7-0.9
```

### Fix Damaged Area
```
Positive: "matching texture, seamless blend"
Negative: "visible seams, color mismatch"
Denoise: 0.5-0.7
```

## Troubleshooting

### "Connection refused" Error
- Ensure ComfyUI server is running
- Check server address matches (default port: 8188)
- Verify firewall allows connection

### "No checkpoint found" Error
- Verify checkpoint name matches file in `ComfyUI/models/checkpoints/`
- Include file extension (`.safetensors` or `.ckpt`)

### Poor Quality Results
- Try different checkpoint (SDXL recommended for high-res)
- Increase steps (30-50)
- Adjust CFG scale
- Improve mask edges (feather in Nuke before sending)

### Mask Not Working
- Ensure mask is white where you want inpainting
- Use single channel or RGB (not alpha)
- Check mask is connected to the `mask` input

## Architecture

```
Nuke                          ComfyUI
-----                         -------
[Image] --+
          |-> Export PNG
[Mask]  --+     |
                v
          POST /upload/image
                |
                v
          POST /prompt
          (workflow JSON)
                |
                v
          [Inpainting]
                |
                v
          GET /history
          GET /view
                |
                v
[Result] <-- Download PNG
```

## Advanced: Custom Workflows

The generated workflow uses these ComfyUI nodes:

1. CheckpointLoaderSimple
2. LoadImage (for input)
3. LoadImage (for mask)
4. ImageToMask
5. CLIPTextEncode (positive)
6. CLIPTextEncode (negative)
7. VAEEncodeForInpaint
8. KSampler
9. VAEDecode
10. SaveImage

To customize, modify `generate_workflow()` in `comfyui_inpaint.py`.

## API Reference

### ComfyUIInpaintNode Class

```python
# Create and display node
inpainter = ComfyUIInpaintNode()
node = inpainter.create_node()

# Upload image
result = inpainter.upload_image(filepath, server_address)

# Queue workflow
prompt_id = inpainter.queue_prompt(workflow, server_address)

# Wait for result
result = inpainter.wait_for_completion(prompt_id, server_address)

# Download output
image_data = inpainter.download_image(filename, server_address)
```

## License

MIT License - Feel free to modify and distribute.

## Contributing

Issues and pull requests welcome on GitHub.
