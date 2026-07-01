---
audio: false
generated: true
image: false
lang: en
layout: post
title: Adding Speaker Diarization to Whisper
translated: false
type: note
---

**Question:** How to add speaker diarization (speaker labels) to my OpenAI Whisper transcription script?

**Answer:**

Your current script calls the `whisper` CLI directly — no diarization. Whisper itself has no speaker labeling built in. The standard approach is to pipe Whisper's output through a diarization pipeline. Two real options:

---

## Option 1: `pyannote.audio` + Whisper (most accurate, open-source)

This is the gold standard. `pyannote` does speaker diarization separately, then you align timestamps with Whisper segments.

### Architecture

```
audio → Whisper (segments + timestamps) → pyannote (speaker segments) → merge by timestamp overlap
```

### Install

```bash
pip install pyannote.audio openai-whisper
# Requires HuggingFace token — accept pyannote model license at:
# https://huggingface.co/pyannote/speaker-diarization-3.1
```

### Drop-in replacement for your script

```python
#!/usr/bin/env python3
"""
whisper_diarize.py — Whisper transcription with pyannote speaker labels
"""

import argparse
import os
import sys
import whisper
from pyannote.audio import Pipeline
import torch

def assign_speakers(diarization, whisper_segments):
    """
    For each Whisper segment, find the dominant speaker from pyannote diarization.
    Uses max overlap strategy.
    """
    results = []
    for seg in whisper_segments:
        seg_start, seg_end = seg["start"], seg["end"]
        speaker_times = {}

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            overlap_start = max(turn.start, seg_start)
            overlap_end = min(turn.end, seg_end)
            overlap = max(0, overlap_end - overlap_start)
            if overlap > 0:
                speaker_times[speaker] = speaker_times.get(speaker, 0) + overlap

        dominant = max(speaker_times, key=speaker_times.get) if speaker_times else "UNKNOWN"
        results.append({
            "start": seg_start,
            "end": seg_end,
            "speaker": dominant,
            "text": seg["text"].strip(),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Whisper + speaker diarization")
    parser.add_argument("input_file")
    parser.add_argument("--model", default="large")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--hf-token", required=True, help="HuggingFace token for pyannote")
    parser.add_argument("--num-speakers", type=int, default=None, help="Hint: number of speakers")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: {args.input_file} not found"); sys.exit(1)

    print(f"[1/3] Loading Whisper {args.model} on {args.device}...")
    model = whisper.load_model(args.model, device=args.device)

    print("[2/3] Transcribing...")
    result = model.transcribe(args.input_file, language=args.language, verbose=False)

    print("[3/3] Running speaker diarization...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=args.hf_token
    ).to(torch.device(args.device))

    diarize_kwargs = {}
    if args.num_speakers:
        diarize_kwargs["num_speakers"] = args.num_speakers

    diarization = pipeline(args.input_file, **diarize_kwargs)

    segments = assign_speakers(diarization, result["segments"])

    output_path = os.path.splitext(args.input_file)[0] + "_diarized.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            line = f"[{seg['start']:.1f}s → {seg['end']:.1f}s] {seg['speaker']}: {seg['text']}"
            print(line)
            f.write(line + "\n")

    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
```

**Usage:**

```bash
python whisper_diarize.py meeting.mp4 \
  --model large \
  --language Chinese \
  --device cuda \
  --hf-token hf_xxx \
  --num-speakers 2
```

---

## Option 2: `whisperx` (fastest, single package)

`whisperx` wraps Whisper + faster-whisper + pyannote into one CLI. Much simpler if you just want it to work.

```bash
pip install whisperx
```

```bash
whisperx meeting.mp4 \
  --model large-v3 \
  --language zh \
  --diarize \
  --hf_token hf_xxx \
  --output_dir ./out
```

Output includes a `_diarize.json` and `.txt` with `SPEAKER_00:`, `SPEAKER_01:` labels per segment.

To integrate into your existing script pattern:

```python
import subprocess

def run_whisperx(input_file, model="large-v3", language="zh", hf_token="hf_xxx", output_dir="."):
    cmd = [
        "whisperx", input_file,
        "--model", model,
        "--language", language,
        "--diarize",
        "--hf_token", hf_token,
        "--output_dir", output_dir,
        "--device", "cuda",
    ]
    subprocess.run(cmd, check=True)
```

`whisperx` also does **word-level alignment** using `wav2vec2` — much more accurate timestamps than vanilla Whisper, which matters for diarization boundary assignment.

---

## Comparison

| | pyannote DIY | whisperx |
| --- | --- | --- |
| Control | Full | Opinionated |
| Speed | Slow (2 passes) | Fast (faster-whisper backend) |
| Word alignment | Manual | Built-in |
| CLI-friendly | No | Yes |
| Custom diarization models | Yes | Partially |

---

## Key gotcha

Both require accepting the pyannote model license on HuggingFace:

- <https://huggingface.co/pyannote/speaker-diarization-3.1>
- <https://huggingface.co/pyannote/segmentation-3.0>

You need a HF account + `huggingface-cli login` or pass `--hf_token`.

---

**My recommendation for your setup:** Use `whisperx` on your RTX 4070 workstation. It's one command, faster-whisper backend is significantly faster than vanilla whisper for long meetings, and diarization is built-in. The `large-v3` model + CUDA should handle a 1-hour meeting in a few minutes.

**References:**

- [whisperx GitHub](https://github.com/m-bain/whisperX)
- [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [pyannote.audio docs](https://github.com/pyannote/pyannote-audio)
