from flask import render_template_string, request, Response, jsonify
import os, queue

commands = queue.Queue()

def stream():
    # Continuous stream of commands from queue
    def generator():
        while True:
            if not commands.empty():
                command = commands.get()
                yield 'data: {}\n\n'.format(command)
    return Response(generator(), mimetype='text/event-stream')

def getCommand():
    # Put incoming commands into queue
    commands.put(request.data.decode(encoding='utf8'))
    return 'ok'

response_text = ''

def responseStream():
    def generator():
        global response_text
        while True:
            if response_text:
                _ = response_text
                response_text = ''
                yield 'data: {}\n\n'.format(_)
    return Response(generator(), mimetype='text/event-stream')

def getResponse():
    global response_text
    response_text = request.data.decode(encoding='utf8')
    return 'ok'

def get_config():
    # Serve user configurations for front-end
    return jsonify({
        'language': config['language']
    })

def config_view():
    # Serve front-end
    text = ''
    with open(os.path.join('.', 'modules', 'voice', 'voice.html')) as file:
        text = file.read()
    return render_template_string(text)

config = {
    'language': 'en',
    'name': 'voice',
    'pos': ['top', 'right'],
    'renderer': None,
    'scripts': ['main.js'],
    'views': [('/voice/command', 'voice-command', getCommand, ['POST'], True),
              ('/voice/stream', 'voice-stream', stream),
              ('/voice/response', 'voice-response', getResponse, ['POST'], True),
              ('/voice/response-stream', 'voice-response-stream', responseStream),
              ('/voice/config', 'voice-config', get_config, ['GET'], True)],
    'config': config_view
}