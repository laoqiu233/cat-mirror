from ..helpers import moduleClass, renderFile
from ..middlewares import make_safe
from flask import request
import os, re, string, random

# Choose what language to use
# List of supported languages provided by Annyang:
# https://github.com/TalAter/annyang/blob/master/docs/FAQ.md#what-languages-are-supported
lang = 'en-US'

commands = {
    r'lights ((?:on)|(?:off))': lambda x,r: module.sendMessage('lights %s' % x.group(1)),
    r'show': lambda x,r: module.sendMessage('show'),
    r'hide': lambda x,r: module.sendMessage('hide'),
}

current_command_id = ''

# Could be used both as a decorator and a function
def addCommand(pattern, callback=None, flags=re.I):
    if (callback == None):
        def decorator(func):
            commands[re.compile(pattern, flags)] = func
        return decorator
    else:
        commands[re.compile(pattern, flags)] = callback

def configView():
    return renderFile(os.path.join('.', 'modules', 'voice', 'voice.html'), lang=lang)

@make_safe
def postCommand():
    command = request.data.decode('utf8')

    for pattern in commands:
        match = re.match(pattern, command.strip())
        print(pattern, command)
        if (match):
            current_command_id = ''.join([random.choice(string.hexdigits) for i in range(10)])
            def respond(msg):
                command_id = current_command_id
                if (current_command_id == command_id):
                    module.sendMessage('reply:' + msg)

            commands[pattern](match, respond)
            break

    return 'ok'

module = moduleClass('voice', renderer=lambda:'<h1>{{ voice.command }}</h1>', configView=configView)

module.setDefaultJson({'command': ''})

module.addView('/voice/command', 'module-voice-commands', postCommand, methods=['POST'])

module.addScript('voice.js')