# ComfyUI Roto Node - Setup Guide

This guide covers the installation and setup of the **ComfyUI_Roto** node for Nuke, including all required ComfyUI custom nodes and models.

---

## 📋 Prerequisites

- **Nuke 11+** (Python 2.7) or **Nuke 13+** (Python 3)
- **ComfyUI** installed and running
- Python `requests` library (if not already installed)

---

## 🔧 ComfyUI Custom Nodes Required

Install these custom nodes in your ComfyUI `custom_nodes/` directory:

### 1. **ComfyUI-segment-anything-2** (kijai) - **REQUIRED**
Provides SAM2 model support for all three workflows.

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/kijai/ComfyUI-segment-anything-2.git
```

**Nodes provided:**
- `SAM2ModelLoader`
- `Sam2Segmentation`
- `Sam2VideoSegmentation`
- `MaskToImage`

---

### 2. **ComfyUI-Contextual-SAM2** (MicheleGuidi) - **For Contextual-SAM2 workflow**
Provides Florence2 + SAM2 integration for context-aware segmentation.

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/MicheleGuidi/ComfyUI-Contextual-SAM2.git
```

**Nodes provided:**
- `Florence2ModelLoader`
- `Florence2Run`
- `Sam2ContextSegmentation`
- `Sam2TiledSegmentation`

---

### 3. **ComfyUI-Grounding-DINO-SAM** (or equivalent) - **For Grounding DINO workflow**
Provides Grounding DINO + SAM integration for natural language grounding.

**Option A:** ComfyUI_GroundingDINO (recommended)
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/IDEA-Research/ComfyUI_GroundingDINO.git
```

**Option B:** Check ComfyUI Manager for "Grounding DINO" nodes

**Nodes provided:**
- `GroundingDinoModelLoader`
- `GroundingDinoDetection`
- `SAMModelLoader`
- `SAMSegmentation`

---

### 4. **ComfyUI-HQ-Image-Save** (spacepxl) - **OPTIONAL (for EXR support)**
Enables 32-bit EXR sequence loading/saving.

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/spacepxl/ComfyUI-HQ-Image-Save.git
```

**Nodes provided:**
- `LoadEXR`
- `LoadEXRFrames`
- `SaveEXRFrames`

---

### 5. **ComfyUI-VideoHelperSuite** (Kosinkadink) - **OPTIONAL (for video support)**
Enables video/sequence batch loading.

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
```

---

## 📦 Models Required

The following models will be **auto-downloaded** on first use, or you can manually download them to the appropriate folders.

### **SAM2 Models** (auto-download from Hugging Face)
Location: `ComfyUI/models/sam2/` or auto-downloaded by custom node

- **sam2.1_hiera_tiny.safetensors** (~100MB) - Fastest, lowest quality
- **sam2.1_hiera_small.safetensors** (~200MB) - Balanced
- **sam2.1_hiera_base_plus.safetensors** (~300MB) - **Recommended**
- **sam2.1_hiera_large.safetensors** (~700MB) - Best quality, slowest

**Download source:** Auto-downloaded from `Kijai/sam2-safetensors` on Hugging Face

---

### **Florence2 Models** (for Contextual-SAM2)
Location: Auto-downloaded via Hugging Face transformers

- **microsoft/florence-2-base** (~300MB) - **Recommended**
- **microsoft/florence-2-large** (~800MB) - Better detection, slower

**Download:** Automatically pulled from Hugging Face on first use

---

### **Grounding DINO Models** (for Grounding DINO workflow)
Location: `ComfyUI/models/grounding-dino/` (or auto-downloaded)

- **GroundingDINO_SwinT_OGC (694MB)** - **Recommended**
- **GroundingDINO_SwinB (938MB)** - Better accuracy

**Download source:** Auto-downloaded on first use, or manually from:
- https://huggingface.co/ShilongLiu/GroundingDINO

---

### **SAM Models** (for Grounding DINO + SAM workflow)
Location: `ComfyUI/models/sam/`

- **sam_vit_h (2.56GB)** - **Recommended** (ViT-H, best quality)
- **sam_vit_l (1.25GB)** - ViT-L, balanced
- **sam_vit_b (375MB)** - ViT-B, fastest

**Download source:**
- https://github.com/facebookresearch/segment-anything#model-checkpoints

---

## 🖥️ VRAM Requirements

Recommended GPU VRAM based on processing resolution:

| Resolution | Workflow | Minimum VRAM | Recommended VRAM |
|------------|----------|--------------|------------------|
| **720p (1280x720)** | SAM2 | 4GB | 6GB |
| **720p** | Contextual-SAM2 | 6GB | 8GB |
| **720p** | Grounding DINO | 6GB | 8GB |
| **HD (1920x1080)** | SAM2 | 6GB | 8GB |
| **HD** | Contextual-SAM2 | 8GB | 12GB |
| **HD** | Grounding DINO | 8GB | 12GB |
| **2K (2048x1080)** | SAM2 | 8GB | 12GB |
| **2K** | Contextual-SAM2 | 12GB | 16GB |
| **4K (4096x2160)** | Any | ❌ Not recommended | 24GB+ |

**Recommendation:** Use **720p** or **HD** processing with Smart Downrez mode for 4K source footage.

---

## 🚀 Nuke Installation

### Step 1: Copy Files

Copy `comfyui_roto.py` to your Nuke scripts directory:

```bash
# Linux/Mac
cp comfyui_roto.py ~/.nuke/

