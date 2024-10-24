# AutoLight

This is a work in progress tool to extract colors from the album cover of the currently playing Spotify track to control some party lights.

If the song changes, the tool generates two new colors and sends out two midi signal depending on the colors. In combination with [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) you can forward these midi signals to trigger scenes in [Daslight](https://www.daslight.com/) to control some DMX-lights. It may be possible to use other DMX softwares, too.

## Spotify Authentication

To communicate with Spotify, you need to create an app in the [developer dashboard](https://developer.spotify.com/dashboard/applications).
In the python project, create a file called `.env` and enter the following information from your Spotify app:

```
SPOTIPY_CLIENT_ID='xxx'
SPOTIPY_CLIENT_SECRET='xxx'
```

## Future Plans

- Add real-time BPM detection and midi clock support
- Add track intensity detection to trigger different dimmer curves or movement patterns
- Add build-up and drop detection to trigger flash scenes
