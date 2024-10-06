class Moderations:
    def __init__(self, client):
        self.client = client

    def create(self, model: str, input):
        """
        Creates a moderation for the given input data and model.

        :param model: The model to use for moderation.
        :param input_data: The input data to moderate.
        :return: The JSON response from the API.
        """
        endpoint = "moderations"
        payload = {
            "model": model,
            "input": input
        }
        response_data = self.client._make_request(endpoint, payload)
        return response_data