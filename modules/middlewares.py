from flask import request, redirect
from functools import wraps
import jwt, json

secret = ''
with open('settings.json') as settings_file:
    settings = json.load(settings_file)
    secret = settings.get('secret', '')

def secure(view):
    @wraps(view)
    def secured_view(*args, **kwargs):
        token = request.cookies.get('jwt', '')
        try:
            payload = jwt.decode(token, secret, algorithms='HS256')
            return view(*args, **kwargs)
        except jwt.InvalidTokenError:
            response = redirect('/login/')
            response.delete_cookie('jwt')
            return response

    return secured_view