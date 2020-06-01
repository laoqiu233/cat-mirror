from flask import render_template_string, request, Response, jsonify
from ..middlewares import make_safe
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

@make_safe
def receiveCommand():
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

@make_safe
def receiveResponse():
    global response_text
    response_text = request.data.decode(encoding='utf8')
    return 'ok'

@make_safe
def moduleConfig():
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
    'views': [('/voice/command', 'voice-command', receiveCommand, ['POST']),
              ('/voice/stream', 'voice-stream', stream),
              ('/voice/response', 'voice-response', receiveResponse, ['POST']),
              ('/voice/response-stream', 'voice-response-stream', responseStream),
              ('/voice/config', 'voice-config', moduleConfig, ['GET'])],
    'config': config_view
}