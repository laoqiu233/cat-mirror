const {remote} = require('electron')
const mirror = true;

document.addEventListener('keydown', e => {
    if (e.key == 'Escape') {
        remote.getCurrentWindow().close();
    }
});

// Clear Cache
remote.getCurrentWindow().webContents.session.clearCache();