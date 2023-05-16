class ListenNotesClient:
    def __init__(self):
        self.name = ''
    
    def query(self, phrase, fake=False):
        from listennotes import podcast_api
        import requests
        import io
        import os
        
        api_key = None
        if 'LISTEN_NOTES_KEY' in os.environ and not fake:
            api_key = os.environ['LISTEN_NOTES_KEY']
        client = podcast_api.Client(api_key=None)
        clientResponse = client.search(q=phrase, sort_by_date=1, only_in='title,description')
        return clientResponse.content