# Windows
copy comfyui_roto.py %USERPROFILE%\.nuke\
```

### Step 2: Update menu.py

Add to your `~/.nuke/menu.py`:

```python
import comfyui_roto
comfyui_roto.add_to_menu()
```

### Step 3: Restart Nuke

Restart Nuke to load the menu entry.

---

## 🎬 Usage

### Basic Workflow

1. **Launch ComfyUI** and ensure it's running at `127.0.0.1:8188`

2. **In Nuke:**
   - Go to **Nodes > ComfyUI > Roto**
   - Connect your plate to the `img` input
   - Select **Workflow Mode** (SAM2, Contextual-SAM2, or Grounding DINO)
   - Set **Frame Range** or enable "Current Frame Only"

3. **Configure Segmentation:**
   - **Text Prompt:** "the person", "the car", etc.
   - **Selection Method:** Point, BBox, or Text Only
   - Set point/bbox coordinates if using Point/BBox mode

4. **Resolution Settings:**
   - **Process Mode:** "Smart Downrez" (recommended for 4K)
   - **Target Resolution:** "720p" or "HD"
   - Enable **"Upscale Alpha to Source"**

5. **Click "Execute Roto"**

6. **Result:** Alpha matte will load into the node's output

---

## 🔍 Workflow Mode Guide

### **SAM2** (Basic)
- **Best for:** Simple, well-defined subjects
- **Input:** Point or BBox on first frame
- **Features:** Temporal tracking across frames
- **Speed:** Fast
- **Accuracy:** Good

### **Contextual-SAM2** (Florence2 + SAM2)
- **Best for:** Complex scenes, multiple objects
- **Input:** Text prompt (auto-detects with Florence2)
- **Features:** Object detection + context-aware segmentation
- **Speed:** Medium
- **Accuracy:** Excellent

### **Grounding DINO + SAM**
- **Best for:** Natural language grounding, open-vocabulary
- **Input:** Text prompt (e.g., "person wearing red shirt")
- **Features:** Advanced language understanding + segmentation
- **Speed:** Medium-slow
- **Accuracy:** Excellent for complex queries

---

## 🛠️ Troubleshooting

### **Error: "No module named 'comfyui_roto'"**
- Ensure `comfyui_roto.py` is in your `.nuke` folder
- Check `menu.py` has the correct import statement
- Restart Nuke

### **Error: "Failed to upload image"**
- Verify ComfyUI is running at the server address
- Check firewall/network settings
- Try accessing `http://127.0.0.1:8188` in a browser

### **Error: "No output images found"**
- Workflow may have failed in ComfyUI
- Check ComfyUI console for errors
- Ensure required custom nodes are installed
- Verify models are downloaded

### **Out of Memory (OOM)**
- Reduce **Target Resolution** to 720p
- Enable **Smart Downrez** mode
- Use smaller SAM2 model (tiny or small)
- Process fewer frames at once

### **Poor mask quality**
- Try **HD** or **2K** processing resolution
- Use larger SAM2 model (base_plus or large)
- Adjust point/bbox coordinates
- Refine text prompt for Contextual-SAM2/DINO

---

## 📊 Performance Tips

### For 4K Workflows:
1. **Always use Smart Downrez** to 720p or HD
2. Process frame-by-frame (built into node)
3. Use **SAM2 base_plus** model (good balance)
4. Upscale alpha in Nuke after processing

### For Speed:
1. Use **SAM2** workflow (fastest)
2. Set Target Resolution to **720p**
3. Use **sam2.1_hiera_tiny** or **small** model
4. Process "Current Frame Only" for testing

### For Quality:
1. Use **Contextual-SAM2** or **Grounding DINO** workflow
2. Set Target Resolution to **HD** or **2K**
3. Use **sam2.1_hiera_large** model
4. Fine-tune text prompts and detection thresholds

---

## 📝 Example Prompts

### Text Prompts (Contextual-SAM2 / Grounding DINO):
- "the person"
- "the main character"
- "the red car"
- "person wearing blue jacket"
- "the building in the background"
- "all people in the scene" (may segment multiple)

### Point Selection (SAM2):
- Click center of object you want to segment
- Use coordinates at **processing resolution** (e.g., 720p coords)

### BBox Selection:
- Draw box around entire object
- Use coordinates at **processing resolution**

---

## 🔗 Useful Links

- **ComfyUI:** https://github.com/comfyanonymous/ComfyUI
- **SAM2:** https://github.com/facebookresearch/segment-anything-2
- **Florence-2:** https://huggingface.co/microsoft/Florence-2-base
- **Grounding DINO:** https://github.com/IDEA-Research/GroundingDINO

---

## 📄 License

MIT License - Free to use and modify

---

## 🐛 Issues & Support

For bugs or feature requests, please open an issue on the GitHub repository.

---

**Happy Rotoscoping! 🎬✨**
