import os
from typing import Any
from listennotes import podcast_api

class PodcastApiClient:
    """
    A class to interact with ListenNotes Podcast services.
    """

    def __init__(self):
        """
        Initialize Podcast API client with environment variable.
        """
        try:
            self.api_key: str = os.environ['LISTENNOTES_API_KEY']
        except KeyError:
            raise ValueError("The LISTENNOTES_API_KEY environment variable must be set.")
        self.client = podcast_api.Client(api_key=self.api_key)

    def get_client(self) -> podcast_api.Client:
        """
        Get the Podcast API client.
        """
        return self.client
    
    def fetch_podcast_by_id(
            self, id: str, next_episode_pub_date: int, sort: str
        ) -> Any:
        """
        Fetch podcast by id.
        """
        return self.client.fetch_podcast_by_id(
            id=id, 
            next_episode_pub_date=next_episode_pub_date, sort=sort
        )
