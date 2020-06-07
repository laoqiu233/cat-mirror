from flask import Flask, request, render_template, send_file, abort, redirect, url_for, make_response, Response
from modules.helpers import moduleClass
from modules.middlewares import make_safe
from modules.utils import settings, generate_token, Channel
import os, importlib, json, threading

def add_module_view(url, endpoint, handler, methods=['GET']):
    app.add_url_rule(url, endpoint, handler, methods=methods)

app = Flask(__name__)

modules = []
to_load = [
    'voice',
    'clock',
    'headlines',
    'weather'
]
served_once = False

# Sockets
json_channel = Channel()
msg_channel = Channel()

app.add_url_rule('/sockets/json', 'json-socket', json_channel.subscribe)
app.add_url_rule('/sockets/message', 'message-socket', msg_channel.subscribe)

threads = []

# Import modules
for folder in to_load:
    # Is valid module
    if os.path.exists(os.path.join('.', 'modules', folder, 'module.py')):
        print('Loading', folder)
        try:
            print('Importing')
            module = importlib.import_module('modules.{}.module'.format(folder))
            print(module.module.__config__, folder)
        except Exception as e:
            print('$INFO$[Warning] Cannot import module "{}"'.format(folder))
            print(e)
            continue
        # Check if module.py file is valid
        try:
            assert 'module' in dir(module) and type(module.module) == moduleClass, 'No module object in file'
            config = module.module.__config__
            assert folder == config.get('name', ''), 'The folder name and the module name are not the same'
            assert callable(config.get('renderer', '')) or config.get('renderer', '') == None, 'Renderer is not a function'

            if (callable(config.get('configView', ''))):
                add_module_view('/config/{}'.format(folder), 'config-{}'.format(folder), config['configView'])

            for view in config.get('views', ''):
                assert callable(view[2]), 'View is not a function'
                assert len(view) == 4, 'Error with view'
                add_module_view(*view)

        except AssertionError as e:
            print('$INFO$[Warning] Module.py file for module "{}" is invalid!'.format(folder))
            print(e)
            continue
        
        print('Creating function')
        def updateData(module_obj):
            while True:
                if (not module_obj.jsonQueue.empty()):
                    json_channel.publish(module_obj.jsonQueue.get())
                

                if (not module_obj.messageQueue.empty()):
                    msg_channel.publish(module_obj.messageQueue.get())

        th = threading.Thread(target=updateData, args=(module.module, ), daemon=True, name='data-update-%s' % module.module.__config__['name'])
        threads.append(th)

        print('$INFO$[Modules] Module {} loaded'.format(folder))
        modules.append(module.module.__config__)
    else:
        print('$INFO$[Modules] Failed to find module "{}"'.format(folder))

@app.route('/')
def index():
    global served_once
    # Take user to config page if not using the Electron client
    if request.user_agent.string.find('Electron') < 0:
        return redirect(url_for('config_page'))
    if not served_once:
        served_once = True
        response = make_response(render_template('index.html', modules=modules, filter=filter_by_pos))
        response.set_cookie('jwt', generate_token(365 * 24 * 60 * 60))
        return response
    else:
        abort(401)

@app.route('/config/')
@make_safe
def config_page():
    return render_template('config.html', modules=modules)

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.cookies.get('jwt', ''):
        return redirect('/')
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form.get('login-password') == settings.get('password', ''):
            response = redirect('/')
            response.set_cookie('jwt', generate_token())
        else:
            response = render_template('login.html', error=True)
        return response

@app.route('/<string:module>/<path:path>')
@make_safe
def serve_module_static(module, path):
    if not os.path.exists(os.path.join(*(['.', 'modules', module] + path.split('/')))):
        abort(404)
    return send_file(os.path.join(*(['.', 'modules', module] + path.split('/'))))

def filter_by_pos(modules, positions):
    filtered = modules
    for pos in positions:
        filtered = list(filter(lambda x: pos in x['pos'], filtered))
    return filtered
    
if __name__ == '__main__':
    for th in threads: th.start()
    app.run(threaded=True, debug=False, host='0.0.0.0', port=12306)