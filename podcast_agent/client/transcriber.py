import tempfile
import openai
import os
from pydub import AudioSegment

class Transcriber:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']
    
    #TODO different path for large files
    #TODO read from cloud
    #TODO error handling
    #       url is formatted for a local file but the file does not exist
    #       invalid file format
    #       network error for links to podcast audio eg 502 Bad gateway
    #       empty/corrupted file
    def read_from_url(self, url):
        #wrapper around openai whisper transcription service to read from 
        # given url and returns transcription
        #
        #url: location of audio file
        #returns: text transcription of file

        if os.path.exists(url):
            transcript = self.local_file_to_transcription(url)
        
        elif url.startswith('https://'):
            if url.startswith('https://www.listennotes'):
                import requests
                audio_file = requests.get(url)

                with tempfile.NamedTemporaryFile(suffix='.mp3', mode='rb+', delete=True) as temp_file:
                    temp_file.write(audio_file.content)
                    temp_file_name = temp_file.name
                    temp_file.seek(0)
                    transcript = self.local_file_to_transcription(temp_file.name)

        return transcript

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
