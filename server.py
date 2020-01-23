from flask import Flask, request, render_template, send_file, abort, redirect, url_for
import os, importlib

app = Flask(__name__)

@app.route('/config/')
def config_page():
    return render_template('config.html', modules=modules.values())

modules = {}

# Import modules
for folder in os.listdir(os.path.join('.', 'modules')):
    # Is valid module
    if os.path.exists(os.path.join('.', 'modules', folder, 'module.py')):
        try:
            module = importlib.import_module('modules.{}.module'.format(folder))
        except:
            '$INFO$[Warning] Cannot import module {}'.format(folder)
            continue
        # Check if module.py file is valid
        try:
            assert 'config' in dir(module)
            assert folder == module.config.get('name', '')
            assert callable(module.config.get('renderer', '')) or module.config.get('renderer', '') == None

            if 'config' in module.config:
                assert callable(module.config.get('config', ''))
                app.add_url_rule('/config/{}'.format(folder), 'config-{}'.format(folder), module.config['config'])

            for view in module.config.get('views', ''):
                assert callable(view[2])
                assert 3 <= len(view) <= 4
                app.add_url_rule(*view[0:3], methods=['GET'] if len(view) == 3 else view[3])

        except AssertionError:
            print('$INFO$[Warning] Module.py file for module "{}" is invalid!'.format(folder))
            continue
            
        print('$INFO$[Modules] Module {} loaded'.format(folder))
        modules[folder] = module.config

@app.route('/')
def index():
    # Take user to config page if not using the Electron client
    if request.user_agent.string.find('Electron') < 0:
        return redirect(url_for('config_page'))
    return render_template('index.html', modules=modules.values(), filter=filter_by_pos)

@app.route('/<string:module>/<path:path>')
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