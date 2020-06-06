const {app, BrowserWindow, Menu} = require('electron');
const {PythonShell} = require('python-shell');
const fs = require('fs');
const path = require('path');

let win;
let server;
//Menu.setApplicationMenu(null);

app.on('ready', () => {
    if (!process.argv.includes('no-server')) {
        server = new PythonShell('server.py');
    
        server.on('message', msg => {
            if (msg.startsWith('$INFO$')) {
                console.log(msg.slice(6));
            }
        });
    }
    
    win = new BrowserWindow({
        fullscreen: true,
        webPreferences: {
            preload: path.join(app.getAppPath(), 'preload.js')
        }
    });

    let try_count = 0;

    const fail_load = (e, errCode, errDesc) => {
        if (try_count < 5) {
            win.loadURL('http://localhost:12306');
        } else {
            let data = fs.readFileSync('templates/failed.html').toString();
            win.loadURL('data:text/html;charset=utf-8,' + encodeURI(data.replace('{%err%}', `${errCode} ${errDesc}`)));
            win.webContents.removeListener('did-fail-load', fail_load);
        }
        try_count++;
    }

    win.webContents.on('did-fail-load', fail_load);

    win.loadURL('http://localhost:12306');

    win.on('closed', () => {
        if (!process.argv.includes('no-server')) server.terminate();
        win = null;
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
})