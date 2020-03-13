const {remote} = require('electron')

document.addEventListener('keydown', e => {
    switch (e.key) {
        case 'Escape':
            remote.getCurrentWindow().close();
            break;
        case 'ArrowUp':
            docSize = document.documentElement.style.fontSize;
            currentSize = docSize ? parseInt(docSize) : 10;
            document.documentElement.style.fontSize = `${currentSize+1}px`;
            break;
        case 'ArrowDown':
            docSize = document.documentElement.style.fontSize;
            currentSize = docSize ? parseInt(docSize) : 10;
            document.documentElement.style.fontSize = `${currentSize-1}px`;
            break;
        default:
            break;
    }
});

// Clear Cache
remote.getCurrentWindow().webContents.session.clearCache();