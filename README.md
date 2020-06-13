# Cat-Mirror - REMASTERED🐈
## Modular Smart Mirror System written using Flask + Electron
**🚧THIS IS A WORK IN PROGRESS🚧**

## About

Cat-Mirror is a modular smart mirror system written in Python and Node.js. It allows users to easily create the module they want for their smart mirror.

Cat-Mirror uses Flask, Electron and Vue.js to make the process of creating a module as simple as possible.

## Pre-Requirements

🐍 Python  
☕ Node.js

## Installation

1. Clone the repository using the command `git clone https://github.com/laoqiu233/cat-mirror.git`
2. Cd into the folder `cd cat-mirror` 
3. Install the required libraries  
```
pip install -r requirements.txt
npm install
```

## Usage
Simply type `npm start` to start the mirror.

To use the web interface, type `http://*mirror-host-ip-address*:12306/` into your browser's address bar.

For server only mode, see [this](#server-only-mode).

**BUT**, Before starting, you will need to setup some modules, because they use a 3rd party API

### Headlines module
First, you need to create an account on the [news api website](https://newsapi.org/). You can use a developer subscription plan.

Then, enter your account page, copy your api key, then open the `/modules/headlines/module.py` file and paste it on the line `apikey = ''` between the quotation marks.

After that, you can further customize what kind of articles you want to see on your mirror. Read the comments in the `module.py` file to learn more.

### Weather module
First, register on [Weatherbit.io](https://www.weatherbit.io/) to get an API key, you can use the free subscription plan.   
Then open the `/modules/weather/module.py` file with a text editor, copy and paste your API key on to the line `key = ''` between the quotation marks.  
You can further specify the city and units by changing other variables, read the comments in the `module.py` file to learn more.

### YouTube player module
For the module to function and search for videos, you will need a Google API key.
1. First, go to the [Google Cloud API Platform console](https://console.cloud.google.com/) and create a new project, it can be named anything you want.  
2. Then, click on `APIs & Services` and `Enable APIs and Services`, search for `YouTube Data API v3`, enable this API.  
3. You will be taken the API overview page, click on `Credentials`, `Create credentials`, `API key`. After that, you will be prompted your API key. 
4. Copy and paste it into the `/modules/youtube/module.py` file on the line `api_key = ''` between the quotation marks. You can restrict the key if you want to.

## Configuration for Web Interface
### Set a Password
Open the `settings.json` file and just change the password field.

### Download Vue.js
To avoid putting the whole Vue.js framework in this repo, a CDN is used to load Vue.js currently. To improve the speed of loading, you can [download Vue.js](https://vuejs.org/js/vue.js) to load it locally.  
To download, open the link, right click on page, and click `Save as...`. Save the file to the `/static` folder.
After that, the following files need to be modified a little bit:
* `/templates/index.html`
* `/modules/clock/clock.html`

All you have to do, is find these two lines:
```html
<!-- <script src="{{ url_for('static', filename='vue.js') }}"></script> -->
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.11"></script>
```
...and replace them with:
```html
<script src="{{ url_for('static', filename='vue.js') }}"></script>
```
*The following only works on Chrome because other browsers like FireFox are more strict about the security of the source*
### Treat Mirror IP address as a Secure Source
For the full functionality of the mirror, you need to treat the web interface as
a secure source, because most browsers nowadays will disable many powerful functionalities
on insecure HTTP sources.  
And because Cat-Mirror is intended to run on a local network with access only through the IP
address, it's not possible to get a certificate and use HTTPs, thus we need to tell the browser
to treat the Mirror's IP address as a secure source.   
Before you proceed, just know that **Cat-Mirror and it's built-in modules will not in any way collect your data for any purposes**.
### Steps
- In Chrome, type `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in the address bar.
- Enable the highlighted flag.
- Type your mirror's IP address, e.g. `http//192.168.0.100:12306`.  
**Note** It is recommended to configure a static IP address on the router for the mirror.
- Restart your browser.
### PWA
There is a manifest.json file written for Cat-Mirror, but since we can't use HTTPs for the mirror,
we can't have a proper PWA. But on Chrome, you can choose to `add to home screen` in the menu. It
will have a icon, splash screen, and function almost like an actual PWA.

## Server Only Mode
In certain cases where electron doesn't work, you will need to use server-only mode and open up a browser window in full screen mode.

Type `python server.py` to start in server only mode. Then type `localhost:12306` in the browser's address bar.

## TODO:
- [X] Create web socket interface for front-end and back-end communication.

- [X] Rewrite old modules
    - [X] Voice control
    - [X] Headlines
    - [X] Weather
    - [X] Youtube player

- [ ] Documentations
    - [X] Module specific documentations
        - [X] Clock
        - [X] Headlines
        - [X] Weather
        - [X] Youtube
        - [X] Voice
    - [X] Readme.md
    - [ ] Developer's Guide