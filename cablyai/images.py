class ImageData:
    def __init__(self, url):
        """
        Initializes an ImageData object with the given image URL.

        :param url: The URL of the image.
        """
        self.url = url

class ImageGenerationResponse:
    def __init__(self, response_data):
        """
        Initializes an ImageGenerationResponse with the given response data from the API.

        :param response_data: The response data from the API.
        """
        self.data = [ImageData(item["url"]) for item in response_data["data"]]

class Images:
    def __init__(self, client):
        """
        Initializes an Images client with the given client.

        :param client: The CablyAI client to use for making requests.
        """
        self.client = client

    def generate(self, prompt: str, n: int = 1, size: str = "1024x1024", response_format: str = "url", model: str = "flux-realism"):
        """
        Generates an image based on the provided prompt.

        :param prompt: The prompt for the image.
        :param n: The number of images to generate (default is 1).
        :param size: The size of the generated image (default is "1024x1024").
        :param response_format: The format of the response (default is "url").
        :param model: The model to use for image generation (default is "flux-realism").
        :return: A list of ImageData objects, each containing the url of a generated image.
        """
        endpoint = "images/generations"
        payload = {
            "prompt": prompt,
            "n": n,
            "size": size,
            "response_format": response_format,
            "model": model
        }
        response_data = self.client._make_request(endpoint, payload)
        return ImageGenerationResponse(response_data)
