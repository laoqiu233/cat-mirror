var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '360',
        width: '640',
    });

    setMessageSocketHandler('youtube', function(msg) {
        if (msg.startsWith('VIDEO')) {
            player.loadVideoById(msg.slice(5));
        } else if (msg.startsWith('PLAYLIST')) {
            player.loadPlaylist(msg.slice(8).split(','));
        } else {
            switch (msg) {
                case 'PAUSE':
                    player.pauseVideo();
                    break;
                case 'PLAY':
                    player.playVideo();
                    break;
                case 'STOP':
                    player.stopVideo();
                    break;
                case 'NEXT':
                    player.nextVideo();
                    break;
                case 'PREVIOUS':
                    player.previousVideo();
                    break;
            }
        }
    });
}