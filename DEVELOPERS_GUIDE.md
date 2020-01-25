# Guide for Module Development 😺
## File Structure
Your module should be a folder which includes a module.py file and 
everything else your module needs in order to work

**Example:**
- *ModuleName*
    - module.py
    - main.js # *Just a js file for the frontend*
    - others.py # *More python stuff*
    - main.css # *Front-end Styling*
## **module.py**
Your *module.py* file should include a dictionary named *config* which
contains everything about the module itself, including the static files 
renderer function, config page view function and etc.

**Example:**
```python
from flask import jsonify, request

def renderer():
    return '<h1>This is example HTML code for the module</h1>'

def custom_view():
    if request.method == 'GET':
        return 'Something'
    elif request.method == 'POST':
        # Do something
        return 'Success!'

config = {
    'name': 'ModuleName', # Should be the same as the folder's name
    'renderer': renderer, # A function that returns raw html code
    'pos': ['top', 'left'], # The position in which the module will be rendered
    'styles': ['styles.css'], # Static css files that the module require
    'scripts': ['main.js'], # Static js files that the module require
    'views': [('/clock/format', 'clock-format', change_format, ['GET', 'POST'])], # Custom views
    # A custom view should be a tuple with the following format:
    # (View route, View end-point, View function, The methods this view supports(Optional))
    # View route should follow the format of /*module name*/*route*
    'config': lambda: 'Testing' # The config page, route is automatically set to /config/*module name*
}
```

# Notes for Developers
## CSS
When writing CSS styles, remember to add `#module-*ModuleName*` before every one of your selectors to avoid conflicts between diffrent modules.
Since modules are warpped inside a *div* element with an id of `#module-*ModuleName*`.

## Developer tools
If you need developer tools for debugging purposes, comment out the line `Menu.setApplicationMenu(null)` in 
`main.js`, then press `Shift + Ctrl + I` to open developer tools.


# Fin.
 And that's basically it! Now you can code your own module for your customized cat-mirror experience.