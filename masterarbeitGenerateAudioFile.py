import random
from google.cloud import texttospeech
from gemeni_subtitleGenerator import generate_subtitles

def generateAudio(story, outputFile="./generated_audio/output.wav"):
    # Set up the Google Cloud client
    client = texttospeech.TextToSpeechClient()

    # Define the input text
    input_text = texttospeech.SynthesisInput(text=story)

    # Choose a random voice for the video
    available_voices = [
        {'name': "de-DE-Journey-F", 'ssml_gender': texttospeech.SsmlVoiceGender.FEMALE},
    ]
    choosen_voice= random.choice(available_voices)

    voice = texttospeech.VoiceSelectionParams(
        #language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        language_code="de-DE", name=choosen_voice['name'], ssml_gender=choosen_voice['ssml_gender']

    )
    # Select the type of audio file you want returned (LINEAR16=WAV, MP3 = MP3)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(outputFile, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        return outputFile

def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code="de-DE")

    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        for language_code in voice.language_codes:
            print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

def generate_audio_and_subtitels(story):
    audioFile = generateAudio(story)
    transcriptionFile = generate_subtitles(audioFile)
    return audioFile, transcriptionFile

if __name__ == "__main__":
    #list_voices()

    # Step 1: Create a list to store stories
    stories = []

    print("Enter your stories (type 'done' when finished):")

    # Step 2: Take user input in a loop and store stories
    while True:
        story = input("Enter a story: ")
        if story.lower() == 'done':
            break
        stories.append(story)

    # Define a function to process each story (e.g., print or transform it)
    def process_story(index, story):
        print(f"Processing story: {story}")
        generateAudio(story, outputFile=f"./generated_audio/output{index}.wav")

    # Step 3: Run the function for each story
    for index, story in enumerate(stories, start=1):
        process_story(index, story)


    #generateAudio("Es war einmal ein kleines süßes Mädchen, das hatte jedermann lieb, der sie nur ansah, am allerliebsten aber ihre Großmutter.")

    #generate_subtitles