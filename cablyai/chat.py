import json
import requests
from bs4 import BeautifulSoup
from googlesearch import search as google_search

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def __repr__(self):
        return str(self.__dict__)

class Web:
    def __init__(self, **_): 
        pass

    def search(self, query: str):
        try:
            # print(str([url for url in google_search(query)]))
            return str([url for url in google_search(query)])
        except Exception as e:
            return f"Failed to execute the search: {e}"
        
    def http_get(self, url, index=[0, 7]):
        try:
            response = requests.get(url, timeout=5)
            print(response.text)
        except requests.RequestException as e:
            return f"Failed to retrieve the webpage: {e}"
        
        if response.status_code != 200:
            return "Failed to retrieve the webpage."
        
        return f"Chunks {index[0]} - {index[1]}:\n" + ' '.join([
            i.get_text() 
            for i in BeautifulSoup(response.text, 'html.parser').find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])[index[0]:index[1]]
        ])

search_tools_dict = {
    "search": {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Searches the web for the given query and returns the top results. You will typically use the http_get function to get the results after using this function, unless the user only wants URLs. Users may refer to this function as the 'search' function, or they may refer to it as 'Search the web', please run this function if they either tell you 'use your search function', 'search the web', or when you know when it's best to search the web for details, for example: What's the latest version for iOS? Search the web for this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    "http_get": {
        "type": "function",
        "function": {
            "name": "http_get",
            "description": "Sends a GET request to the given URL and returns the shortened response...",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to send the GET request to"
                    },
                    "index": {
                        "type": "array",
                        "description": "An array of two numbers representing the index...",
                        "items": {
                            "type": "number"
                        }
                    }
                },
                "required": ["url"]
            }
        }
    }
}

search_tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Searches the web for the given query and returns the top results. You will typically use the http_get function to get the results after using this function, unless the user only wants URLs. Users may refer to this function as the 'search' function, or they may refer to it as 'Search the web', please run this function if they either tell you 'use your search function', 'search the web', or when you know when it's best to search the web for details, for example: What's the latest version for iOS? Search the web for this.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "http_get",
            "description": "Sends a GET request to the given URL and returns the shortened response...",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to send the GET request to"
                    },
                    "index": {
                        "type": "array",
                        "description": "An array of two numbers representing the index...",
                        "items": {
                            "type": "number"
                        }
                    }
                },
                "required": ["url"]
            }
        }
    }
]

tool_definitions = {
    "search": Web().search,
    "http_get": Web().http_get
}

class Choice:
    def __init__(self, choice):
        self.index = choice["index"]
        self.message = Message(choice["message"]["role"], choice["message"]["content"])
        self.finish_reason = choice["finish_reason"]

    def __repr__(self):
        return str(self.__dict__)

class Completion:
    def __init__(self, choices):
        self.choices = [Choice(choice) for choice in choices]

    def __repr__(self):
        return str(self.__dict__)

class Completions:
    def __init__(self, client):
        self.client = client

    def create(self, model: str, messages: list, tools: list = None, max_tokens: int = None, temperature: int = None):
        if tools and model not in ["gpt-4o", "gpt-4o-mini", "chatgpt-4o-latest", "gpt-4-turbo"]:
            return "Unsupported model. Please use one of the following: 'gpt-4o', 'gpt-4o-mini', 'chatgpt-4o-latest', 'gpt-4-turbo'"
        
        endpoint = "chat/completions"
        payload = {
            "model": model,
            "messages": messages,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        if temperature is not None:
            payload["temperature"] = temperature

        if tools is not None:
            payload["tools"] = tools

        response_data = self.client._make_request(endpoint, payload)
        
        return Completion(response_data["choices"])

    def create_search(self, model: str, messages: list, max_tokens: int = None, temperature: int = None):
        response_text = None
        if model not in ["gpt-4o", "gpt-4o-mini", "chatgpt-4o-latest", "gpt-4-turbo"]:
            return "Unsupported Model. Please use one of the following: 'gpt-4o', 'gpt-4o-mini', 'chatgpt-4o-latest', 'gpt-4-turbo'"
        
        endpoint = "chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "tools": search_tools
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        if temperature is not None:
            payload["temperature"] = temperature

        while response_text is None or (isinstance(response_text, str) and response_text.strip() == ""):
            print('Sending request...')
            
            response_data = self.client._make_request(endpoint, payload)
            
            if "choices" not in response_data or len(response_data["choices"]) == 0:
                print("Warning: No valid choices in response.")
                break
            
            message = response_data["choices"][0]["message"]
            response_text = message["content"]
            tool_calls = message.get("tool_calls", [])
            print("Tool Calls:", tool_calls)
            print("Response Text:", response_text)

            messages.append(
                {
                    "role": "assistant",
                    "content": response_text,
                    "tool_calls": [
                        {
                            "id": tool_call["id"],
                            "name": tool_call["function"]["name"],
                            "type": tool_call["type"],
                            "function": {
                                "name": tool_call["function"]["name"],
                                "arguments": tool_call["function"]["arguments"]
                            }
                        } for tool_call in tool_calls
                    ]
                }
            )

            for tool_call in tool_calls:
                print(f'Executing tool call {tool_call}')
                function = tool_call["function"]
                function_name = function["name"]
                kwargs = json.loads(function["arguments"])
                required_keys = search_tools_dict[function_name]['function']['parameters'].get('required', [])
                
                if all(key in kwargs for key in required_keys):
                    function_to_call = tool_definitions[function_name]
                    try:
                        tool_call_response = function_to_call(**kwargs)
                    except Exception as e:
                        tool_call_response = f"Error: {e}"

                    messages.append(
                        {
                            "role": "tool",
                            "name": function_name,
                            "tool_call_id": tool_call["id"],
                            "content": tool_call_response
                        }
                    )
                print(f'Executed tool call {tool_call}')

        return Completion(response_data["choices"])

class Chat:
    def __init__(self, client):
        self.client = client
        self.completions = Completions(client)
