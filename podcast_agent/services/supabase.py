import json
from podcast_agent.client.supabase import SupabaseClient


class SupabaseService:
    """
    A class to interact with Supabase via SupabaseClient.
    """

    def __init__(self):
        """
        Initialize Supabase service with SupabaseClient.
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
            return json.dumps(response.json())
        except Exception as e:
            print(f"An error occurred while uploading file: {e}")
