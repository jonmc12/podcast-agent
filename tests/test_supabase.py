import pytest
import unittest.mock
from podcast_agent.services.supabase import SupabaseService

class TestSupabaseService:
    @pytest.fixture
    def mock_upload_file(self):
        with unittest.mock.patch(
            'podcast_agent.services.supabase.SupabaseService.upload_file', 
            new_callable=unittest.mock.MagicMock
        ) as _mock:
            yield _mock

    def test_upload_file(self, mock_upload_file):
        mock_upload_file.return_value = True 

        service = SupabaseService()
        
        result = service.upload_file(
            bucket_name='episode-audio-files',
            file_name='test.mp3'
        )
        
        mock_upload_file.assert_called_once_with(
            bucket_name='episode-audio-files',
            file_name='test.mp3'
        )
        assert result is not None
