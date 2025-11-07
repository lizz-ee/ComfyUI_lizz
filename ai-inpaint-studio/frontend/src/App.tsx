import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import TextToImage from './components/TextToImage'
import Inpainting from './components/Inpainting'
import { checkHealth } from './services/api'

type Tab = 'text-to-image' | 'inpainting' | 'settings'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('text-to-image')
  const [backendStatus, setBackendStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking')
  const [comfyUIStatus, setComfyUIStatus] = useState<'connected' | 'disconnected'>('disconnected')

  // Check backend health on mount
  useEffect(() => {
    const checkBackendHealth = async () => {
      try {
        const health = await checkHealth()
        setBackendStatus('connected')
        setComfyUIStatus(health.comfyui.running ? 'connected' : 'disconnected')
      } catch (error) {
        setBackendStatus('disconnected')
        setComfyUIStatus('disconnected')
      }
    }

    checkBackendHealth()
    const interval = setInterval(checkBackendHealth, 5000) // Check every 5s

    return () => clearInterval(interval)
  }, [])

  const renderContent = () => {
    switch (activeTab) {
      case 'text-to-image':
        return <TextToImage />
      case 'inpainting':
        return <Inpainting />
      case 'settings':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Settings</h2>
            <p className="text-text-secondary">Settings panel coming soon...</p>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <Layout
      activeTab={activeTab}
      onTabChange={setActiveTab}
      backendStatus={backendStatus}
      comfyUIStatus={comfyUIStatus}
    >
      {renderContent()}
    </Layout>
  )
}

export default App
