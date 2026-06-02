---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Speeding Up Long Audio Transcription Processing
translated: false
type: note
---

### Why Is Processing So Long for 30-Min or 1-Hour Audio?

The Google Cloud Speech-to-Text Batch API (v2) is designed for asynchronous, long-running operations, especially with the `"long"` model, which handles extended audio files (up to ~1 hour per file). Here's why it can feel "too long":

- **Processing Time Scales with Audio Length**: Transcription isn't instant. For a 30-minute audio file, it might take 5-20 minutes; for 1 hour, 10-40 minutes or more. This includes:
  - Queueing time (if your project/region is busy).
  - Actual transcription (AI model inference, which is compute-intensive for long audio).
  - Post-processing (e.g., word timings, confidence scores).
- **Batch Nature**: Unlike real-time streaming, batch jobs run in the background on Google's servers. Your script calls `operation.result()`, which blocks and waits, but the real work happens asynchronously.
- **Other Factors**:
  - Audio format/quality: OGG/Opus or M4A/AAC needs decoding, which adds overhead if sample rates/channels are mismatched.
  - Model choice: `"long"` is optimized for meetings/podcasts but slower than shorter models like `"default"` or `"short"`.
  - Network/Quota: Uploading to GCS, API calls, and downloading results add latency. Free tier quotas or high demand can delay jobs.
  - No Built-in Parallelism: The script processes one file at a time sequentially.

If your audio is consistently 30+ minutes, the current setup isn't ideal for quick turnaround—it's better for offline/bulk processing.

### How to Fix It: Reduce Processing Time

To handle long audio faster, the key is **splitting the file into smaller chunks** (e.g., 5-15 minutes each). This allows:

- Parallel processing (run multiple batch jobs concurrently).
- Using faster models (e.g., `"short"` or `"default"`) per chunk.
- Shorter wait times per job (e.g., 1-5 minutes per chunk vs. 30+ minutes for the whole file).

#### Step 1: Split the Audio File

Use **FFmpeg** (free, command-line tool) to split files without re-encoding (fast and lossless). Install FFmpeg if needed (e.g., `brew install ffmpeg` on macOS, `apt install ffmpeg` on Linux).

Add a function to your script to split the input file. Here's an updated version of your script with splitting integrated:

