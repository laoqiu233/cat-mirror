from flask import render_template_string, request, abort, jsonify, url_for, redirect, Response
from time import sleep
import os, json

def stream():
    # Sends a SSE whenever the format is modified
    def generator():
        format = None
        while True:
            # Open the config file to check changes
            with open(os.path.join('.', 'modules', 'clock', 'config.json'), encoding='utf-8') as file:
                config_file = json.load(file)
                # If the format is changed, send a SSE
                if 'format' in config_file and config_file['format'] != format:
                    format = config_file['format']
                    yield 'data: {}\n\n'.format(format)
            # Checks every half of a second
            sleep(0.5)
    return Response(generator(), mimetype='text/event-stream')

def change_format():
    # API for clock format
    if request.method == 'POST':
        # If the user haven't' specified a format, return 400
        if 'format-input' not in request.values:
            abort(400)
        # Change the format in file
        with open(os.path.join('.', 'modules', 'clock', 'config.json'), 'w', encoding='utf-8') as file:
            print(json.dumps({'format': request.values['format-input']}))
            json.dump({'format': request.values['format-input']}, file)
        return redirect(url_for('config-clock'))
    elif request.method == 'GET':
        # Give user the current format
        with open(os.path.join('.', 'modules', 'clock', 'config.json'), encoding='utf-8') as file:
            config_file = json.load(file)
            # If there is no format specified, return 404
            if 'format' not in config_file:
                abort(404)
            return jsonify(config_file)

def config():
    # Simply renders the config page
    with open(os.path.join('.', 'modules', 'clock', 'config.html')) as file:
        return render_template_string(file.read())

config = {
    'name': 'clock', # Should be the same as the folder name
    'renderer': None,
    'pos': ['bottom', 'left'],
    'styles': ['clock.css'],
    'scripts': ['main.js'],
    'views': [('/clock/format', 'clock-format', change_format, ['GET', 'POST']),
              ('/clock/stream', 'clock-stream', stream)],
    'config': config,
}