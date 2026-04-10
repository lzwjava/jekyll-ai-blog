import os
import argparse
from google.cloud import storage
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


MAX_AUDIO_LENGTH_SECS = 20 * 60 * 60
OUTPUT_DIRECTORY = "assets/transcriptions"


def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US"):
    """
    Transcribes an audio file using Google Cloud Speech-to-Text Batch API.

    Args:
        audio_gcs_uri: GCS URI of the audio file.
        output_gcs_folder: GCS URI of the folder to store the transcription.
        language_code: Language code for transcription (e.g., "en-US", "cmn-CN").
    """
    client = SpeechClient()

    # Determine file extension from GCS URI
    filename = audio_gcs_uri.split("/")[-1]
    file_extension = filename.split(".")[-1].lower()

    # Pick the correct oneof for decoding_config
    # - OGG/Opus requires explicit decoding.
    # - m4a/aac and most others can rely on auto detect.

    # Set model based on language code
    if "cmn-CN" in language_code:
        model = "long"
    else:
        model = "long"

    if file_extension == "ogg":
        decoding = cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.OGG_OPUS,
            # You can omit these if unknown; Opus is often 48 kHz/stereo, but STT handles downmixing.
            # Provide only if you know them; leaving them out lets the service infer.
            sample_rate_hertz=48000,
            audio_channel_count=1,
        )
        config = cloud_speech.RecognitionConfig(
            explicit_decoding_config=decoding,
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            language_codes=[language_code],
        )
        config.model = model
    else:
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            language_codes=[language_code],
        )
        config.model = model

    output_config = cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(uri=output_gcs_folder),
    )

    files = [cloud_speech.BatchRecognizeFileMetadata(uri=audio_gcs_uri)]

    request = cloud_speech.BatchRecognizeRequest(
        recognizer="projects/graphite-ally-445108-k3/locations/global/recognizers/_",
        config=config,
        files=files,
        recognition_output_config=output_config,
    )

    print("Waiting for operation to complete...")
    operation = client.batch_recognize(request=request)
    # Timeout scaled to your MAX_AUDIO_LENGTH_SECS
    response = operation.result(timeout=3 * MAX_AUDIO_LENGTH_SECS)
    print(response)


def process_audio_file(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.basename(input_file)
    if not (filename.endswith(".m4a") or filename.endswith(".ogg")):
        print(f"Error: {filename} is not a supported audio file (.m4a or .ogg).")
        return

    output_filename = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
    if os.path.exists(output_filename):
        print(f"Skipping {filename}: {output_filename} already exists.")
        return

    print(f"Processing: {filename}")
    try:
        # Determine language based on filename suffix
        # Tip: v2 expects BCP-47; "cmn-CN" generally works, but you can also try "cmn-Hans-CN".
        if filename.endswith("-zh.m4a") or filename.endswith("-zh.ogg"):
            language_code = "cmn-Hans-CN"
        else:
            language_code = "en-US"

        # Construct GCS URIs
        gcs_audio_uri = f"gs://test2x/audio-files/{filename}"
        gcs_output_uri = f"gs://test2x/transcripts/{os.path.splitext(filename)[0]}"

        # Upload the file to GCS if it doesn't exist
        storage_client = storage.Client()
        bucket = storage_client.bucket("test2x")
        blob = bucket.blob(f"audio-files/{filename}")
        if not blob.exists():
            blob.upload_from_filename(input_file)
            print(f"Uploaded {filename} to GCS.")
        else:
            print(f"{filename} already exists in GCS.")

        run_batch_recognize(
            audio_gcs_uri=gcs_audio_uri,
            output_gcs_folder=gcs_output_uri,
            language_code=language_code,
        )
        print(f"File {filename} processed.\n")

        # Download the transcription JSON(s)
        blobs = storage_client.list_blobs(
            "test2x", prefix=f"transcripts/{os.path.splitext(filename)[0]}"
        )
        for b in blobs:
            if b.name.endswith(".json"):
                local_output_path = os.path.join(output_dir, os.path.basename(b.name))
                b.download_to_filename(local_output_path)
                print(f"Downloaded {b.name} to {local_output_path}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")

    print(f"Processing complete for {filename}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a single Voice Memo (.m4a/.ogg) file to generate transcription."
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Input path for the Voice Memo file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="assets/transcriptions",
        help="Output directory for transcriptions.",
    )

    args = parser.parse_args()

    process_audio_file(
        input_file=args.input_file,
        output_dir=args.output,
    )
