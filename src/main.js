const { app, BrowserWindow, Menu, ipcMain, screen } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow = null;

function loadGreetingsConfig() {
  const configPath = path.join(__dirname, '..', 'config', 'greetings.json');
  try {
    if (fs.existsSync(configPath)) {
      const data = fs.readFileSync(configPath, 'utf-8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('Failed to load greetings config:', e);
  }
  return null;
}

function loadPetConfig(petName) {
  const petPath = path.join(__dirname, '..', 'assets', 'pets', petName, 'config.json');
  try {
    if (fs.existsSync(petPath)) {
      const data = fs.readFileSync(petPath, 'utf-8');
      return JSON.parse(data);
    }
  } catch (e) {
    console.error('Failed to load pet config:', e);
  }
  return null;
}

function createWindow() {
  const greetingsConfig = loadGreetingsConfig();
  const petSize = greetingsConfig?.pet_size || 64;

  mainWindow = new BrowserWindow({
    width: petSize,
    height: petSize,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  const displays = screen.getAllDisplays();
  const primaryDisplay = screen.getPrimaryDisplay();
  const { width: screenWidth, height: screenHeight } = primaryDisplay.size;

  mainWindow.setPosition(screenWidth - petSize - 20, screenHeight - petSize - 20);

  mainWindow.loadFile(path.join(__dirname, '..', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  console.log('Window created successfully');
  console.log('Greetings config:', greetingsConfig);
}

function createMenu() {
  const template = [
    {
      label: '退出',
      click: () => {
        app.quit();
      }
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {
  createWindow();
  createMenu();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.handle('get-greetings-config', () => {
  return loadGreetingsConfig();
});

ipcMain.handle('get-pet-config', (event, petName) => {
  return loadPetConfig(petName);
});

ipcMain.handle('get-pet-assets-path', () => {
  return path.join(__dirname, '..', 'assets', 'pets');
});

ipcMain.handle('quit-app', () => {
  app.quit();
});

ipcMain.handle('set-window-position', (event, x, y) => {
  if (mainWindow) {
    mainWindow.setPosition(Math.round(x), Math.round(y));
  }
});
