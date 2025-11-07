/**
 * API service for communicating with Python backend
 */

const API_BASE_URL = 'http://127.0.0.1:8000/api'

export interface HealthResponse {
  status: string
  backend: {
    running: boolean
    version: string
  }
  comfyui: {
    running: boolean
    url: string
  }
  hardware: {
    gpu_available: boolean
    gpu_name: string
    vram_used: string
    vram_total: string
    ram_used: string
    ram_total: string
  }
}

export interface GenerateRequest {
  prompt: string
  style?: string
  steps?: number
  width?: number
  height?: number
  seed?: number | null
}

export interface GenerateResponse {
  image_path: string
  prompt_id: string
  seed: number
  generation_time: number
}

export interface InpaintRequest {
  original_image: File
  annotated_image: File
  prompt?: string
  negative_prompt?: string
  model?: 'sd15' | 'lama'
  steps?: number
  cfg?: number
  denoise?: number
}

export interface InpaintResponse {
  result_path: string
  prompt_id: string
  generation_time: number
}

/**
 * Check backend and ComfyUI health
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error('Backend not responding')
  }
  return response.json()
}

/**
 * Simple ping to check if backend is alive
 */
export async function ping(): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE_URL}/ping`)
  if (!response.ok) {
    throw new Error('Backend not responding')
  }
  return response.json()
}

/**
 * Generate image from text prompt
 */
export async function generateImage(request: GenerateRequest): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    throw new Error('Failed to generate image')
  }

  return response.json()
}

/**
 * Inpaint/remove objects from image
 */
export async function inpaintImage(request: InpaintRequest): Promise<InpaintResponse> {
  const formData = new FormData()
  formData.append('original_image', request.original_image)
  formData.append('annotated_image', request.annotated_image)
  formData.append('prompt', request.prompt || 'photorealistic, high quality')
  formData.append('negative_prompt', request.negative_prompt || '')
  formData.append('model', request.model || 'sd15')
  formData.append('steps', String(request.steps || 30))
  formData.append('cfg', String(request.cfg || 7.5))
  formData.append('denoise', String(request.denoise || 1.0))

  const response = await fetch(`${API_BASE_URL}/inpaint`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to inpaint image')
  }

  return response.json()
}

/**
 * WebSocket connection for real-time progress
 */
export function connectProgressWebSocket(
  promptId: string,
  onProgress: (data: any) => void,
  onError?: (error: Event) => void
): WebSocket {
  const ws = new WebSocket(`ws://127.0.0.1:8000/api/ws/generate/${promptId}`)

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onProgress(data)
  }

  if (onError) {
    ws.onerror = onError
  }

  return ws
}