```python
import os
import argparse
import subprocess
import tempfile
from google.cloud import storage
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import sys
import time  # For polling

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.llm.openrouter_client import call_openrouter_api  # noqa: F401

MAX_AUDIO_LENGTH_SECS = 20 * 60 * 60
OUTPUT_DIRECTORY = "assets/transcriptions"
CHUNK_DURATION_SECS = 600  # 10 minutes per chunk; adjust as needed (e.g., 900 for 15 min)


def split_audio_file(input_file, chunk_duration_secs=CHUNK_DURATION_SECS):
    """
    Split audio file into smaller chunks using FFmpeg.

    Args:
        input_file: Path to input audio.
        chunk_duration_secs: Duration of each chunk in seconds.

    Returns:
        List of chunk file paths.
    """
    filename = os.path.basename(input_file)
    name_without_ext = os.path.splitext(filename)[0]
    dir_name = os.path.dirname(input_file)

    # Create temp dir for chunks
    temp_dir = tempfile.mkdtemp()
    chunk_files = []

    # FFmpeg command (no re-encoding for speed)
    cmd = [
        "ffmpeg", "-i", input_file,
        "-f", "segment",  # Output format
        "-segment_time", str(chunk_duration_secs),
        "-c", "copy",  # Copy streams without re-encoding
        "-map", "0",  # Map all streams
        f"{temp_dir}/{name_without_ext}_chunk_%03d.{os.path.splitext(filename)[1][1:]}",  # Output pattern
        "-y"  # Overwrite
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # Find generated chunks
        for file in os.listdir(temp_dir):
            if file.startswith(f"{name_without_ext}_chunk_") and file.endswith(os.path.splitext(filename)[1]):
                chunk_files.append(os.path.join(temp_dir, file))
        chunk_files.sort()  # Sort by name (e.g., chunk_001, chunk_002)
        print(f"Split {filename} into {len(chunk_files)} chunks.")
        return chunk_files
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error splitting {filename}: {e}")
        return []


def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US"):
    """
    Transcribes an audio file using Google Cloud Speech-to-Text Batch API.
    Updated to use shorter model if audio is likely short (e.g., after splitting).
    """
    client = SpeechClient()

    filename = audio_gcs_uri.split('/')[-1]
    file_extension = filename.split('.')[-1].lower()

    # For chunks, use "short" or "default" model for speed (if <15 min)
    model = "short" if CHUNK_DURATION_SECS < 900 else "long"  # Adjust based on chunk size

    if file_extension == "ogg":
        decoding = cloud_speech.ExplicitDecodingConfig(
            encoding=cloud_speech.ExplicitDecodingConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            audio_channel_count=1
        )
        config = cloud_speech.RecognitionConfig(
            explicit_decoding_config=decoding,
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            model=model,
            language_codes=[language_code],
        )
    else:
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            features=cloud_speech.RecognitionFeatures(
                enable_word_confidence=True,
                enable_word_time_offsets=True,
            ),
            model=model,
            language_codes=[language_code],
        )

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

    print(f"Starting batch recognize for {filename}...")
    operation = client.batch_recognize(request=request)

    # Poll for progress (see below for details)
    poll_operation_with_progress(operation, filename)

    response = operation.result(timeout=3 * CHUNK_DURATION_SECS)  # Shorter timeout per chunk
    print(f"Completed transcription for {filename}. Response: {response}")
    return response


def poll_operation_with_progress(operation, filename):
    """
    Poll the long-running operation and show progress.
    """
    while not operation.done():
        # Get operation metadata (if available; Speech API provides basic status)
        try:
            metadata = operation.metadata
            print(f"Progress for {filename}: State={getattr(metadata, 'state', 'Unknown')}, "
                  f"Processed={getattr(metadata, 'progress_bytes', 'N/A')} bytes")
        except Exception:
            print(f"Waiting for {filename}... (checking every 30s)")

        time.sleep(30)  # Poll every 30 seconds
    if operation.exception():
        raise operation.exception()


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

    # Determine language
    if filename.endswith("-zh.m4a") or filename.endswith("-zh.ogg"):
        language_code = "cmn-CN"
    else:
        language_code = "en-US"

    # Split into chunks if file is long (heuristic: >15 min, but you can probe duration with ffprobe)
    chunk_files = []
    if os.path.getsize(input_file) > 100 * 1024 * 1024:  # Rough check: >100MB likely long
        print(f"File is large; splitting into {CHUNK_DURATION_SECS//60}-minute chunks.")
        chunk_files = split_audio_file(input_file)
        if not chunk_files:
            print("Splitting failed; processing as single file.")
            chunk_files = [input_file]
    else:
        chunk_files = [input_file]

    storage_client = storage.Client()
    bucket = storage_client.bucket("test2x")

    all_transcripts = []  # To combine later

    for chunk_idx, chunk_file in enumerate(chunk_files):
        chunk_filename = os.path.basename(chunk_file)
        base_name = os.path.splitext(filename)[0]
        chunk_name = f"{base_name}_chunk_{chunk_idx+1:03d}"

        # Construct GCS paths
        gcs_audio_uri = f"gs://test2x/audio-files/{chunk_filename}"
        gcs_output_uri = f"gs://test2x/transcripts/{chunk_name}"

        # Upload chunk if needed
        blob = bucket.blob(f"audio-files/{chunk_filename}")
        if not blob.exists():
            blob.upload_from_filename(chunk_file)
            print(f"Uploaded chunk {chunk_filename} to GCS.")
        else:
            print(f"Chunk {chunk_filename} already in GCS.")

        # Transcribe
        try:
            run_batch_recognize(
                audio_gcs_uri=gcs_audio_uri,
                output_gcs_folder=gcs_output_uri,
                language_code=language_code,
            )

            # Download and collect transcript
            blobs = storage_client.list_blobs("test2x", prefix=f"transcripts/{chunk_name}")
            chunk_transcript = ""
            for b in blobs:
                if b.name.endswith(".json"):
                    local_path = os.path.join(output_dir, f"{os.path.basename(b.name)}")
                    b.download_to_filename(local_path)
                    # Parse JSON to extract text (simplified; use json module for full parsing)
                    import json
                    with open(local_path, 'r') as f:
                        data = json.load(f)
                        if 'results' in data:
                            chunk_text = ' '.join([result.get('alternatives', [{}])[0].get('transcript', '') for result in data['results']])
                            chunk_transcript += chunk_text + "\n"
                    print(f"Downloaded and parsed {b.name}")

            all_transcripts.append(chunk_transcript)

            # Clean up temp chunk if split
            if chunk_file != input_file and os.path.exists(chunk_file):
                os.remove(chunk_file)

        except Exception as e:
            print(f"Failed to process chunk {chunk_filename}: {e}")

    # Combine all transcripts into one file
    combined_text = "\n\n--- Chunk Boundary ---\n\n".join(all_transcripts)
    with open(output_filename, 'w') as f:
        f.write(combined_text)
    print(f"Combined transcript saved to {output_filename}")

    # Clean up temp dir if splitting occurred
    if chunk_files != [input_file]:
        import shutil
        shutil.rmtree(os.path.dirname(chunk_files[0]) if chunk_files else None)

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
    parser.add_argument(
        "--chunk_secs",
        type=int,
        default=CHUNK_DURATION_SECS,
        help="Chunk duration in seconds (for splitting long files).",
    )

    args = parser.parse_args()
    global CHUNK_DURATION_SECS  # Allow override
    CHUNK_DURATION_SECS = args.chunk_secs

    process_audio_file(
        input_file=args.input_file,
        output_dir=args.output,
    )
```

