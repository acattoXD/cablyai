class Message:
    def __init__(self, role, content):
        """
        Initializes a Message object with the given role and content.

        :param role: The role of the message (either "system", "assistant" and finally "user").
        :param content: The content of the message.
        """
        self.role = role
        self.content = content

class Choice:
    def __init__(self, choice):
        """
        Initializes a Choice object with the given data from the API.

        :param choice: The JSON data for the choice from the API.
        """
        self.index = choice["index"]
        self.message = Message(choice["message"]["role"], choice["message"]["content"])
        self.finish_reason = choice["finish_reason"]


class Completion:
    def __init__(self, choices):
        self.choices = [Choice(choice) for choice in choices]

class Completions:
    def __init__(self, client):
        self.client = client

    def create(self, model: str, messages: list, max_tokens: int = None, temperature: int = None):
        """
        Creates a completion for the given messages and model.

        :param model: The model to use for generating the completion.
        :param messages: The messages to generate a completion for.
        :param max_tokens: The maximum number of tokens to generate (default is model dependent).
        :param temperature: The temperature to use for generating the completion (default is 0.7).
        :return: A Completion object containing the generated completion.
        """
        endpoint = "chat/completions"
        payload = {
            "model": model,
            "messages": messages
        }
        
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        if temperature is not None:
            payload["temperature"] = temperature

        response_data = self.client._make_request(endpoint, payload)
        
        return Completion(response_data["choices"])


class Chat:
    def __init__(self, client):
        self.client = client
        self.completions = Completions(client)  
