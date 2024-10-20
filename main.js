const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const electron = require('electron');
require('electron-reload')(__dirname);

app.disableHardwareAcceleration();
app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('disable-gpu');

let mainWindow;
let pythonProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.loadURL('http://localhost:8080');

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startPythonSubprocess() {
  pythonProcess = spawn('python', ['main.py']);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`Python stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python subprocess exited with code ${code}`);
  });
}

app.on('ready', () => {
  startPythonSubprocess();
  setTimeout(createWindow, 1000); // Give the Flask server some time to start
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});
