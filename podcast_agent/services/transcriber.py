import asyncio

import requests

from podcast_agent.client.transcriber import TranscriberClient
from podcast_agent.services.podcast_api import PodcastApiService
from podcast_agent.services.supabase import SupabaseService


class TranscriberService:
    """
    A class to interact with OpenAI Whisper via TranscriberClient.
    """

    def __init__(self):
        """
        Initialize Transcriber service with TranscriberClient.
        """
        self.client = TranscriberClient()

    def transcribe_from_file(self, file_name: str):
        """
        Transcribe a local file
        """
        return self.client.local_file_to_transcription(
            file_to_transcribe=open(file_name, "rb"),
        )

    def transcribe_from_url(self, url: str):
        """
        Transcribe an mp3 from a ListenNotes URL
        """
        return self.client.read_from_url(
            url=url,
        )

    def transcribe_and_upload(self):
        """
        Transcribe an mp3 from a ListenNotes URL and upload to Supabase
        """
        podcast_api_service = PodcastApiService()
        loop = asyncio.get_event_loop()
        # transcription = self.transcribe_from_url(url=url)
        episode_response = loop.run_until_complete(podcast_api_service.get_episode(
            id="87a935f22138437baa4b0a1043895e9b",
            show_transcript=1
        ))

        audio_url = episode_response["audio"]

        if episode_response["transcript"] is not None:
            transcription = episode_response["transcript"] 
        else:
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open("podcast.mp3", "wb") as file:
                    for chunk in audio_response.iter_content(chunk_size=1024):
                        file.write(chunk)
                print("Download completed.")
            else:
                print("Failed to download file.")

            supabase_service = SupabaseService()
            supabase_service.upload_file(
                bucket_name="episode-audio-files",
                file_name="podcast.mp3",
            )

            transcription = self.transcribe_from_file(file_name="podcast.mp3")

        return transcription


