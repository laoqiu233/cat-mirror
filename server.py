from flask import Flask, request, render_template, send_file, abort, redirect, url_for, make_response
from modules.middlewares import secure
import os, importlib, jwt, time, json

settings = {}

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

def generate_token(expiration=60*60*24):
    # Default expiration is a day
    curr_time = int(time.time())
    secret = settings.get('secret', '')

    token = jwt.encode({
        'iss': 'cat-mirror',
        'iat': curr_time,
        'exp': curr_time + expiration # Cookie lives for a day 
    }, secret, algorithm='HS256')

    return token

def add_module_view(url, endpoint, handler, methods=['GET'], secure_view=False):
    print(url, methods)
    if secure:
        app.add_url_rule(url, endpoint, secure(handler), methods=methods)
    else:
        app.add_url_rule(url, endpoint, handler, methods=methods)

app = Flask(__name__)

modules = []
to_load = [
    'voice',
    'clock',
    'headlines',
    'weather',
]
served = False

# Import modules
for folder in to_load:
    # Is valid module
    if os.path.exists(os.path.join('.', 'modules', folder, 'module.py')):
        try:
            module = importlib.import_module('modules.{}.module'.format(folder))
        except:
            print('$INFO$[Warning] Cannot import module "{}"'.format(folder))
            continue
        # Check if module.py file is valid
        try:
            assert 'config' in dir(module)
            assert folder == module.config.get('name', '')
            assert callable(module.config.get('renderer', '')) or module.config.get('renderer', '') == None

            if 'config' in module.config:
                assert callable(module.config.get('config', ''))
                add_module_view('/config/{}'.format(folder), 'config-{}'.format(folder), module.config['config'], secure_view=True)

            for view in module.config.get('views', ''):
                assert callable(view[2])
                assert 3 <= len(view) <= 5
                add_module_view(*view)

        except AssertionError:
            print('$INFO$[Warning] Module.py file for module "{}" is invalid!'.format(folder))
            continue
            
        print('$INFO$[Modules] Module {} loaded'.format(folder))
        modules.append(module.config)
    else:
        print('$INFO$[Modules] Failed to find module "{}"'.format(folder))

@app.route('/')
def index():
    global served
    # Take user to config page if not using the Electron client
    if request.user_agent.string.find('Electron') < 0:
        return redirect(url_for('config_page'))
    if not served:
        served = True
        response = make_response(render_template('index.html', modules=modules, filter=filter_by_pos))
        response.set_cookie('jwt', generate_token(365 * 24 * 60 * 60))
        return response
    else:
        abort(401)

@app.route('/config/')
@secure
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
@secure
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
    app.run(debug=False, host='0.0.0.0', port=12306)