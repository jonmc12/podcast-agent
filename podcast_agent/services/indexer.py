import asyncio

import requests
import tempfile
from podcast_agent.client.transcriber import TranscriberClient
from podcast_agent.services.podcast_api import PodcastApiService
from podcast_agent.services.supabase import SupabaseService

supabase_service = SupabaseService()

from llama_index import (
    GPTVectorStoreIndex, 
    GPTSimpleKeywordTableIndex, 
    SimpleDirectoryReader,
    LLMPredictor,
    ServiceContext,
    StorageContext
)

from llama_index.storage.docstore import SimpleDocumentStore#, SimpleVectorStore, SimpleIndexStore,ServiceContext

from langchain.llms.openai import OpenAIChat

class IndexerService:
    def __init__(self, persist_dir = './indices'):
        self.supabase_service = SupabaseService()
        self.llm_predictor_chatgpt = LLMPredictor(llm=OpenAIChat(temperature=0, model_name="gpt-3.5-turbo"))
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=self.llm_predictor_chatgpt, chunk_size_limit=1024
            )
        self.persist_dir = persist_dir
        #self.storage_context = StorageContext.from_defaults(
        #    docstore=SimpleDocumentStore.from_persist_dir(persist_dir=self.persist_dir),
            #vector_store=SimpleVectorStore.from_persist_dir(persist_dir=self.persist_dir),
            #index_store=SimpleIndexStore.from_persist_dir(persist_dir=self.persist_dir),
        #    )
    def index_content(self, content):

        with tempfile.NamedTemporaryFile(suffix='.txt', mode='r+', delete=True) as temp_file:
            temp_file.write(content)
            temp_file_name = temp_file.name
            temp_file.seek(0)
            return GPTVectorStoreIndex.from_documents(
                                                        SimpleDirectoryReader(input_files=[temp_file_name]).load_data(), 
                                                        service_context=self.service_context
                                                    )
            
    def persist_index(self, content):
        indices = self.index_content(content)
        #self.storage_context.persist(persist_dir=self.persist_dir)

    def run_query(self, indices, query):
        query_engine = indices.as_query_engine()
        response = query_engine.query(query)
        return response 

    def read_from_supabase(self, bucket, file):
        SupabaseService().client.download_file(bucket, file)

    