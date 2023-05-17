# podcast-agent

## Setup

``` bash
conda create --name podcast-agent python=3.10
conda activate podcast-agent

pip install -e .
```

## Modules

1. Podcast API: find and download podcasts
2. Supabase: interact with database and documents
3. Transcriber: use OpenAI whisper to transcribe mp3
4. Audio Clipper: create clips of audio from a start and end time
5. Indexer: index episode transcripts for semantic search
6. Aligner: align speech and text and diarize transcripts

Each module has Clients, Repositories and Services.

## Tests

To run tests:

``` bash
pytest
```

See examples of functionality in the tests.
