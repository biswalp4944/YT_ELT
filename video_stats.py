import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # Load environment variables from .env file

API_KEY = os.getenv("API_KEY")
CHANNEL_Handle = "MrBeast" 
#print("API key loaded:", bool(API_KEY))
def  get_playlist_id():
    try:
      url= f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_Handle}&key={API_KEY}"

      response = requests.get(url)
      #print(response)
      response.raise_for_status()  # Raise an exception for HTTP errors
      json_data = response.json()
      #json_string = json.dumps(json_data, indent=4)
      #print(json_string)
      channel_items=json_data["items"][0]
      channel_playlist_id=channel_items['contentDetails']['relatedPlaylists']['uploads']
      print(channel_playlist_id)
      return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__":
    get_playlist_id()

