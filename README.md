<Installation>

install ffmpeg:
    -MacOs: brew install ffmpeg
    -Linux:
        sudo apt update
        sudo apt install ffmpeg

install imagemagic:
    -MacOs: brew install imagemagick
    -Linux: sudo apt install imagemagick

Noje.js
GoogleChrome

follow install instructions of tiktok_uploader (readme.md inside folder)
AFTER installing the requirements txt for the tiktok uploader reinstall the requirements txt of the videoGenerator bcs we need an older version of one of the dependecies (using pip install -r requirements.txt)
    adjust config.txt (VIDEOS_DIR= "./VideosDirPath" change to appropriate path)

pip install -r requirements.txt
(pip install coqui-tts instead of pip install tts if there are problems)
(Pillow should be version==8.4.0 -> pip install Pillow==8.4.0)


<Videos>
For Downloaded videos if they are corrupted run:
    ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
