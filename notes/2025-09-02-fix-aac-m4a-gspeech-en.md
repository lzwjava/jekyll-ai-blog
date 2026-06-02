---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix AAC M4A for Google Speech API
translated: false
type: note
---

Yep—your file is **AAC in an M4A container** (iPhone Voice Memos). Google Speech-to-Text v2 Batch often fails to auto-decode AAC/M4A and returns that exact error. Convert to a supported codec/container first—then either keep `AutoDetectDecodingConfig()` or (better) specify the decoding explicitly.

Here’s the quickest path.

## Option A — One-liner fix with `ffmpeg` (recommended: Ogg/Opus)

Small files, great accuracy, officially supported.

```bash
# 48 kHz, mono, Opus in OGG
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 48000 -c:a libopus -b:a 48k ~/Downloads/haifeng_and_zhiwei.ogg
```

Then run your script on the new file:

```bash
python scripts/agent/speech_to_text_agent.py --input_file ~/Downloads/haifeng_and_zhiwei.ogg
```

## Option B — Lossless FLAC (also supported)

Smaller than WAV; lossless.

```bash
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 48000 -sample_fmt s16 -c:a flac ~/Downloads/haifeng_and_zhiwei.flac
```

## Option C — Linear16 WAV (largest file)

```bash
ffmpeg -i ~/Downloads/haifeng_and_zhiwei.m4a -vn -ac 1 -ar 16000 -sample_fmt s16 -c:a pcm_s16le ~/Downloads/haifeng_and_zhiwei.wav
```

---

## Code tweaks (so you never hit this again)

1. **Allow more extensions** and pick language from suffix the same way.
2. **Transcode automatically** to a supported format (I use Ogg/Opus).
3. **Tell the API exactly what you’re sending** (explicit decoding).

Drop this into your script (minimal, focused changes):

```python
import subprocess
import tempfile
from pathlib import Path
from google.cloud.speech_v2.types import cloud_speech

SUPPORTED_EXTS = {".ogg", ".flac", ".wav", ".mp3"}  # mp3 is supported too

def _transcode_to_ogg_opus(src_path: str) -> str:
    src = Path(src_path)
    dst = src.with_suffix(".ogg")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(src),
        "-vn",
        "-ac", "1",
        "-ar", "48000",
        "-c:a", "libopus",
        "-b:a", "48k",
        str(dst),
    ]
    subprocess.run(cmd, check=True)
    return str(dst)

def run_batch_recognize(audio_gcs_uri, output_gcs_folder, language_code="en-US", decoding="ogg_opus"):
    client = SpeechClient()

    # Prefer explicit decoding — avoids "unsupported encoding" surprises
    if decoding == "ogg_opus":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            ogg_opus=cloud_speech.OggOpusDecodingConfig()
        )
    elif decoding == "flac":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            flac=cloud_speech.FlacDecodingConfig()
        )
    elif decoding == "linear16":
        decoding_cfg = cloud_speech.ExplicitDecodingConfig(
            linear16=cloud_speech.Linear16DecodingConfig()
        )
    else:
        decoding_cfg = cloud_speech.AutoDetectDecodingConfig()  # fallback

    config = cloud_speech.RecognitionConfig(
        explicit_decoding_config=decoding_cfg,
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
        language_codes=[language_code],
        # Optional: diarization, punctuation, etc.
        # speech_adaptation=...
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
    print("Waiting for operation to complete...")
    response = client.batch_recognize(request=request).result(timeout=3 * MAX_AUDIO_LENGTH_SECS)
    print(response)

def process_audio_file(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    src = Path(input_file)
    if not src.exists():
        print(f"Error: {src} does not exist.")
        return

    # Decide language by suffix
    language_code = "cmn-CN" if src.name.endswith("-zh" + src.suffix) else "en-US"

    # Ensure supported encoding/container
    if src.suffix.lower() not in SUPPORTED_EXTS:
        print(f"Transcoding {src.name} to Ogg/Opus...")
        input_file = _transcode_to_ogg_opus(str(src))
        src = Path(input_file)

    # Output gating for your local .txt (you can keep as-is or key off stem)
    output_filename = os.path.join(output_dir, f"{src.stem}.txt")
    if os.path.exists(output_filename):
        print(f"Skipping {src.name}: {output_filename} already exists.")
        return

    print(f"Processing: {src.name}")

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket("test2x")
        # Keep folder "audio-files/", keep real filename with new extension
        blob = bucket.blob(f"audio-files/{src.name}")
        if not blob.exists():
            blob.upload_from_filename(str(src))
            print(f"Uploaded {src.name} to GCS.")
        else:
            print(f"{src.name} already exists in GCS.")

        gcs_audio_uri = f"gs://test2x/audio-files/{src.name}"
        gcs_output_uri = f"gs://test2x/transcripts/{src.stem}"

        # Pick decoding based on extension
        ext = src.suffix.lower()
        if ext == ".ogg":
            decoding = "ogg_opus"
        elif ext == ".flac":
            decoding = "flac"
        elif ext == ".wav":
            decoding = "linear16"
        else:
            decoding = None  # fall back to autodetect

        run_batch_recognize(
            audio_gcs_uri=gcs_audio_uri,
            output_gcs_folder=gcs_output_uri,
            language_code=language_code,
            decoding=decoding,
        )

        print(f"File {src.name} processed.\n")

        # Download the transcription JSONs
        blobs = storage_client.list_blobs("test2x", prefix=f"transcripts/{src.stem}")
        for b in blobs:
            if b.name.endswith(".json"):
                local_output_path = os.path.join(output_dir, os.path.basename(b.name))
                b.download_to_filename(local_output_path)
                print(f"Downloaded {b.name} to {local_output_path}")

    except Exception as e:
        print(f"Failed to process {src.name}: {e}")

    print(f"Processing complete for {src.name}.")
```

### Why this works

* iOS Voice Memos → **AAC/M4A**. Batch STT v2 doesn’t reliably autodetect/decode that.
* By transcoding to **OGG/Opus** (or **FLAC/WAV**) and **telling the API the codec**, you avoid the “unsupported encoding” error entirely.

### Practical tips

* For long recordings like your **1h21m mono voice memo**, **OGG/Opus 48k** keeps quality while shrinking size and GCS egress.
* Keep mono (`-ac 1`). Stereo just doubles cost without helping recognition.
* If the conversation is Mandarin, your `"cmn-CN"` code is fine; use `"-zh.m4a"` naming convention as you already do.
* If you need speaker turns, enable diarization later; fix the decode path first.

If you want, I can also add optional **automatic local → GCS upload + re-naming** so your `m4a` input is accepted but always processed as an internal `.ogg` behind the scenes.
