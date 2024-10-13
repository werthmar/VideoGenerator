import os
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import crop
import speech_recognition as sr

# Function to generate transcription with timing
def get_transcription_with_timing(audio_path):
    recognizer = sr.Recognizer()
    audio_clip = AudioFileClip(audio_path)
    duration = int(audio_clip.duration)
    step = 5  # seconds
    transcription_with_timing = []

    for start_time in range(0, duration, step):
        end_time = min(start_time + step, duration)
        audio_chunk = audio_clip.subclip(start_time, end_time)
        audio_chunk.write_audiofile("./temp/temp_chunk.wav", codec="pcm_s16le")

        with sr.AudioFile("./temp/temp_chunk.wav") as source:
            audio = recognizer.record(source)
            try:
                recognized_text = recognizer.recognize_google(audio)
                words = recognized_text.split()
                word_duration = step / max(1, len(words))  # Avoid division by zero

                for i in range(0, len(words), 5):
                    group = words[i:i+5]  # Take up to 5 words
                    text = ' '.join(group[:3]) + '\n' + ' '.join(group[3:])
                    start_word_time = start_time + i * word_duration
                    group_duration = word_duration * len(group)
                    transcription_with_timing.append((text, start_word_time, group_duration))
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

    os.remove("./temp/temp_chunk.wav")  # Clean up temporary audio chunk
    return transcription_with_timing

# Function to add captions to video
def add_captions(video_clip, captions):
    output_clips = [video_clip]

    for text, start_time, duration in captions:
        text = text.upper()  # Convert text to uppercase
        text_clip = (TextClip(txt=text, fontsize=80, font="Verdana-bold", color='white', stroke_color='black', stroke_width=6)
                     .set_position('center', 'center')
                     .set_duration(duration)
                     .set_start(start_time))
        output_clips.append(text_clip)

    return CompositeVideoClip(output_clips, size=video_clip.size)

def add_title(video_clip, title="Crazy Story!!"):
    title_clip = (TextClip(title.upper(), fontsize=70, font="Verdana-bold", color='black', bg_color='white')
                  .set_position(('center', 40))  # Position at top center with some margin
                  .set_duration(video_clip.duration))
    return CompositeVideoClip([video_clip, title_clip])

def crop_to_vertical(video, target_width=1080, target_height=1920):
    original_width, original_height = video.size
    
    target_aspect_ratio = target_width / target_height
    original_aspect_ratio = original_width / original_height
    
    if original_aspect_ratio > target_aspect_ratio:
        # If video is wider than the target
        new_width = original_height * target_aspect_ratio
        x1 = (original_width - new_width) / 2
        video = crop(video, x1=x1, width=new_width)
    else:
        # If video is taller than the target
        new_height = original_width / target_aspect_ratio
        y1 = (original_height - new_height) / 2
        video = crop(video, y1=y1, height=new_height)
    
    # Resize to the target resolution after cropping
    return video.resize((target_width, target_height))

def split_video_into_parts(video_clip, part_duration):
    duration = video_clip.duration
    parts = []
    for start_time in range(0, int(duration), part_duration):
        end_time = min(start_time + part_duration, duration)
        part = video_clip.subclip(start_time, end_time)
        parts.append(part)
    return parts

# Main function to combine everything
def processVideo(video_path="./video_templates/MinecraftVid1.mp4", audio_path="./generated_audio/output.wav"):
    output_path = "./generated_video/mergedVideo.mp4"
    # Load video and audio files
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Limit video duration to audio duration and crop it to right format
    video_clip = video_clip.subclip(0, audio_clip.duration)
    cropped_video = crop_to_vertical(video_clip)

    # Get automatic captions
    captions = get_transcription_with_timing(audio_path)

    # Add captions to video
    video_with_captions = add_captions(cropped_video, captions)

    # Add title to the video
    video_with_captions_title = add_title(video_with_captions, title="Insane Story!!")

    # Save the final video with captions
    video_with_captions_title.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile=f"./temp/mergedVideo_temp.mp4")

    # Return the location of the saved video
    return output_path

if __name__ == "__main__":
    print(processVideo())