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
            path_to_file_to_transcribe=file_name,
        )

    def transcribe_from_url(self, url: str):
        """
        Transcribe an mp3 from a ListenNotes URL
        """
        return self.client.read_from_url(
            url=url,
        )

    def download_podcast(self, audio_url: str, filename: str) -> bool:
        """
        Download a podcast episode.
        """
        audio_response = requests.get(audio_url)
        if audio_response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in audio_response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print("Download from Podcast API completed.")
            return True
        else:
            print("Failed to download file.")
            return False

    def transcribe_and_upload(self, episode_id: str):
        """
        Transcribe an mp3 from a ListenNotes URL and upload to Supabase
        """
        podcast_api_service = PodcastApiService()
        supabase_service = SupabaseService()
        loop = asyncio.get_event_loop()
        episode_response = loop.run_until_complete(podcast_api_service.get_episode(
            id=episode_id,
            show_transcript=1
        ))

        audio_url = episode_response["audio"]
        audio_filename = f"podcast_{episode_id}.mp3"
        transcription_filename = f"podcast_transcript_{episode_id}.txt"

        if episode_response["transcript"] is not None:
            transcription = episode_response["transcript"] 
        else:
            if self.download_podcast(audio_url, audio_filename):
                audio_file_response = supabase_service.upload_file(
                    bucket_name="episode-audio-files",
                    file_name=audio_filename,
                )

                print(f"Upload to Supabase completed: {audio_file_response}")

                transcription = self.transcribe_from_file(file_name=audio_filename)
                print(f"Transcription completed: {len(transcription)} characters")
            else:
                print("Failed to transcribe the episode.")
                return None

        with open(transcription_filename, "w") as file:
            file.write(transcription)

        episode_transcription_response = supabase_service.upload_file(
            bucket_name="episode-transcriptions",
            file_name=transcription_filename,
        )
        print(f"Upload to Supabase completed: {episode_transcription_response}")

        return len(transcription)
