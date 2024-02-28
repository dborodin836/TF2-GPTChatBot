// Import required modules
const path = require('path');
const { app, BrowserWindow } = require('electron');
const isDev = false;

// Initialize mainWindow variable
let mainWindow;

// Function to create the main window
const createWindow = () => {
  // Configure the main window
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true, // Enable Node.js integration
      enableRemoteModule: true, // Enable remote module
      contextIsolation: false, // Disable context isolation
      autoHideMenuBar: true, // Auto-hide menu bar
    },
  });

  // Hide the menu bar
  mainWindow.setMenuBarVisibility(false);

  // Load the appropriate URL based on the environment
  mainWindow.loadURL(
    isDev
      ? 'http://localhost:3000' // Development URL
      : `file://${path.join(__dirname, '../build/index.html')}` // Production URL
  );

  // Open DevTools in development mode
  if (isDev) {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }
};

// Create the main window when the app is ready
app.whenReady().then(createWindow);

// Quit the app when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Create a new window when the app is activated (macOS)
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});