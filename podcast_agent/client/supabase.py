import os
from typing import Any
from supabase.client import Client, create_client

class SupabaseClient:
    """
    A class to interact with Supabase services.
    """

    def __init__(self):
        """
        Initialize Supabase client with environment variables.
        """
        try:
            self.url: str = os.environ['SUPABASE_URL']
            self.key: str = os.environ['SUPABASE_KEY']
        except KeyError:
            raise ValueError("Both SUPABASE_URL and SUPABASE_KEY must be set.")
        self.client: Client = create_client(self.url, self.key)
        self.email: str = "jonathan@teammachine.ai"
        self.password: str = "yog-pean-eek-01"

    def get_client(self) -> Client:
        """
        Get the Supabase client.
        """
        return self.client

    def get_storage(self) -> Any:
        return self.client.storage

    def list_storage_buckets(self) -> Any:
        return self.client.storage.list_buckets()

    def create_storage_bucket(self, name: str) -> Any:
        return self.client.storage.create_bucket(name)

    def get_bucket(self, bucket_name: str) -> Any:
        return self.client.storage.get_bucket(bucket_name)

    def get_table(self, table_name: str) -> Any:
        return self.client.table(table_name)

    def sign_up_user(self, email: str, password: str) -> Any:
        return self.client.auth.sign_up({"email": email, "password": password})

    def sign_in_user(self, email: str, password: str) -> Any:
        return self.client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    
    def download_file(self, bucket_name: str, file_name: str) -> Any:
        with open(file_name, 'wb+') as f:
            res = self.client.storage.from_(bucket_name).download(file_name)
            f.write(res)

        return
    
    def upload_file(self, bucket_name: str, file_name: str) -> Any:
        with open(file_name, 'rb') as f:
            res = self.client.storage.from_(bucket_name).upload(
                file_name, 
                os.path.abspath(file_name)
            )

        return res
