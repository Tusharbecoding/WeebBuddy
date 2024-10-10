import requests
import os

class MyAnimeListAPI:
    def __init__(self):
        self.base_url = "https://api.myanimelist.net/v2"
        self.headers = {
            "X-MAL-CLIENT-ID": os.getenv('MAL_CLIENT_ID')
        }

    def get_anime_recommendations(self, genre=None):
        # Adjust the genre filtering if needed
        url = f"{self.base_url}/anime?q={genre}&limit=5"
        print(f"Requesting URL: {url}")  # Log the URL

        response = requests.get(url, headers=self.headers)
        print(f"Response: {response.status_code}")  # Log the status code
        print(f"Response Content: {response.text}")  # Log the response content

        if response.status_code == 200:
            return response.json().get('data', [])
        return None
