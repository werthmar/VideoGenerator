from storyGenerator import generateStory
from audioGenerator import generateAudio
from videoPicker import selectRandomVideo
from videoGenerator import processVideo
import subprocess

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


def testUpload():
    # Define your command as a list
    command = [
        'python', 'cli.py', 'upload',
        '--user', 'my_saved_username',
        '-v', '../generated_video/part_1.mp4',
        '-t', 'My video title'
    ]

    try:
        # Run the command
        result = subprocess.run(command, cwd='./tiktok_auto_uploader', capture_output=True, text=True, check=True)

        # Print the output
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("Error message:", e.stderr, e.stdout)

if __name__ == "__main__":
    #main()
    testUpload()