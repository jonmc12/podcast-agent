
import json
from podcast_agent.client.supabase import SupabaseClient


class SupabaseService:
    """
    A class to interact with Podcast API via PodcastApiClient.
    """

    def __init__(self):
        """
        Initialize Podcast API service with PodcastApiClient.
        """
        self.client = SupabaseClient()

    def upload_file(self, bucket_name: str, file_name: str):
        """
        Upload file to Supabase storage bucket
        """
        try:
            response = self.client.upload_file(
                bucket_name=bucket_name,
                file_name=file_name,
            )
            print(json.dumps(response.json()))
        except Exception as e:
            print(f"An error occurred while fetching podcast: {e}")
