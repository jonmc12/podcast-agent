import os
import tempfile
from typing import Any, BinaryIO, Union
from pydub import AudioSegment

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
            # with open(url, "rb") as file:
            #     return self.local_file_to_transcription(file)
            transcript = self.local_file_to_transcription(url)
        
        elif url.startswith('https://'):
            response = requests.get(url)
            response.raise_for_status()  # if HTTPError is 4xx, 5xx

            # with tempfile.NamedTemporaryFile(
            #     suffix='.mp3',
            #     mode='rb+',
            #     delete=True
            # ) as temp_file:
            #     temp_file.write(response.content)
            #     temp_file.seek(0)
            #     return self.local_file_to_transcription(file_to_transcribe=temp_file)
            with tempfile.NamedTemporaryFile(suffix='.mp3', mode='rb+', delete=True) as temp_file:
                temp_file.write(audio_file.content)
                temp_file_name = temp_file.name
                temp_file.seek(0)
                transcript = self.local_file_to_transcription(url)

        else:
            raise ValueError(f"Invalid URL: {url}")

    # def local_file_to_transcription(
    #         self, 
    #         file_to_transcribe: Union[BinaryIO, Any]
    #     ) -> Union[str, Any]:
    #     """
    #     Transcribe a local audio file using the OpenAI API.

    #     :param file_to_transcribe: an audio file.
    #     :return: The transcription of the audio file or None if an error occurred.
    #     """
    #     try:
    #         return openai.Audio.transcribe("whisper-1", file_to_transcribe)
    #     except Exception as e:
    #         print(f"An error occurred while transcribing the audio: {e}")
    #         return None
        
    def get_segments(self, L, mSS):
        return [L[i:(i + 1)*mSS] for i in range(len(L)//mSS) + 1]


    def local_file_to_transcription(self, path_to_file_to_transcribe):
        #call openai transcription API on given file
        #
        #path_to_file_to_transcribe: path to a file
        #returns: text transcription of file
        import os
        
        if not os.path.isfile(path_to_file_to_transcribe):
            raise FileNotFoundError(f'[Errno 2] no such file {path_to_file_to_transcribe}')

        audio = AudioSegment.from_mp3(path_to_file_to_transcribe)
        prefix = path_to_file_to_transcribe.replace('.mp3', '')
        mSS = 6*(10**4)

        num_segments = 1 + (len(audio)//mSS)

        for i in range(num_segments):
            audio[i:(i + 1)*mSS].export(prefix + f'_{i}.mp3')  
        
        out = []

        for i in range(num_segments):
            transcript = openai.Audio.transcribe("whisper-1", open(prefix + f'_{i}.mp3', 'rb'))
            os.remove(prefix + f'_{i}.mp3')
            out.append(transcript.text)
        
        return ''.join(out)
