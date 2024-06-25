## Spotify playlist auto cleaner

### This app enable you to maintain you playlist cap to a certain duration.

### How to use it

- Start the enviroment ```. .venv/bin/activate```
- Add ```.env``` with you credentials
  -   ```CLIENT_ID = ""```
  -   ```CLIENT_SECRET = ""```
  -   ```REDIRECT_URI = ""```
  -   ```PLAYLIST_URL = ""```
- Set the var ```TOTAL_ALLOWED_TIME_IN_SECODS``` with the amount of time to cap the playlist in seconds 
- Run ```python run.py```. go to the url, authorize the spotify app and copy the code in the URL
- Go to ```http://127.0.0.1:8000/callback?code=``` and paste the code.
- The playlist will delete the amount of tracks necessary to archive the amount of time.


Build this to auto cap my gym playlist to 2hs30min the maximun time of my training session. xD
https://open.spotify.com/playlist/1XyzbkDY4mQrJsEN9L64dm
