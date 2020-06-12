from ..helpers import moduleClass
from ..voice.module import addCommand
import requests, json

# Your google API key
api_key = ''

renderer = lambda: '<div id="player"></div>' 

module = moduleClass('youtube', ['top', 'left'], renderer=renderer)

module.addScript('youtube.js')
module.addScript('https://www.youtube.com/iframe_api')
module.addStyle('youtube.css')

def getPlaylistItems(playlist_id):
    results = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', {
        'part': 'snippet',
        'playlistId': playlist_id,
        'key': api_key
    }).json()

    # Get array of video ids in playlist
    return [item['snippet']['resourceId']['videoId'] for item in results['items']]

@addCommand(r'Youtube search for (?:((?:video)|(?:channel)|(?:playlist))s? )?(.+)')
def searchCommand(match, respond):
    # Get media type
    media_type = (match.group(1).lower() if match.group(1) else 'video')

    # Get results for media type
    results = requests.get('https://www.googleapis.com/youtube/v3/search', {
        'part': 'id,snippet',
        'q': match.group(2),
        'type': media_type,
        'key': api_key
    }).json()['items']

    if (results):
        # Send message based on media type
        if (media_type == 'video'):
            respond('Playing video "{}"'.format(results[0]['snippet']['title']))
            module.sendMessage('VIDEO' + results[0]['id']['videoId'])
        elif (media_type == 'channel'):
            # Get channel uploads playlist
            channel_playlist = requests.get('https://www.googleapis.com/youtube/v3/channels', {
                'part': 'contentDetails',
                'id': results[0]['id']['channelId'],
                'key': api_key
            }).json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            respond('Playing videos on channel "{}"'.format(results[0]['snippet']['title']))
            module.sendMessage('PLAYLIST' + ','.join(getPlaylistItems(channel_playlist)))
        elif (media_type == 'playlist'):
            respond('Playing videos from playlist "{}"'.format(results[0]['snippet']['title']))
            module.sendMessage('PLAYLIST' + ','.join(getPlaylistItems(results[0]['id']['playlistId'])))
    else:
        respond('Nothing found based on the search term "{}"'.format(match.group(2)))

# Playback control commands

@addCommand(r'Youtube pause')
def pauseCommand(match, respond):
    module.sendMessage('PAUSE')
    respond('Video paused')

@addCommand(r'Youtube play')
def playCommand(match, respond):
    module.sendMessage('PLAY')
    respond('Video resumed')

@addCommand(r'Youtube stop')
def stopCommand(match, respond):
    module.sendMessage('STOP')
    respond('Video stopped')

@addCommand(r'Youtube next')
def nextCommand(match, respond):
    module.sendMessage('NEXT')
    respond('Video skipped')

@addCommand(r'Youtube previous')
def previousCommand(match, respond):
    module.sendMessage('PREVIOUS')
    respond('Playing the previous video')