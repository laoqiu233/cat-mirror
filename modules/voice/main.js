var voice_module_commands = {
    '/(?:(?:Ok)|(?:Okay)) boomer (.+)/i': function(match) {document.getElementById('module-voice').innerHTML=`<h1>${match[1]}</h1>`}
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