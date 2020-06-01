from flask import request, redirect
from functools import wraps
from .utils import settings, generate_token
import jwt, json, base64

def make_safe(view):
    @wraps(view)
    def secured_view(*args, **kwargs):
        token = request.cookies.get('jwt', '')
        try:
            jwt.decode(token, settings['secret'], algorithms='HS256')
            return view(*args, **kwargs)
        except jwt.InvalidTokenError:
            response = redirect('/login/')
            response.delete_cookie('jwt')
            return response

    return secured_view