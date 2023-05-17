import os

import aiohttp

# from listennotes import podcast_api

class PodcastApiClient:
    """
    A class to interact with ListenNotes Podcast services.
    """
    BASE_URL = "https://listen-api.listennotes.com/api/v2"

    def __init__(self):
        """
        Initialize Podcast API client with environment variable.
        """
        try:
            self.api_key: str = os.environ['LISTENNOTES_API_KEY']
        except KeyError:
            raise ValueError("The LISTENNOTES_API_KEY environment variable must be set.")
        # self.client = podcast_api.Client(api_key=self.api_key)
        self.headers = {"X-ListenAPI-Key": self.api_key}
    
    async def fetch_podcast_by_id(
            self,
            id: str,
            next_episode_pub_date: int,
            sort: str
        ) -> dict:
        """
        Fetch podcast by id.
        """
        url = f"{self.BASE_URL}/podcasts/{id}"
        params = {'next_episode_pub_date': next_episode_pub_date}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=self.headers,
                params=params
            ) as response:
                return await response.json()
