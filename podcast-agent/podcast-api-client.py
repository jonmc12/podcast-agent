import os
from listennotes import podcast_api

api_key = os.environ.get('LISTENNOTES_API_KEY')

client = podcast_api.Client(api_key=api_key)

response = client.search(q='star wars')

print(response.json())
