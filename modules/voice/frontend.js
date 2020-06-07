setMessageSocketHandler('voice', (msg) => {
    switch (msg) {
        case 'lights on':
            document.body.style.backgroundColor = '#FFF';
            break;
        case 'lights off':
            document.body.style.backgroundColor = '#000';
            break;
        case 'show':
            for (let elem of document.getElementsByClassName('module-container')) {
                console.log(elem);
                elem.style.display = '';
            }
            break;
        case 'hide':
            for (let elem of document.getElementsByClassName('module-container')) {
                console.log(elem);
                elem.style.display = 'none';
            }
            break;
    }
})