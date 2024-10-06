from .chat import Chat
from .images import Images
from .audio import Audio
from .moderations import Moderations
import requests

class CablyAI:
    def __init__(self, api_key: str):
        """
        Initializes a CablyAI client with the given API key.

        :param api_key: The API key to use for authentication.
        """
        self.api_key = api_key
        self.chat = Chat(self)
        self.images = Images(self)
        self.audio = Audio(self)
        self.moderations = Moderations(self)
        
    def _make_request(self, endpoint: str, payload: dict, files=None):
        """
        Makes a POST request to the CablyAI API with the given endpoint and payload.

        :param endpoint: The API endpoint to POST to.
        :param payload: The JSON payload to send with the request.
        :param files: The files to upload with the request.
        :return: The JSON response from the API or raw content if it's audio.
        :raises requests.exceptions.RequestException: If the request fails.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}

        if files:
            response = requests.post(
                f"https://cablyai.com/v1/{endpoint}",
                headers=headers,
                data=payload,
                files=files
            )
        else:
            response = requests.post(
                f"https://cablyai.com/v1/{endpoint}",
                headers=headers,
                json=payload
            )

        response.raise_for_status()

        if endpoint == "audio/speech":
            return response.content
        else:
            return response.json()
