import requests

class TranscriptionResponse:
    def __init__(self, response_data):
        self.text = response_data.get("text", "")

class Transcriptions:
    def __init__(self, client):

        self.client = client

    def create(self, model, file):
        """
        Transcribes the given audio file using the specified model.

        :param model: The model to use for transcription.
        :param file: The audio file to transcribe.
        :return: The transcription result.
        """
        endpoint = "audio/transcriptions"
        files = {
            "file": file
        }
        response_data = self.client._make_request(endpoint, {"model": model}, files=files)
        
        return TranscriptionResponse(response_data)

class SpeechResponse:
    def __init__(self, audio_bytes):
        self.audio_bytes = audio_bytes

    def stream_to_file(self, file_path):
        """
        Streams the audio bytes to a file.

        :param file_path: The path where the audio file will be saved.
        """
        with open(file_path, 'wb') as audio_file:
            audio_file.write(self.audio_bytes)

class Speech:
    def __init__(self, client):
        self.client = client

    def create(self, model: str, voice: str, input_text: str):
        """
        Generates speech from text using the specified model and voice.

        :param model: The model to use for text-to-speech.
        :param voice: The voice to use for generating the speech.
        :param input_text: The text to convert to speech.
        :return: The generated speech response.
        """
        endpoint = "audio/speech"
        payload = {
            "model": model,
            "voice": voice,
            "input": input_text
        }
        response_content = self.client._make_request(endpoint, payload)
        
        return SpeechResponse(response_content)

class Audio:
    def __init__(self, client):
        self.client = client
        self.transcriptions = Transcriptions(client)
        self.speech = Speech(client)
