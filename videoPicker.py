import os
import random

def selectRandomVideo():
    # List all files in the specified folder
    all_files = os.listdir("./video_templates")
    
    # Filter out only video files (you can add more video extensions as needed)
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    videos = [file for file in all_files if any(file.lower().endswith(ext) for ext in video_extensions)]

    if not videos:
        raise FileNotFoundError("No video files found in the specified directory.")

    # Select a random video from the list
    random_video = random.choice(videos)
    
    #print(f"Selected video: {random_video}")

    return os.path.join("./video_templates", random_video)

# Example usage
random_video_path = selectRandomVideo()