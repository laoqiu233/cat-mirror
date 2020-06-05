from ..middlewares import make_safe
from ..helpers import moduleClass, renderFile, setInterval
from flask import request, redirect
import os, json, time, datetime

path = os.path.join('.', 'modules', 'clock')

# Default formats
formats = {
    'header': '%H:%M:%S',
    'subtitle': '%U, %m-%d'
}

# Get format or create config file
if (not os.path.exists(os.path.join(path, 'config.json'))):
    with open(os.path.join(path, 'config.json'), 'w') as f:
        json.dump(formats, f)
else:
    with open(os.path.join(path, 'config.json')) as f:
        formats = json.load(f)

@make_safe
def formatView():
    if (request.method == 'GET'):
        return json.dumps(formats)
    elif (request.method == 'POST'):
        formats['header'] = request.values['format-header']
        formats['subtitle'] = request.values['format-subtitle']

        module.sendJson(formats)

        with open(os.path.join(path, 'config.json'), 'w') as f:
            json.dump(formats, f)

        return redirect('/config/clock')

def configView():
    # Simply renders the config page
    return renderFile(os.path.join(path, 'config.html'), **formats)

module = moduleClass('clock', renderer=lambda: '<h1>{{ clock.header }}</h1><h2>{{ clock.subtitle }}</h2>', configView=configView)

module.addStyle('clock.css')

module.addView('/clock/format', 'clock-format', formatView, ['GET', 'POST'])

module.setDefaultJson({
    'header': 'header',
    'subtitle': 'subtitle'
})

@setInterval(1000)
def sendTime():
    module.sendJson({
        'header': datetime.datetime.now().strftime(formats['header']),
        'subtitle': datetime.datetime.now().strftime(formats['subtitle']),
    })