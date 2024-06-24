import path from 'path';
import { app, BrowserWindow } from 'electron';
import { spawn } from 'child_process';
import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';

const env = process.env.VITE_ENVIRONMENT;

globalThis.__filename = fileURLToPath(import.meta.url);
globalThis.__dirname = dirname(__filename);

let execPath;
let launchOptions;
let childProcess;
let cwd;
let mainWindow;
let restartAttempts = 0;
const MAX_RETRIES = 4;

if (env === 'demo') {
  // Demo
  execPath = path.join(__dirname, '..', '..', '.venv', 'Scripts', 'python.exe');
  launchOptions = [path.join(__dirname, '..', '..', 'main.py'), '--web-server', '--no-gui', '--sleep', '1'];
  cwd = path.dirname(path.join(__dirname, '..'));
} else if (env === "development") {
  // Development
  // Doesn't start backend
} else {
  // Production
  execPath = path.join(__dirname, '..', '..', '..', 'tf2-gptcb');
  launchOptions = ['--web-server', '--no-gui', '--sleep', '1'];
  cwd = path.dirname(execPath);
}

function spawnChildProcess() {
  childProcess = spawn(execPath, launchOptions, { cwd: cwd });

  childProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    mainWindow.webContents.send('alert-message', 'TF2-GPTChatbot process died. Restarting...');

    if (restartAttempts < MAX_RETRIES) {
      restartAttempts++;
      console.log(`Restart attempt #${restartAttempts}`);
      spawnChildProcess();
    } else {
      console.log('Max restart attempts reached. Not restarting.');
      mainWindow.webContents.send(
        'alert-message',
        'Max restart attempts reached. Try restarting app.',
      );
    }
  });
}

// Function to create the main window
const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1040,
    height: 600,
    minWidth: 1040,
    minHeight: 600,
    webPreferences: {
      sandbox: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // Hide the menu bar
  mainWindow.setMenuBarVisibility(false);

  // Load the appropriate URL based on the environment
  mainWindow.loadURL(
    env === 'development'
      ? 'http://localhost:3000' // Development URL
      : `file://${path.join(__dirname, '../build/index.html')}`, // Production URL
  );

  // Open DevTools in development mode
  if (env === 'development') {
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  }
};

// Create the main window when the app is ready
app.whenReady().then(() => {
  createWindow();
  if (env === 'production' || env === 'demo' || env === undefined) {
    spawnChildProcess();
  }
});

// Quit the app when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

if (env === 'production' || env === 'demo' || env === undefined) {
  app.on('before-quit', () => {
    // Kill the child process when the app is terminated
    app.on('before-quit', () => {
      if (childProcess) {
        childProcess.kill();
      }
    });
  });
}


// Create a new window when the app is activated (macOS)
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
