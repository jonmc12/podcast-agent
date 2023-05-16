import os
from listennotes import podcast_api

def get_client():
    api_key = os.environ.get('LISTENNOTES_API_KEY')
    return podcast_api.Client(api_key=api_key)