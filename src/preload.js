const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getConfig: () => ipcRenderer.invoke('get-config'),
  getPetConfig: (petName) => ipcRenderer.invoke('get-pet-config', petName),
  getPetAssetsPath: () => ipcRenderer.invoke('get-pet-assets-path'),
  quitApp: () => ipcRenderer.invoke('quit-app'),
  setWindowPosition: (x, y) => ipcRenderer.invoke('set-window-position', x, y)
});
