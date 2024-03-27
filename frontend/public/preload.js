const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('electronAPI', {
  onAlertMessage: (callback) => ipcRenderer.on('alert-message', (_event, value) => callback(value))
})
