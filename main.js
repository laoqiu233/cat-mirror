const {app, BrowserWindow, Menu} = require('electron');
const {PythonShell} = require('python-shell');
const path = require('path');

let win;
let server;
Menu.setApplicationMenu(null)

app.on('ready', () => {
    server = new PythonShell('server.py');

    win = new BrowserWindow({
        fullscreen: true,
        webPreferences: {
            preload: path.join(app.getAppPath(), 'preload.js')
        }
    });

    win.loadURL('http://localhost:12306');

    win.on('closed', () => {
        win = null;
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
})