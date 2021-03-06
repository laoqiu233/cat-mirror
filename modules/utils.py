import json, base64, os, jwt, time

def load_settings():
    '''
    Loads user settings. Loads or generates a secret for JWT.
    '''
    settings = {}

    # Load User Settings
    with open('settings.json') as settings_file:
        settings = json.load(settings_file)

    # Load or Generate Secret for JWT
    try:
        with open('key') as key_file:
            # Load Secret
            settings['secret'] = base64.b64decode(key_file.read())
    except OSError:
        print('%INFO% No key file detected, generating a new secret.')
        with open('key', 'wb') as key_file:
            # Generate Secret
            settings['secret'] = os.urandom(64)
            key_file.write(base64.b64encode(settings['secret']))

    return settings

def generate_token(expiration=60*60*24):
    '''
    Generates a JWT token for authentication purposes to
    use across Cat-Mirror.
    '''
    # Default expiration is a day
    curr_time = int(time.time())
    secret = settings.get('secret', '')

    token = jwt.encode({
        'iss': 'cat-mirror',
        'iat': curr_time,
        'exp': curr_time + expiration # Cookie lives for a day 
    }, secret, algorithm='HS256')

    return token

settings = load_settings()