import os
import tempfile
from typing import Any, BinaryIO, Union

import openai
import requests


class TranscriberClient:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("The OPENAI_API_KEY environment variable must be set.")

    def read_from_url(self, url: str) -> str:
        """
        Transcribe audio from a given URL.

        :param url: The URL of the audio file. Could be a local path or an HTTP URL.
        :return: The transcription of the audio file.
        """
        if os.path.exists(url):
            with open(url, "rb") as file:
                return self.local_file_to_transcription(file)

        elif url.startswith('https://'):
            response = requests.get(url)
            response.raise_for_status()  # if HTTPError is 4xx, 5xx

            with tempfile.NamedTemporaryFile(
                suffix='.mp3',
                mode='rb+',
                delete=True
            ) as temp_file:
                temp_file.write(response.content)
                temp_file.seek(0)
                return self.local_file_to_transcription(file_to_transcribe=temp_file)

        else:
            raise ValueError(f"Invalid URL: {url}")

    def local_file_to_transcription(
            self, 
            file_to_transcribe: Union[BinaryIO, Any]
        ) -> Union[str, Any]:
        """
        Transcribe a local audio file using the OpenAI API.

        :param file_to_transcribe: an audio file.
        :return: The transcription of the audio file or None if an error occurred.
        """
        try:
            return openai.Audio.transcribe("whisper-1", file_to_transcribe)
        except Exception as e:
            print(f"An error occurred while transcribing the audio: {e}")
            return None
