from TTS.api import TTS
import os

#using coqui-ai tts
def generateAudio(story: str, output_file: str = "./generated_audio/output.wav"):
    # Initialize Coqui TTS with a specific model
    # Replace 'tts_models/en/ljspeech/glow-tts' with the model you wish to use
    tts = TTS(model_name="tts_models/en/jenny/jenny")

    # Generate speech from the story text and save to the specified output file
    tts.tts_to_file(
        text=story,
        file_path=output_file,
        split_sentences=True,
        speed=0.9,
        pitch=-1,
        effects=["reverb"],
        #emotion="calm"
        emotion="excited",
    )
    
    #print(f"Audio generated and saved to {output_file}")
    return output_file



def listModels():
    # List available models
    models = TTS.list_models()

    # Print organized model information
    print(f"{'Model Name':<40} {'Language':<20} {'Description'}")
    print("=" * 80)

    # Iterate through each model and print details
    for model in models:
        # Extract language information from the model name
        # Example: "tts_models/en/ljspeech/glow-tts" -> "English"
        parts = model.split('/')
        language_code = parts[1]  # e.g., 'en' or 'es'
        language = "Unknown"

        # Map language codes to full language names
        language_mapping = {
            'en': 'English',
            'es': 'Spanish',
            'de': 'German',
            'fr': 'French',
            'zh': 'Chinese',
            # Add other mappings as needed
        }
        
        # Get the language name if it exists in the mapping
        language = language_mapping.get(language_code, "Unknown")

        # Print the model name, language, and description
        # Model names and descriptions can be customized based on your knowledge or use cases
        print(f"{model:<40} {language:<20} {'Pre-trained model for speech synthesis'}")


# Example usage:
if __name__ == "__main__":
    #listModels()
    sample_story = "Once upon a time in a faraway land, there was a brave knight."
    generateAudio(sample_story)
