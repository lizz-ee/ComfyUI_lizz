export default function Inpainting() {
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Image Inpainting</h2>

      <div className="card">
        <p className="text-text-secondary">
          Inpainting interface coming soon in Phase 3...
        </p>
        <p className="text-sm text-text-secondary mt-2">
          Features:
        </p>
        <ul className="list-disc list-inside text-sm text-text-secondary mt-2 space-y-1">
          <li>Upload or select image</li>
          <li>Draw mask with brush/circle tools</li>
          <li>Auto-detect objects with SAM (click to select)</li>
          <li>Remove objects with SD 1.5 or LaMa</li>
          <li>Before/After comparison slider</li>
        </ul>
      </div>
    </div>
  )
}
