# Cat-Mirror🐈
## Modular Smart Mirror System written using Flask + Electron

## Pre-requirements:
- Python3 🐍
- NPM + Node.JS ☕

## Installation
    npm install
    pip install -r requirements.txt

## Usage
Simply type `npm start` to boot the mirror.

## Configuration for Web Interface
*This only works on Chrome because other browsers like FireFox are more strict about the security of the source*
### Treat Mirror IP address as a Secure Source
For the full functionality of the mirror, you need to treat the web interface as
a secure source, because most browsers nowadays will disable many powerful functionalities
on insecure HTTP sources.  
And because Cat-Mirror is intended to run on a local network with access only through the IP
address, it's not possible to get a certificate and use HTTPs, thus we need to tell the browser
to treat the Mirror's IP address as a secure source.   
Before you proceed, just know that **Cat-Mirror and it's built-in modules will not in any way collect your data for any purposes**.
### Steps
- On Chrome, type `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in the address bar.
- Enable the highlighted flag.
- Type your mirror's IP address, e.g. `http//192.168.0.100:12306`.  
**Note** It is recommended to configure a static IP address on the router for the mirror.
- Restart your browser.
### PWA
There is a manifest.json file written for Cat-Mirror, but since we can't use HTTPs for the mirror,
we can't have a proper PWA. But on Chrome, you can choose to `add to home screen` in the menu. It
will have a icon, splash screen, and function almost like an actual PWA.

## TODO:
- [x] Make a config navigation page for all modules.  
- [x] Write weather module  
- [ ] Reduce the amount of front-end css code  
- [x] News module  
- [x] PWA for Chrome (?)
- [ ] Voice Control
    - [ ] Basic module for testing
    - [ ] Interface for other modules 