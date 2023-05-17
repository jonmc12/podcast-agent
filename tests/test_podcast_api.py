import pytest
from podcast_agent.services.podcast_api import PodcastApiService

class TestPodcastApiService:
    @pytest.mark.asyncio
    async def test_get_podcast(self):
        service = PodcastApiService()
        result = await service.get_podcast(
            id='4d3fe717742d4963a85562e9f84d8c79',
            next_episode_pub_date=1479154463000,
            sort='recent_first',
        )
        assert result is not None
        # Add more assertions based on expected result
