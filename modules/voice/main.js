var voice_module_commands = {
    '/display text (.+)/i': function(match) {document.getElementById('module-voice').innerHTML=`<h1>${match[1]}</h1>`;},
    '/lights ((?:on)|(?:off))/i': function(match) {match[1] == 'on' ? document.body.style.background='white' : document.body.style.background='black';},
    '/hide/i': function() {
        [...document.getElementsByClassName('container')].forEach(container => {
            container.style.opacity = 0;
        })
    },
    '/show/i': function() {
        [...document.getElementsByClassName('container')].forEach(container => {
            container.style.opacity = 1;
        })
    }
}

function createVoiceModule() {
    // Open stream for incoming commands
    var stream = new EventSource('/voice/stream');
    stream.onmessage = e => {
        // Log the commands
        console.log(`Command received: "${e.data}"`);
        // Iterate through registered commands
        for (var pattern in voice_module_commands) {
            // Make expression
            let regex = new RegExp(pattern.split('/')[1], pattern.split('/')[2]);
            if (regex.test(e.data)) {
                // Execute function if matched
                voice_module_commands[pattern](regex.exec(e.data));
                break;
            }
        }
    }
}

createVoiceModule();