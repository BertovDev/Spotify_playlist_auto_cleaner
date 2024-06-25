import os
from dotenv import load_dotenv
from spotify_client import SpotifyClient
import requests
from urllib.parse import urlencode
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
playlist_url = os.getenv("PLAYLIST_URL")


def get_access_token_debug():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    auth_response = requests.post(url, headers=headers, data=data).json()
    access_token = auth_response["access_token"]
    return access_token


def get_access_token(auth_code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        },
        auth=(client_id, client_secret),
    )
    access_token = response.json()["access_token"]
    return access_token


@app.get("/")
async def auth():
    scope = ["playlist-modify-private", "playlist-modify-public"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={' '.join(scope)}"
    return HTMLResponse(content=f'<a href="{auth_url}">Authorize</a>')


@app.get("/callback")
async def callback(code):
    access_token = get_access_token(code)
    spotify_client = SpotifyClient(access_token, playlist_url)
    spotify_client.maybe_remove_playlist_items()


def debug():
    access_token = get_access_token_debug()
    spotify_client = SpotifyClient(access_token, playlist_url)
    spotify_client.maybe_remove_playlist_items()


if __name__ == "__main__":
    # uvicorn.run(app)
    debug()
