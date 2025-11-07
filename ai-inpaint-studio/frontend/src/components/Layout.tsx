import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
  activeTab: string
  onTabChange: (tab: 'text-to-image' | 'inpainting' | 'settings') => void
  backendStatus: 'connected' | 'disconnected' | 'checking'
  comfyUIStatus: 'connected' | 'disconnected'
}

export default function Layout({
  children,
  activeTab,
  onTabChange,
  backendStatus,
  comfyUIStatus,
}: LayoutProps) {
  return (
    <div className="flex flex-col h-screen">
      {/* Header/Tabs */}
      <header className="bg-bg-secondary border-b border-border">
        <div className="flex items-center justify-between px-4 h-12">
          <div className="flex items-center gap-4">
            <h1 className="text-lg font-semibold">AI Inpaint Studio</h1>
          </div>
          <div className="flex items-center gap-2">
            <StatusIndicator label="Backend" status={backendStatus} />
            <StatusIndicator label="ComfyUI" status={comfyUIStatus} />
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 px-4">
          <button
            className={`tab ${activeTab === 'text-to-image' ? 'tab-active' : ''}`}
            onClick={() => onTabChange('text-to-image')}
          >
            Text to Image
          </button>
          <button
            className={`tab ${activeTab === 'inpainting' ? 'tab-active' : ''}`}
            onClick={() => onTabChange('inpainting')}
          >
            Inpainting
          </button>
          <button
            className={`tab ${activeTab === 'settings' ? 'tab-active' : ''}`}
            onClick={() => onTabChange('settings')}
          >
            Settings
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {children}
      </main>

      {/* Status Bar */}
      <footer className="bg-bg-secondary border-t border-border px-4 py-1 flex items-center justify-between text-sm text-text-secondary">
        <div className="flex items-center gap-4">
          <span>Ready</span>
        </div>
        <div className="flex items-center gap-4">
          <span>v0.1.0</span>
        </div>
      </footer>
    </div>
  )
}

// Status indicator component
function StatusIndicator({
  label,
  status,
}: {
  label: string
  status: 'connected' | 'disconnected' | 'checking'
}) {
  const statusColor = {
    connected: 'bg-success',
    disconnected: 'bg-error',
    checking: 'bg-warning',
  }[status]

  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="text-text-secondary">{label}:</span>
      <div className={`w-2 h-2 rounded-full ${statusColor}`} />
    </div>
  )
}
