from storyGenerator import generateStory
from audioGenerator import generateAudio
from videoPicker import selectRandomVideo
from videoGenerator import processVideo
from videoSpliter import splitVideo

def main():
    # 1. Generate the story
    print("Generating story...")
    story = generateStory()
    print(f"Story generated: {story}")

    # 2. Convert story to audio (TTS)
    print("Generating audio...")
    audio_file = generateAudio(story)
    print(f"Audio file created: {audio_file}")

    # 3. Pick a video template and generate a video
    print("Generating video...")
    videoTemplate = selectRandomVideo()
    print(f"Selected video: {videoTemplate}")
    generatedVideo = processVideo(video_path=videoTemplate)
    print(f"Video file created: {generatedVideo}")


if __name__ == "__main__":
    main()