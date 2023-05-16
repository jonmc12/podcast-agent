from transcriber import Transcriber

transcriber = Transcriber()

def test_transcribe_local():
    #TODO populate with a small mp3 file
    return transcriber.read_from_url('file://test_audio.mp3')


print(test_transcribe_local())