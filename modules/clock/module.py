from flask import render_template_string, request, abort, jsonify, url_for, redirect, Response
from time import sleep
import os, json

def stream():
    # Sends a SSE whenever the format is modified
    def generator():
        format = {}
        while True:
            # Open the config file to check changes
            file = open(os.path.join('.', 'modules', 'clock', 'config.json'), encoding='utf-8')
            config_file = json.load(file)
            file.close()
            # If the format is changed, send a SSE
            if format.get('header', '') != config_file.get('header', '') or format.get('subtitle', '') != config_file.get('subtitle', ''):
                format = config_file
                yield 'data: {}\n\n'.format(json.dumps(config_file))
            # Checks every half of a second
            sleep(0.5)
    return Response(generator(), mimetype='text/event-stream')

def change_format():
    # API for clock format
    if request.method == 'POST':
        # If the user haven't specified a format, return 400
        if 'format-header' not in request.values or 'format-subtitle' not in request.values:
            abort(400)
        # Change the format in file
        with open(os.path.join('.', 'modules', 'clock', 'config.json'), 'w', encoding='utf-8') as file:
            json.dump({'header': request.values['format-header'], 'subtitle': request.values['format-subtitle']}, file)
        return redirect(url_for('config-clock'))
    elif request.method == 'GET':
        # Give user the current format
        file = open(os.path.join('.', 'modules', 'clock', 'config.json'), encoding='utf-8')
        config_file = json.load(file)
        # If there is no format specified, write default format into the file
        if 'header' not in config_file or 'subtitle' not in config_file:
            file.close()
            file = open(os.path.join('.', 'modules', 'clock', 'config.json'), 'w', encoding='utf-8')
            config_file['header'] = config_file.get('header', '%H:%M:%S')
            config_file['subtitle'] = config_file.get('subtitle', '%U, %m-%d')
            json.dump(config_file, file)
        file.close()
        
        return jsonify(config_file)

def config_view():
    # Simply renders the config page
    with open(os.path.join('.', 'modules', 'clock', 'config.html')) as file:
        return render_template_string(file.read())

config = {
    'name': 'clock', # Should be the same as the folder name
    'renderer': None,
    'pos': ['bottom', 'left'],
    'styles': ['clock.css'],
    'scripts': ['main.js'],
    'views': [('/clock/format', 'clock-format', change_format, ['GET', 'POST'], True),
              ('/clock/stream', 'clock-stream', stream)],
    'config': config_view,
}