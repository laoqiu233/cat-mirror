from ..helpers import moduleClass, setInterval, renderFile
from ..voice.module import addCommand
from urllib.parse import quote_plus
import requests, os

### Config ###
# Youre API key for newsapi.org
apikey = '' 
# 2-letter ISO 3166-1 code of the country
# Options: ae ar at au be bg br ca ch cn 
#          co cu cz de eg fr gb gr hk hu 
#          id ie il in it jp kr lt lv ma 
#          mx my ng nl no nz ph pl pt ro 
#          rs ru sa se sg si sk th tr tw 
#          ua us ve za
country = 'us'
# Category of the articles
# Options: business entertainment general 
#          health science sports technology
# Leave blank for all
category = ''
# Keywords or phrase to search for
keywords = ''

articles = []

def configView():
    return renderFile(os.path.join('.', 'modules', 'headlines', 'headlines.html'), articles=articles)

renderer = lambda: '''
<div v-if="headlines.articles.length">
<h3 style="font-size:2.5rem;">{{ headlines.articles[headlines.n].title.split('-').slice(0, -1).join('-') }}</h3>
<h4 style="color:#AAA;font-size:2rem;">{{ headlines.articles[headlines.n].source.name }} - {{ headlines.articles[headlines.n].publishedAt }}</h4>
</div>
<h3 v-else style='color:#AAA;font-size:2rem;'>No articles found...</h3>
'''

module = moduleClass('headlines', pos=['bottom', 'mid'], renderer=renderer, configView=configView)

module.addStyle('headlines.css')

module.addScript('headlines.js')

module.setDefaultJson({
    'articles': [],
    'n': 0
})

@setInterval(10 * 60 * 1000)
def getNews():
    global articles

    url = 'https://newsapi.org/v2/top-headlines?apiKey={}'.format(apikey)
    if (country): url += '&country=' + country
    if (category): url += '&category=' + category
    if (keywords): url += '&q=' + quote_plus(keywords)

    resp = requests.get(url).json()

    if (resp['status'] == 'ok'):
        articles = resp['articles']
        module.sendJson({
            'articles': articles,
            'n': 0
        })
    else:
        print('Failed to get new articles')

@addCommand(r'news description')
def newsDescription(match, respond):
    module.sendMessage('show news')
    respond('Showing it on the big screen right now!')

@addCommand(r'close news description')
def hideDescription(match, respond):
    module.sendMessage('hide news')
    respond('News hidden!')