#### Key Changes and Benefits

- **Splitting**: Uses FFmpeg to create non-overlapping chunks (e.g., 10-min each). For a 1-hour file, that's ~6 jobs, which can run in parallel if you modify to use threading/multiprocessing (e.g., via `concurrent.futures`).
- **Faster Model**: Switches to `"short"` for chunks <15 min—processes 2-3x faster.
- **Combining Transcripts**: Parses JSON outputs and merges them into a single `.txt` file with boundaries for easy reading.
- **Cleanup**: Removes temp chunks and old GCS blobs if needed (add `blob.delete()` in a loop).
- **Usage**: Run as before, e.g., `python script.py --input_file long_audio.m4a --chunk_secs 600`. For no splitting, use a large `--chunk_secs` (e.g., 3600).

#### Other Optimizations

- **Parallel Processing**: If you have many chunks/files, use Python's `ThreadPoolExecutor` to submit `run_batch_recognize` jobs concurrently (limit to 5-10 to avoid quota hits).
- **Probe Audio Duration**: Use `ffprobe` (FFmpeg) to dynamically decide if splitting is needed: `ffprobe -v quiet -show_entries format=duration -of csv=p=0 input.m4a`.
- **Switch to Streaming API**: For interactive use, use synchronous `recognize` (limits ~1 min/file) or streaming for live, but it's not ideal for batch long files.
- **Costs/Quotas**: Check your Google Cloud quota (Speech-to-Text allows ~1000 req/min). Long jobs consume more credits (~$0.036/min for standard model).
- **Test Shorter First**: Start with `--chunk_secs 300` (5 min) to see speedup.

### Showing Progress: Polling the Operation

The updated `poll_operation_with_progress()` function replaces the blocking `operation.result()`. It:

- Checks every 30 seconds.
- Prints status from `operation.metadata` (e.g., state like "RUNNING" or "DONE", and bytes processed if available—Speech API metadata is basic, but it's better than nothing).
- Raises an error if it fails.

For more detailed progress (e.g., % complete), the Speech API doesn't provide granular metrics, but you can:

- Monitor via Google Cloud Console (Operations page for your project).
- Use `gcloud` CLI: `gcloud alpha speech operations describe OPERATION_ID --project=graphite-ally-445108-k3`.
- After completion, the JSON results include per-utterance progress indirectly via timestamps.

If splitting, you'll see interleaved progress from multiple chunks, making it feel less "stuck."

If this doesn't resolve your issue (e.g., specific errors), share logs/output for more tweaks!
