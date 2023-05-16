import json
from podcast_agent.client.podcast_api import get_client

def get_podcast():
    client = get_client()

    response = client.fetch_podcast_by_id(
        id='4d3fe717742d4963a85562e9f84d8c79',
        next_episode_pub_date=1479154463000,
        sort='recent_first',
    )
    print(json.dumps(response.json()))
