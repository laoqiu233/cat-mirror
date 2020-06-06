from ..helpers import moduleClass, setInterval
import requests

# Your weatherbit.io key
key = ''
# Put your city name here
# Leave empty for the module to determine on its own
city = ''
# Measuring units
# M - [DEFAULT] Metric (Celcius, m/s, mm)
# S - Scientific (Kelvin, m/s, mm)
# I - Fahrenheit (F, mph, in)
units = 'M'

units_text = {
    'M': '°C',
    'S': 'K',
    'I': '°F'
}

if (not city): 
    resp = requests.get('http://ip-api.com/json').json()
    if (resp['status'] == 'success'):
        city = resp['city']
    else:
        print('$INFO$[WEATHER] Failed to determine location, defaults to Montreal')
        city = 'Montreal'

renderer = lambda: ('''
    <div v-if="weather.data.length">
        <div class="current-weather">
            <img :src="`https://www.weatherbit.io/static/img/icons/${{weather.data[0].weather.icon}}.png`" style="width:12rem;">
            <h1>{{{{ weather.data[0].temp }}}}{unit_text}</h1>
        </div>
        <h3>Weather forecast for {{{{ weather.city }}}}</h3>
        <table>
            <tr v-for="data, index in weather.data.slice(1)">
                <td><img :src="`https://www.weatherbit.io/static/img/icons/${{data.weather.icon}}.png`" style="width:3.5rem"></td>
                <td v-if="index < 3">{{{{ ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][(new Date().getDay() + index + 1) % 7] }}}}</td>
                <td v-else>{{{{ data.valid_date.split('-').slice(1).join('-') }}}}</td>
                <td>{{{{ data.max_temp }}}}{unit_text}</td>
                <td>{{{{ data.min_temp }}}}{unit_text}</td>
            </tr>
        </table>
    </div>
'''.format(unit_text=units_text[units]))

module = moduleClass('weather', ['top', 'left'], renderer)

module.addStyle('widget.css')

module.setDefaultJson({
    'data': [],
    'city': city
})

@setInterval(30 * 60 * 1000)
def getForecast():
    resp = requests.get('https://api.weatherbit.io/v2.0/forecast/daily?city={}&key={}&units={}&days=6'.format(
        city,
        key,
        units
    )).json()

    module.sendJson({
        'data': resp['data'],
        'city': city
    })