from flask import jsonify, Response, request, render_template_string
import os, json

def news():
    if request.method == 'POST':
        with open(os.path.join('.', 'modules', 'headlines', 'news.json'), 'w', encoding='utf-8') as file:
            json.dump(request.json, file)
        return 'ok'

def getConfig():
    return jsonify({
        'key': config['key'],
        'country': config['country']
    })

def config_view():
    template = ''
    news = None
    with open(os.path.join('.', 'modules', 'headlines', 'config.html'), encoding='utf-8') as file:
        template = file.read()
    with open(os.path.join('.', 'modules', 'headlines', 'news.json'), encoding='utf-8') as file:
        news = json.load(file)
    
    return render_template_string(template, articles=news)
    

config = {
    'key': '',
    'country': 'us', # 2-letter ISO 3166-1 code
    'name': 'headlines',
    'renderer': None,
    'pos': ['bottom', 'mid'],
    'views': [('/headlines/config', 'headlines-config', getConfig),
              ('/headlines/news', 'headlines-news', news, ['POST'])],
    'scripts': ['main.js'],
    'styles': ['styles.css'],
    'config': config_view
}