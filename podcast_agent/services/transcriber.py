from podcast_agent.client.transcriber import TranscriberClient


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
