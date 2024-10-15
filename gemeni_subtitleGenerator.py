from google.cloud import speech
from google.cloud import storage
import json

# Upload audio file to Google Cloud Storage
def upload_to_gcs(source_file_name, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'File uploaded to gs://{bucket_name}/{destination_blob_name}')
    return f'gs://{bucket_name}/{destination_blob_name}'

def transcribe_audio_with_word_time_offsets(gcs_uri, outputFile="./temp/transcription_results.json"):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000, #Make sure its same sample rate as in voices
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=600)

    # The first result includes the start and end time for each word.
    word_timings = []
    for result in response.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            print(f"Word: {word}, start_time: {start_time}, end_time: {end_time}")
            word_timings.append({'word': word, 'start_time': start_time, 'end_time': end_time})

    # Save to a JSON file
    with open(outputFile, 'w') as json_file:
        json.dump(word_timings, json_file, indent=4)
    return outputFile

def generate_subtitles(audioFile='./generated_audio/output.wav'):
    cloud_text = upload_to_gcs(audioFile, 'video_generator_temp', 'output.wav')
    return transcribe_audio_with_word_time_offsets(cloud_text)

def load_transcription_results():
    with open('./temp/transcription_results.json', 'r') as json_file:
        return json.load(json_file)

if __name__ == "__main__":
    generate_subtitles()
