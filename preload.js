const {remote} = require('electron')

document.addEventListener('keydown', e => {
    if (e.key == 'Escape') {
        remote.getCurrentWindow().close();
    }
});

// Clear Cache
remote.getCurrentWindow().webContents.session.clearCache();