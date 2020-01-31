let button = document.getElementById('voice-control');
let text = document.getElementById('voice-text');
let results_dom = document.getElementById('voice-result');

function startVoiceRecognition(language) {
    if (annyang) {
        // Warning message
        annyang.addCallback('errorPermissionBlocked', function() {
            alert('It looks like you browser have blocked the microphone permission, did you follow the steps described in README.md?');
            button.classList.remove('c-blue');
            button.disabled = true;
            text.innerHTML = "Your browser have blocked voice control";
        })
        annyang.setLanguage(language);
        annyang.start();
        annyang.pause();
        
        annyang.addCallback('result', function(results) {
            results_dom.innerHTML = results[0];
            fetch('/voice/command', {
                method: 'POST',
                body: results[0]
            })
            button.click();
        });

        button.addEventListener('click', function() {
            console.log(annyang.isListening());
            if (annyang.isListening()) {
                button.classList.replace('c-red', 'c-blue');
                text.innerHTML = 'Start';
                results_dom.classList.remove('hidden');
                annyang.pause();
            } else {
                button.classList.replace('c-blue', 'c-red');
                text.innerHTML = 'Listening...';
                results_dom.classList.add('hidden');
                annyang.resume();
            }
        });
    } else {
        button.classList.remove('c-blue');
        button.disabled = true;
        text.innerHTML = "Your browser doesn't support voice control";
    }
}

// Fetch user configuration
fetch('/voice/config')
.then(function(data) {return data.json()})
.then(function(json) {
    startVoiceRecognition(json.language);
})