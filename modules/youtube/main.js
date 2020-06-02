function onYouTubeIframeAPIReady() {
    let player = new YT.Player('player', {
        height: '360',
        width: '640'
    });

    // Put your google api key here
    const api_key = '';

    function cueVideo(id) {
        player.loadVideoById(id);
    }

    function cueChannel(id) {
        fetch(`https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id=${id}&key=${api_key}`)
        .then((data) => data.json())
        .then((results) => {
            cuePlaylist(results.items[0].contentDetails.relatedPlaylists.uploads);
        });
    }

    function cuePlaylist(id) {
        fetch(`https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId=${id}&maxResults=50&key=${api_key}`)
        .then((data) => data.json())
        .then((results) => {
            player.loadPlaylist(results.items.map((x) => x.contentDetails.videoId));
        });
    }

    function search(searchTerm, mediaType) {
        return fetch (`https://www.googleapis.com/youtube/v3/search?part=id,snippet&q=${encodeURI(searchTerm)}&type=${mediaType}&key=${api_key}`)
        .then((data) => data.json())
        .then((results) => {
            if (results.items) {
                return results.items[0];
            } else {
                return null;
            }
        });
    }

    if (voice_module_commands) {
        voice_module_commands['/Youtube search for (?:((?:video)|(?:channel)|(?:playlist))s? )?(.+)/i'] = async (match, r) => {
            let mediaType = match[1] ? match[1] : 'video';
            let result = await search(match[2], mediaType.toLowerCase());
            if (result) {
                switch (mediaType.toLowerCase()) {
                    case 'video':
                        cueVideo(result.id.videoId);
                        r(`Playing video "${result.snippet.title}"`);
                        break;
                    case 'playlist':
                        cuePlaylist(result.id.playlistId);
                        r(`Playing playlist "${result.snippet.title}"`);
                        break;
                    case 'channel':
                        cueChannel(result.id.channelId);
                        r(`Playing videos on the channel "${result.snippet.title}"`);
                        break;
                }
            } else {
                r(`No results found based on the search term "${match[2]}"`);
            }
        }

        voice_module_commands['/Youtube pause/i'] = (match, r) => {
            player.pauseVideo();
            r('Video Paused.');
        }

        voice_module_commands['/Youtube play/i'] = (match, r) => {
            player.playVideo();
            r('Video Resumed.');
        }

        voice_module_commands['/Youtube stop/i'] = (match) => {
            player.stopVideo();
        }

        voice_module_commands['/Youtube next/i'] = (match) => {
            player.nextVideo();
        }

        voice_module_commands['/Youtube previous/i'] = (match) => {
            player.previousVideo();
        }
    }
}