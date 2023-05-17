import json
from podcast_agent.client.podcast_api import PodcastApiClient

class PodcastApiService:
    """
    A class to interact with Podcast API via PodcastApiClient.
    """

    def __init__(self):
        """
        Initialize Podcast API service with PodcastApiClient.
        """
        self.client = PodcastApiClient()

    async def get_podcast(self, id: str, next_episode_pub_date: int, sort: str):
        """
        Fetch podcast by id using Podcast API.
        """
        try:
            response = await self.client.fetch_podcast_by_id(
                id=id,
                next_episode_pub_date=next_episode_pub_date,
                sort=sort,
            )
            return response
        except Exception as e:
            print(f"An error occurred while fetching podcast: {e}")

    async def get_episode(self, id: str, show_transcript: int):
        """
        Fetch episode by id using Podcast API.
        """
        try:
            response = await self.client.fetch_episode_by_id(
                id=id,
                show_transcript=show_transcript,
            )

            return response
        except Exception as e:
            print(f"An error occurred while fetching episode: {e}")
