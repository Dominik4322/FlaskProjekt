import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token():
    url = "https://id.twitch.tv/oauth2/token"

    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    return response.json()["access_token"]


def search_games(name):
    token = get_token()

    url = "https://api.igdb.com/v4/games"

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    body = f'''
    fields name, rating, first_release_date;
    search "{name}";
    limit 5;
    '''

    response = requests.post(url, headers=headers, data=body)
    return response.json()