# AI Inpaint Studio

Desktop application for AI-powered image generation and inpainting.

## Architecture

```
Frontend: Electron + React + TypeScript + Tailwind CSS
Backend:  Python FastAPI
ML:       ComfyUI + FLUX + SD 1.5 Inpainting
```

## Prerequisites

### Backend:
- Python 3.12
- PyTorch with CUDA support
- ComfyUI with models installed

### Frontend:
- Node.js 18+ and npm

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 3. Copy Your Existing Scripts

Copy your existing ComfyUI scripts to the backend:

```bash
# From your ComfyUI_lizz directory
cp flux_generate.py ../ai-inpaint-studio/backend/models/
cp flux_inpaint.py ../ai-inpaint-studio/backend/models/
cp flux_cinematic_workflow.json ../ai-inpaint-studio/backend/models/
cp sd_inpaint_workflow.json ../ai-inpaint-studio/backend/models/
```

## Running the Application

### Start ComfyUI (Terminal 1):
```bash
cd ComfyUI_lizz
python main.py --listen 127.0.0.1 --port 8190
```

### Start Backend (Terminal 2):
```bash
cd ai-inpaint-studio/backend
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

python main.py
```
Backend will run on: http://127.0.0.1:8000

### Start Frontend (Terminal 3):
```bash
cd ai-inpaint-studio/frontend

# Development mode with hot reload
npm run electron:dev
```

The Electron app will open automatically!

## Development

### Frontend Only (for UI work):
```bash
cd frontend
npm run dev
```
Opens in browser at: http://localhost:5173

### Backend API Docs:
Once backend is running, visit: http://127.0.0.1:8000/docs

## Building for Production

```bash
cd frontend
npm run electron:build
```

This creates an installer in `frontend/dist/`

## Project Status

### ✅ Phase 1: MVP Setup (Complete!)
- [x] Project structure
- [x] Backend FastAPI with health check
- [x] Frontend Electron + React + Dark theme
- [x] Basic UI layout with tabs
- [x] Backend-frontend communication

### 🚧 Phase 2: Text-to-Image (In Progress)
- [x] UI components created
- [ ] Wire up flux_generate.py
- [ ] WebSocket progress updates
- [ ] Display generated images

### 📋 Phase 3: Inpainting (Planned)
- [ ] Canvas annotation tool
- [ ] Wire up flux_inpaint.py
- [ ] Before/After slider

### 📋 Phase 4: LaMa Integration (Planned)
- [ ] Add LaMa model
- [ ] Better object removal

### 📋 Phase 5: SAM Integration (Planned)
- [ ] Click-to-select objects
- [ ] Auto-generate masks

## Troubleshooting

### Backend won't start:
- Make sure port 8000 is not in use
- Check that virtual environment is activated
- Verify all dependencies installed

### Frontend won't connect to backend:
- Ensure backend is running on port 8000
- Check CORS settings in backend/main.py
- Look for errors in browser console (F12)

### ComfyUI not detected:
- Make sure ComfyUI is running on port 8190
- Check http://127.0.0.1:8190 in browser
- Verify GPU drivers are installed

## Next Steps

1. Test the basic app (all 3 terminals running)
2. Wire up flux_generate.py to backend
3. Implement real-time progress updates
4. Add image display functionality
5. Build inpainting canvas

## License

MIT
