import pytest
from podcast_agent.services.transcriber import TranscriberService

class TestTranscriberService:
    def test_transcribe_from_file(self):
        service = TranscriberService()
        transcript = service.transcribe_from_file(file_name='test.mp3')
        assert transcript is not None
        # Add more assertions based on expected transcript content
