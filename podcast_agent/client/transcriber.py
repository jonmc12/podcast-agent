class Transcriber:
    def __init__(self):
        import openai
        import os
        openai.api_key = os.environ['OPENAI_API_KEY']
    
    #TODO different path for large files
    #TODO read from cloud
    def read_from_url(self, url):
        #wrapper around openai whisper transcription service to read from 
        # given url and returns transcription
        #
        #url: location of audio file
        #returns: text transcription of file

        import openai
        import os

        if os.path.exists(url):
            transcript = self.local_file_to_transcription(open(url, "rb"))
        
        elif url.startswith('https://'):
            import tempfile
            if url.startswith('https://www.listennotes'):
                import requests
                audio_file = requests.get(url)

                with tempfile.NamedTemporaryFile(suffix='.mp3', mode='rb+', delete=True) as temp_file:
                    temp_file.write(audio_file.content)
                    temp_file_name = temp_file.name
                    temp_file.seek(0)
                    transcript = self.local_file_to_transcription(open(temp_file_name, 'rb'))

        return transcript

    def local_file_to_transcription(self, fileToTranscribe):
        #call openai transcription API on given file
        #
        #url: file like object
        #returns: text transcription of file
        import openai
        
        return  openai.Audio.transcribe("whisper-1", fileToTranscribe)
