# cablyai

A simple Python client for interacting with the CablyAI API, allowing you to easily make requests for text, image, audio generation, and moderation.

## Installation

To install the package, you can clone the repository using git and install it using `pip`:

```bash
git clone https://github.com/acattoXD/cablyai.git
cd cablyai
pip install .
```
Or, you install it using the pypi library.
```bash
pip install cablyai
```
## Usage

Here’s a basic example of how to use the CablyAI client:

```python
from cablyai import CablyAI

# Initialize the client with your API key
client = CablyAI("YOUR_API_KEY")

# Example: Chat request
response = client.chat.completions.create(
    model="MODEL_NAME",
    messages=[
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
)
print("Chat Response:", response.choices[0].message.content)

# Example: Image generation request
image_response = client.images.generate(
    prompt="A sunset over the mountains.",
    n=1,
    size="1024x1024",
    response_format="url",
    model="MODEL_NAME"
)
print("Image Response:", image_response.data[0].url)


# Example: Text-to-speech request
from pathlib import Path

speech_file_path = Path(__file__).parent / "speech.mp3"
audio_response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!"
)
audio_response.stream_to_file(speech_file_path)
print(f"Speech saved to {speech_file_path}")

# Example: Content moderation request
moderation_response = client.moderations.create(
    model="omni-moderation-latest",
    input="I hate you"
)
print("Moderation Response:", moderation_response)
```

## API Methods

### `client.chat.completions.create(model: str, messages: list)`

- **Description**: Sends a chat prompt to the CablyAI API and returns the response.
- **Parameters**:
  - `model`: The model to use for the chat.
  - `messages`: A list of messages in the conversation.

### `client.images.generate(prompt: str, n: int = 1, size: str = "1024x1024", response_format: str = "url", model: str)`

- **Description**: Generates an image based on the provided prompt.
- **Parameters**:
  - `prompt`: The prompt for the image.
  - `n`: The number of images to generate (default is 1).
  - `size`: The size of the generated image (default is "1024x1024").
  - `response_format`: Format of the response (default is "url").
  - `model`: The model to use for image generation.


### `client.audio.speech.create(model: str, voice: str, input: str)`

- **Description**: Generates speech from the provided text input.
- **Parameters**:
  - `model`: The model to use for text-to-speech conversion.
  - `voice`: The voice to use for the generated speech.
  - `input`: The text input to convert to speech.

### `client.moderations.create(model: str, input)`

- **Description**: Checks the content moderation for the provided input, which can be text or a combination of text and images.
- **Parameters**:
  - `model`: The moderation model to use.
  - `input`: The input to moderate, can be text or a list containing both text and images.

## License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

acatto