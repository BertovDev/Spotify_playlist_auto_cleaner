import requests
from urllib.parse import urlparse
import json


TOTAL_ALLOWED_TIME_IN_SECODS = 10200  # 2hs 30min


class SpotifyClient:
    def __init__(self, access_token, playlist_url):
        self.access_token = access_token
        self.playlist_url = playlist_url

    def get_playlist(self):
        response = requests.get(
            self.playlist_url,
            headers={
                "Content-Type": "application/json",
                                "Authorization": f"Bearer {self.access_token}"
            }
        )
        response_json = response.json()
        return response_json

    def get_playlist_total_dutation(self, playlist):
        tracks = playlist['tracks']['items']
        total_time_seconds = sum(
            track["track"]["duration_ms"] for track in tracks)

        return total_time_seconds / 1000

    def maybe_remove_playlist_items(self):
        response_json = self.get_playlist()
        total_time = self.get_playlist_total_dutation(response_json)

        if (total_time > TOTAL_ALLOWED_TIME_IN_SECODS):
            time_diference = total_time - TOTAL_ALLOWED_TIME_IN_SECODS
            self.remove_track(response_json, time_diference)
        else:
            print("Time is already capped.")

    def remove_track(self, response_json, time_diference):
        tracks_uri = self.get_tracks_to_delete(response_json, time_diference)

        params = {
            "tracks": tracks_uri
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        remove_response = requests.delete(
            f"{self.playlist_url}/tracks", headers=headers, data=json.dumps(params, ensure_ascii=False))

        print(remove_response.text)
        print("Delete " + str(len(tracks_uri)) + " tracks")

    def get_tracks_to_delete(self, response_json, time_diference):
        tracks_uri = []
        tracks = response_json['tracks']['items']
        amount_to_delete = 0
        track_count = 0
        for i in range(len(tracks)):
            if amount_to_delete < time_diference:
                track = tracks[i]
                amount_to_delete += track["track"]["duration_ms"] / 1000
                track_count += 1
            else:
                break
        for i in range(track_count):
            tracks_uri.append({"uri": str(tracks[i]["track"]["uri"])})
        return tracks_uri
