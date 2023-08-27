# AutoLight

This is a work in progress tool to extract colors from the album cover of the currently playing Spotify track.
In the future, it will be used to control some DMX lights.

## Spotify Authentication

To communicate with Spotify, you need to create an app in the [developer dashboard](https://developer.spotify.com/dashboard/applications).
In the python project, create a file called `.env` and enter the following information from your Spotify app:
```
SPOTIPY_CLIENT_ID='xxx'
SPOTIPY_CLIENT_SECRET='xxx'
```

## Required Packages

```pip install python-dotenv mido opencv-python pillow spotipy python-rtmidi```
