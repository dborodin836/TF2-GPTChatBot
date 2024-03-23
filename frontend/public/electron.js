const path = require('path');
const {app, BrowserWindow} = require('electron');
const {spawn} = require('child_process');
const isDev = process.env.REACT_APP_DEV === 'true';
const devTools = process.env.REACT_APP_DEVTOOLS === 'true';
let execPath;
let launchOptions;
let childProcess;
let cwd;

if (isDev) {
    execPath = path.join(__dirname, '..', '..', '.venv', 'Scripts', 'python.exe');
    launchOptions = [path.join(__dirname, '..', '..', 'main.py'), '--web-server', "--no-gui"];
    cwd = path.dirname(path.join(__dirname, '..'));
} else {
    execPath = path.join(__dirname, '..', '..', '..', 'tf2-gptcb.exe');
    launchOptions = ['--web-server', "--no-gui"];
    cwd = path.dirname(execPath);
}

function spawnChildProcess() {
    childProcess = spawn(execPath, launchOptions, {cwd: cwd});

    childProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
}

// Initialize mainWindow variable
let mainWindow;

// Function to create the main window
const createWindow = () => {
    // Configure the main window
    mainWindow = new BrowserWindow({
        width: 1040,
        height: 600,
        minWidth: 1040,
        minHeight: 600,
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
    if (devTools && isDev) {
        mainWindow.webContents.openDevTools({mode: 'detach'});
    }
};

// Create the main window when the app is ready
app.whenReady().then(() => {
    createWindow();
    spawnChildProcess();
});

// Quit the app when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    // Kill the child process when the app is terminated
    app.on('before-quit', () => {
        if (childProcess) {
            childProcess.kill();
        }
    });
})

// Create a new window when the app is activated (macOS)
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});