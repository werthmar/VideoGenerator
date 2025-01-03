# VideoGenerator

## Overview

VideoGenerator is a Python program designed to automatically generate and upload videos using AI from the Google Cloud Platform. This tool is ideal for content creators who want to streamline their video production process by leveraging advanced AI technologies and cloud services.
This project was purely made for learning purposes.

## Features

- **Automated Video Generation**: Uses AI to generate stories, tts and captions and combines them with video templates to upload them.
- **Cloud Integration**: Utilizes Google Cloud Platform services for processing and storage, ensuring scalability and reliability.
- **TikTok Auto Uploader**: Includes a module for automatically uploading videos to TikTok, saving time and effort, module can be downloaded here: [TikTok-auto-uploader](https://github.com/makiisthenes/TiktokAutoUploader)

## Installation
install ffmpeg:
    -MacOs: brew install ffmpeg
    -Linux:
        sudo apt update
        sudo apt install ffmpeg

install imagemagic:
    -MacOs: brew install imagemagick
    -Linux: sudo apt install imagemagick

Gemini Method: install google cloud cli: https://cloud.google.com/sdk/docs/install

follow install instructions of tiktok_uploader (readme.md inside folder) -> requirements.txt install not necessary bcs its included in main requirements.txt
AFTER installing the requirements txt for the tiktok uploader reinstall the requirements txt of the videoGenerator bcs we need an older version of one of the dependecies (using pip install -r requirements.txt)
    adjust config.txt (VIDEOS_DIR= "./VideosDirPath" change to appropriate path)

pip install -r requirements.txt
(pip install coqui-tts instead of pip install tts if there are problems)
(Pillow should be version==8.4.0 -> pip install Pillow==8.4.0)


<Videos>
For Downloaded videos if they are corrupted run:
    ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4

<h1>Startup</h1>
python_enviroment/bin/activate
gcloud init
