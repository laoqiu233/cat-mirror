from flask import render_template_string
from queue import Queue
from functools import wraps
import threading, time, json

class moduleClass():

    __config__ = {
        'views': [],
        'scripts': [],
        'styles': [],
        'defaultJson': {}
    }

    jsonQueue = Queue()
    messageQueue = Queue()

    def __init__(self, name, pos=['bottom', 'left'], renderer=None, configView=None):
        self.__config__['name'] = name
        self.__config__['pos'] = pos
        self.__config__['renderer'] = renderer
        self.__config__['configView'] = configView

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

    def sendJson(self, obj):
        self.jsonQueue.put('event:{}\ndata:{}\n\n'.format(self.__config__['name'], json.dumps(obj)))

    def sendMessage(self, msg):
        self.messageQueue.put('event:{}\ndata:{}\n\n'.format(self.__config__['name'], msg))

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