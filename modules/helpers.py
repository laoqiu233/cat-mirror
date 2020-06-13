from flask import render_template_string
from functools import wraps
from .sockets import json_channel, msg_channel
import threading, time, json, string, random

class moduleClass():
    def __init__(self, name, pos=['bottom', 'left'], renderer=None, configView=None):
        self.__config__ = {
            'name': name,
            'pos': pos,
            'renderer': renderer,
            'configView': configView,
            'scripts': [],
            'styles': [],
            'views': [],
            'defaultJson': {}
        }

    def addView(self, route, endpoint, func, methods=['GET']):
        self.__config__['views'].append((route, endpoint, func, methods))

    def view(self, route, endpoint, methods=['GET']):
        def decorator(func):
            self.__config__['views'].append((route, endpoint, func, methods))
        return decorator
    
    def addScript(self, script):
        self.__config__['scripts'].append(script)

    def addStyle(self, style):
        self.__config__['styles'].append(style)

    def setDefaultJson(self, obj):
        self.__config__['defaultJson'] = json.dumps(obj)

    def sendJson(self, obj, send_to=None):
        if (send_to == None): send_to = self.__config__['name']
        json_channel.publish('id:{}\nevent:{}\ndata:{}\n\n'.format(generateId(), send_to, json.dumps(obj)))

    def sendMessage(self, msg, send_to=None):
        if (send_to == None): send_to = self.__config__['name']
        msg_channel.publish('id:{}\nevent:{}\ndata:{}\n\n'.format(generateId(), send_to, msg))

def generateId(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join([random.choice(chars) for i in range(size)])

def renderFile(path, status_code=200, **context):
    f = open(path)
    text = f.read()
    f.close()

    return render_template_string(text, **context), status_code

def setInterval(interval):
    def decorator(func):
        @wraps(func)
        def wrapped():
            try:
                while True:
                    func()
                    time.sleep(interval / 1000)
            except KeyboardInterrupt:
                pass

        th = threading.Thread(target=wrapped, daemon=True, name='interval-%s' % interval)
        th.start()
    
    return decorator