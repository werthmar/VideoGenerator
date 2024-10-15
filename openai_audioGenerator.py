import os
from openai import OpenAI
from dotenv import load_dotenv

def generateAudio(story: str, output_file: str = "./generated_audio/output.mp3"):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print(os.getenv("OPENAI_API_KEY"))

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=story
    )

    response.with_streaming_response_method(output_file)

# Example usage:
if __name__ == "__main__":
    generateAudio("Today is a wonderful day to build something people love!")