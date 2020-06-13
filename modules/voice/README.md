# Voice Module
This module provides a web interface for voice control functionalities. Developers can easily add new commands with custom functions.

## Usage
Open the web interface for this module. Click start and say a command.

This module comes with some built-in commands:
* Lights *|ON|OFF|*  
Turns the background white/black
* Hide  
Hide every module
* Show  
Show every module

## For developers

Developing your own voice commands is pretty simple. First, you need to import the addCommand function:

```python
# /modules/myModule/module.py
from ..voice.module import addCommand
```

Then, you will need a command handler function, which takes two arguments, the regular expression match, and a respond function.

*regular expression match is a re.Match object*

```python
# /modules/myModule/module.py
from ..voice.module import addCommand

n = 0

def myCommandHandler(match, respond):
    n += 1
    # Use the respond function to display text on the web interface
    respond('This command has been called %s times, %s' %n, match.group(1))
```

Then, you will need a regular expression for your command, and bind it to your command handler

```python
# /modules/myModule/module.py
from ..voice.module import addCommand
import re

n = 0

# You can use the function as a decorator
# Flags argument defaults to re.I
@addCommand('Test command (.+)', flags=re.I|re.S)
def myCommandHandler(match, respond):
    n += 1
    # Use the respond function to display text on the web interface
    respond('This command has been called %s times, %s' %n, match.group(1))

#..or use it as a function
addCommand('Test command (.+)', callback=myCommandHandler, flags=re.I|re.S)
```