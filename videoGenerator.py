import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageFont, ImageDraw
from moviepy.video.fx.all import crop
import speech_recognition as sr
from pilmoji import Pilmoji
import numpy as np
import re
import emoji
from gemeni_subtitleGenerator import load_transcription_results

# Function to generate transcription with timing OLD, now using gemeni_subtitleGenerator
def get_transcription_with_timing(audio_path):
    recognizer = sr.Recognizer()
    audio_clip = AudioFileClip(audio_path)
    duration = int(audio_clip.duration)
    step = 2  # seconds
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

                for i in range(0, len(words), 3):  # Process in chunks of up to 3 words
                    group = words[i:i+3]  # Take up to 3 words
                    if len(group) == 3:
                        text = group[0] + ' ' + group[1] + '\n' + group[2]
                    else:
                        text = ' '.join(group)  # Handle cases where fewer than 3 words

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
    # Create a list of text clips based on transcription data
    text_clips = []
    for word_info in captions:
        word = word_info['word']
        start_time = word_info['start_time']
        end_time = word_info['end_time']
        text_clip = (
            TextClip(txt=word.upper(), fontsize=100, font="./fonts/Rubik-ExtraBold.ttf", color='white', stroke_color='black', stroke_width=8) #Verdana-bold
                    .set_position('center', 'center')
                    .set_start(start_time)
                    .set_duration(end_time - start_time)
            )
        text_clips.append(text_clip)

    # Overlay the text clips on the video
    return CompositeVideoClip([video_clip, *text_clips], size=video_clip.size)

    #return CompositeVideoClip(output_clips, size=video_clip.size)

def add_title(video_clip, title, start):
    # Extract emojis
    emojis = [char for char in title if char in emoji.EMOJI_DATA]
    emojis = ''.join(emojis)
    title = re.sub(emoji.get_emoji_regexp(), '', title)
    
    # Add the title
    title_clip = (TextClip(title.upper(), fontsize=70, font="Verdana-bold", color='black', bg_color='white')
                  .set_position(('center', 440))  # Position at top center with some margin
                  .set_start(start)
                  .set_duration(7.0)) #video_clip.duration
    
    video_with_title= CompositeVideoClip([video_clip, title_clip])
    #return CompositeVideoClip([video_clip, title_clip])

    # Add the emoji
    emoji_font = ImageFont.truetype('./fonts/NoToColorEmoji-Regular.ttf', 120)
    # Calculate the size needed for the image
    text_size = emoji_font.getsize(emojis.strip())
    text_size = (text_size[0], text_size[1] * 2) #increase size so emoji dosnt get cut off

    # Create a transparent image
    image = Image.new('RGBA', text_size, (0, 0, 0, 0))
    # Use Pilmoji to draw the emoji onto the image
    with Pilmoji(image) as pilmoji:
        pilmoji.text((0, 0), emojis.strip(), (0, 0, 0), emoji_font)

    # Create the emoji image clip
    emoji_clip = (ImageClip(np.array(image))
                  .set_position(('center', 550))
                  .set_start(start)
                  .set_duration(7.0)) #video_clip.duration

    return CompositeVideoClip([video_with_title, emoji_clip])

def add_part_name(video_clip, part_number, part_color, start):
    # Only display part name for first 5 sec so its visible in profile
    part_clip = (TextClip(f'Part {part_number}', fontsize=120, font="./fonts/Rubik-ExtraBold.ttf", color=part_color, stroke_color="white", stroke_width=8)
                  .set_position(('center', 700))  # Position at bottom center with some margin
                  .set_start(start)
                  .set_duration(2.0))
    
    return CompositeVideoClip([video_clip, part_clip])

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

def define_part_duration(video_duration):
    #other idea just make video.duration = partduration * numerOfParts
    # Define the part length in seconds
    number_of_parts = 1

    # Decide the number of parts based on video length
    if video_duration >= 420:
        number_of_parts = 4
    elif video_duration >= 300:
        number_of_parts = 3
    elif video_duration >= 180:
        number_of_parts = 2

    # Calculate initial part length
    part_length = video_duration / number_of_parts
    return int(part_length), number_of_parts


# Main function to combine everything
def processVideo(title, video_path="./video_templates/MinecraftVid1.mp4", audio_path="./generated_audio/output.wav"):
    output_dir = "./generated_video/"
    # Load video and audio files
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Limit video duration to audio duration and crop it to right format
    video_clip = video_clip.subclip(0, audio_clip.duration)
    cropped_video = crop_to_vertical(video_clip)

    # Get automatic captions
    #captions = get_transcription_with_timing(audio_path)
    captions = load_transcription_results()
    # Add captions to video
    video_with_captions = add_captions(cropped_video, captions)

    # Determina part length
    video_length = int(video_with_captions.duration)
    part_length, number_of_parts = define_part_duration(video_length)
    #Cap video length to length of parts
    video_length = part_length * number_of_parts

    #part_length = 70  # 1 minute and 10 seconds
    output_files = []

    # Pick a random color for the part text
    #colors = ["cyan", "red", "blue", "green", "purple", "pink", "orange", "yellow", "magenta"]
    #part_color = random.choice(colors)

    # Split video by defined part length
    for i, start in enumerate(range(0, video_length, part_length)):
        end = min(start + part_length + 5, video_with_captions.duration)
        part_name = f"{title}_part_{i+1}.mp4"
        output_path = os.path.join(output_dir, part_name)

        # Add title to the video
        video_with_captions_and_title = add_title(video_with_captions, title, start)

        # Add part name for thumbmail
        final_video = add_part_name(video_with_captions_and_title, i + 1, "black", start)

        # Use subclip to extract and write each segment
        final_video.subclip(start, end).write_videofile( output_path, codec="libx264", audio_codec="aac", temp_audiofile=f"./temp/{title}_part_{i+1}_temp.mp4")
        output_files.append(part_name)

    # Return the location of the saved video
    return output_files

if __name__ == "__main__":
    print(processVideo("emoji 8 😤!!"))