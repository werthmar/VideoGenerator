<Installation>

install ffmpeg:
    -MacOs: brew install ffmpeg
    -Linux:
        sudo apt update
        sudo apt install ffmpeg

install imagemagic:
    -MacOs: brew install imagemagick
    -Linux: sudo apt install imagemagick

pip install -r requirements.txt
(pip install coqui-tts instead of pip install tts if there are problems)
(Pillow should be version==8.4.0 -> pip install Pillow==8.4.0)


<Videos>
For Downloaded videos if they are corrupted run:
    ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
