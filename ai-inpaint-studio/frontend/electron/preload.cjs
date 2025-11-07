/**
 * Electron Preload Script
 * Bridge between main process and renderer (React app)
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods to renderer process
contextBridge.exposeInMainWorld('electron', {
  // Get app paths
  getAppPath: () => ipcRenderer.invoke('get-app-path'),

  // Platform info
  platform: process.platform,

  // Add more APIs as needed
});
