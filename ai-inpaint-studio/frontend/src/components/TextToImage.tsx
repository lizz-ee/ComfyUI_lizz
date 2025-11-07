import { useState } from 'react'
import { generateImage, connectProgressWebSocket } from '../services/api'

const STYLES = [
  { value: 'cinematic', label: 'Cinematic' },
  { value: 'night', label: 'Night' },
  { value: 'photoreal', label: 'Photo Realistic' },
  { value: 'dramatic', label: 'Dramatic' },
  { value: 'portrait', label: 'Portrait' },
  { value: 'landscape', label: 'Landscape' },
  { value: 'vintage', label: 'Vintage' },
]

export default function TextToImage() {
  const [prompt, setPrompt] = useState('')
  const [style, setStyle] = useState('cinematic')
  const [steps, setSteps] = useState(20)
  const [isGenerating, setIsGenerating] = useState(false)
  const [progress, setProgress] = useState(0)
  const [generatedImage, setGeneratedImage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setIsGenerating(true)
    setError(null)
    setProgress(0)
    setGeneratedImage(null)

    try {
      const result = await generateImage({
        prompt,
        style,
        steps,
      })

      // Connect to WebSocket for progress updates
      const ws = connectProgressWebSocket(
        result.prompt_id,
        (data) => {
          setProgress(data.percent)
        },
        (error) => {
          console.error('WebSocket error:', error)
        }
      )

      // For now, just show mock image path
      // TODO: Actually display the generated image
      setGeneratedImage(result.image_path)
      setIsGenerating(false)

      // Close WebSocket
      setTimeout(() => ws.close(), 100)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate image')
      setIsGenerating(false)
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Text to Image Generation</h2>

      <div className="space-y-6">
        {/* Prompt Input */}
        <div>
          <label className="block text-sm font-medium mb-2">Prompt</label>
          <textarea
            className="input-field resize-none"
            rows={3}
            placeholder="Describe the image you want to generate..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            disabled={isGenerating}
          />
        </div>

        {/* Style Selector */}
        <div>
          <label className="block text-sm font-medium mb-2">Style</label>
          <select
            className="input-field"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            disabled={isGenerating}
          >
            {STYLES.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </div>

        {/* Steps */}
        <div>
          <label className="block text-sm font-medium mb-2">
            Steps: {steps}
          </label>
          <input
            type="range"
            min="10"
            max="50"
            step="5"
            value={steps}
            onChange={(e) => setSteps(Number(e.target.value))}
            disabled={isGenerating}
            className="w-full"
          />
        </div>

        {/* Generate Button */}
        <button
          className="btn-primary w-full"
          onClick={handleGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate Image'}
        </button>

        {/* Progress Bar */}
        {isGenerating && (
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Progress</span>
              <span>{progress}%</span>
            </div>
            <div className="w-full bg-bg-tertiary rounded-full h-2">
              <div
                className="bg-accent h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-4 bg-error/20 border border-error rounded text-error">
            {error}
          </div>
        )}

        {/* Generated Image Preview */}
        {generatedImage && (
          <div className="card">
            <h3 className="text-lg font-semibold mb-2">Generated Image</h3>
            <div className="bg-bg-tertiary rounded p-4 text-center">
              <p className="text-text-secondary">Image path: {generatedImage}</p>
              <p className="text-xs text-text-secondary mt-2">
                (Image display coming soon)
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
