import requests
import json
from datetime import date
# import os
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="./.env")  # Load environment variables from .env file
from airflow.decorators import task
from airflow.models import Variable
API_KEY = Variable.get("API_KEY")
CHANNEL_Handle = Variable.get("CHANNEL_Handle")
maxResults = 50  # Maximum number of results to retrieve per API call
@task
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
      #print(channel_playlist_id)
      return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e
@task
def get_video_ids(playlist_id):
    video_ids = []
    page_token = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            url=base_url
            if page_token:
                url += f"&pageToken={page_token}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            json_data = response.json()
            for item in json_data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            page_token = json_data.get("nextPageToken")
            if not page_token:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e
@task
def extract_video_data(video_id):
    extracted_data =[]

    def batch_list(Video_id_list,batch_size):
        for video_id in range(0, len(Video_id_list), batch_size):
            yield Video_id_list[video_id:video_id + batch_size]
    
    try:
        for batch in batch_list(video_id, maxResults):
            video_ids_str=",".join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            json_data = response.json()
            for item in json_data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                statistics = item['statistics']
                content_details = item['contentDetails']
                video_data = {
                    'video_id': video_id,
                    'title': snippet.get('title'),
                    'description': snippet.get('description'),
                    'published_at': snippet.get('publishedAt'),
                    'view_count': statistics.get('viewCount',None),
                    'like_count': statistics.get('likeCount',None),
                    'comment_count': statistics.get('commentCount',None),
                    'duration': content_details.get('duration')
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e
@task
def save_to_json(extracted_data):
     file_path =f"./data/YT_api_data_{date.today()}.json"

     with open(file_path, 'w',encoding='utf-8') as json_outfile:
            json.dump(extracted_data, json_outfile, indent=4,ensure_ascii=False)
if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
