import random
from storyGenerator import generateStory
#from inputStory import manualStoryInput
#from coqui_audioGenerator import generateAudio
from gemeni_storyGenerator import generateStory
from gemeni_audioGenerator import generate_audio_and_subtitels
from videoPicker import selectRandomVideo
from videoGenerator import processVideo
from uploader import upload
import os
import glob

def main():
    
    while True:

        # 1. Generate the story
        # Manual Method
        #stories = manualStoryInput()

        # Gemini Method
        print("Generating story...")
        title, tags, story = generateStory()

        # Process each Story
        print(f"\nProcessing story: {title}")

        # 2. Convert story to audio (TTS) and add subtitles
        print("Generating audio...")
        audio_file, transcriptionFile = generate_audio_and_subtitels(story)
        print(f"Audio file created: {audio_file}, Transcription file created {transcriptionFile}")

        # 3. Pick a video template and generate a video
        print("Generating video...")
        videoTemplate = selectRandomVideo()
        print(f"Selected video: {videoTemplate}")
        generatedVideos = processVideo(title, video_path=videoTemplate, audio_path=audio_file)
        print(f"Video file created: {generatedVideos}")

        # 5. Select TikTok Account
        available_accounts = ['my_saved_username', 'storiesaboutstufff']
        selected_account = random.choice(available_accounts)

        # 4. Upload every video part to TikTok
        for x, video in enumerate(generatedVideos, start=1):
            upload(f'{title} Part {x} {tags}', video, selected_account)

        # 5. Cleanup
        clear_directory('./temp/')
        clear_directory('./generated_video/')
        clear_directory('./generated_audio/')


def clear_directory(directory_path):
    try:
        # Use glob to get all files in the directory
        files = glob.glob(os.path.join(directory_path, '*'))

        # Iterate through the list and remove each file
        for file_path in files:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()