---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pyannote Segmentation 3.0 Overview
translated: false
type: note
---

**Question:** What is `pyannote/segmentation-3.0` on Hugging Face?

**Answer:**

`pyannote/segmentation-3.0` is a **neural speaker segmentation model** — the backbone of the [pyannote.audio](https://github.com/pyannote/pyannote-audio) diarization ecosystem.

### What it does

It takes **10 seconds of mono audio at 16kHz** and outputs a `(num_frames, num_classes)` matrix representing who's speaking when. The architecture uses **powerset multi-class encoding** — instead of independent binary labels per speaker, it encodes all speaker combinations as a single multi-class problem:

| Class index | Meaning |
|---|---|
| 0 | Non-speech |
| 1 | Speaker #1 only |
| 2 | Speaker #2 only |
| 3 | Speaker #3 only |
| 4 | Speakers #1 and #2 overlap |
| 5 | Speakers #1 and #3 overlap |
| 6 | Speakers #2 and #3 overlap |

Max 3 speakers per chunk, max 2 simultaneously active — gives you `C(3,0)+C(3,1)+C(3,2) = 1+3+3 = 7` classes.

### Why powerset matters

Traditional multi-label diarization (separate sigmoid per speaker) treats speakers independently, making it hard to model mutual exclusivity and overlaps correctly. Powerset turns it into a softmax over all valid speaker subsets — one clean cross-entropy loss, better calibration for overlaps. The paper: [Plaquet & Bredin, INTERSPEECH 2023](https://www.isca-speech.org/archive/interspeech_2023/plaquet23_interspeech.html).

### Training data

Trained on a mix of 9 datasets: AISHELL, AliMeeting, AMI, AVA-AVD, DIHARD, Ego4D, MSDWild, REPERE, VoxConverse — broad coverage across languages, domains, and recording conditions.

### What it's used for

This model is a **chunk-level segmentation primitive**. By itself it only handles 10s windows. It's plugged into:

- **[pyannote/speaker-diarization-3.1](https://hf.co/pyannote/speaker-diarization-3.1)** — adds a speaker embedding model + clustering to handle full-length recordings
- **VAD** — voice activity detection pipeline
- **OSD** — overlapped speech detection pipeline

### Quick usage

```python
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection

model = Model.from_pretrained(
    "pyannote/segmentation-3.0",
    use_auth_token="<HF_TOKEN>"
)

# Full diarization needs the higher-level pipeline
# (this model alone = 10s chunks only)
pipeline = VoiceActivityDetection(segmentation=model)
pipeline.instantiate({"min_duration_on": 0.0, "min_duration_off": 0.0})
vad = pipeline("audio.wav")  # pyannote.core.Annotation
```

### Relevance for you

If you're building any audio pipeline — meeting transcription, speaker-attributed ASR (whisper + diarization), podcast processing — this is the standard open-source entry point. It's used in 100+ HF Spaces and gets ~13.7M downloads/month. You'd pair it with Whisper for speaker-attributed transcription, which is a common pattern in agent tools that process voice recordings.

**References:**

- [pyannote/segmentation-3.0 on HuggingFace](https://huggingface.co/pyannote/segmentation-3.0)
- [Plaquet & Bredin — Powerset multi-class cross entropy loss for neural speaker diarization (INTERSPEECH 2023)](https://www.isca-speech.org/archive/interspeech_2023/plaquet23_interspeech.html)
- [pyannote.audio GitHub](https://github.com/pyannote/pyannote-audio)
