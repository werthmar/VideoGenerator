from moviepy.video.io.VideoFileClip import VideoFileClip

def splitVideo(inputFile, videoTitle="splitVideo", timeInteval=65):
    # Load the video
    video = VideoFileClip(inputFile)
    
    # Calculate the number of parts
    duration = video.duration
    parts = int(duration // timeInteval) + (1 if duration % timeInteval else 0)
    
    # List to store the file paths of the created video parts
    part_files = []

    # Split video into parts
    for i in range(parts):
        start_time = i * timeInteval
        end_time = min((i + 1) * timeInteval, duration)
        
        # Generate output filename
        outputFile = f"./generated_video/{videoTitle}_part{i+1}.mp4"
        
        # Subclip and write part
        print(f"Exporting {outputFile} from {start_time} to {end_time}")
        video.subclip(start_time, end_time).write_videofile(outputFile, codec="libx264", audio_codec="aac")
        
        # Add the output file path to the list
        part_files.append(outputFile)

    # Close the original video file
    video.close()
    
    # Return the list of file paths
    return part_files


if __name__ == "__main__":
    # Set the parameters
    inputFile = "./generated_video/output.mp4" # Replace with your actual video file name
    timeInteval = 600  # 1 minute and 5 seconds is 65 seconds
    videoTitle = "split_video" # Name prefix for the output files

    # Call the function
    created_parts = splitVideo(inputFile, videoTitle="subwaySurfer", timeInteval=600)

    # Print the paths of the created video parts
    print("Created video parts:", created_parts)