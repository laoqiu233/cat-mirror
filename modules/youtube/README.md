# Youtube Player Module
This module provides you with a YouTube iframe player that can be controlled by voice commandns from the web interface.

## Configuration
For the module to function and search for videos, you will need a Google API key.
1. First, go to the [Google Cloud API Platform console](https://console.cloud.google.com/) and create a new project, it can be named anything you want.  
2. Then, click on `APIs & Services` and `Enable APIs and Services`, search for `YouTube Data API v3`, enable this API.  
3. You will be taken the API overview page, click on `Credentials`, `Create credentials`, `API key`. After that, you will be prompted your API key. 
4. Copy and paste it into the `/modules/youtube/module.py` file on the line `api_key = ''` between the quotation marks. You can restrict the key if you want to.

## Usage

There are a few voice commands to control the YouTube player.

* YouTube search for *|SEARCH TERM|*  
Search for videos matching the term.
* YouTube search for *|VIDEOS|PLAYLISTS|CHANNELS|* *|SEARCH TERM|*  
Serach for tor the specified media type matching the search term.
* YouTube pause  
Pause the video
* YouTube play  
Resume the video
* YouTube stop  
Stop the video entirely
* YouTube next  
Skip to the next video in the playlist
* YouTube previous  
Play the previous video in the playlist