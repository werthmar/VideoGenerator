import subprocess

def upload(title, video):
    # Define your command as a list
    command = [
        'python', 'cli.py', 'upload',
        '--user', 'my_saved_username',
        '-v', f'../generated_video/{video}',
        '-t', title
    ]

    try:
        # Run the command
        result = subprocess.run(command, cwd='./tiktok_auto_uploader', capture_output=True, text=True, check=True)

        # Print the output
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Upload failed with exit code {e.returncode}")
        print("Error message:", e.stderr, e.stdout)


if __name__ == "__main__":
    upload()
    #testUpload()