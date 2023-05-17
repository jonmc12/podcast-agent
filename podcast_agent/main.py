from podcast_agent.services.supabase import SupabaseService
from services.podcast_api import PodcastApiService
from dotenv import load_dotenv

load_dotenv()

def main():
    # Podcast API example:
    # service = PodcastApiService()
    # service.get_podcast(
    #     id='4d3fe717742d4963a85562e9f84d8c79',
    #     next_episode_pub_date=1479154463000,
    #     sort='recent_first',
    # )

    # Supabase example:
    service = SupabaseService()
    service.upload_file(
        bucket_name='episode-audio-files',
        file_name='test.mp3',
    )

if __name__ == "__main__":
    main()
