---
audio: false
generated: true
image: false
lang: en
layout: post
title: SPGISpeech Dataset Overview
translated: false
type: note
---

Question: Give an introduction to the SPGISpeech dataset on Hugging Face (`kensho/spgispeech`).

Answer:

## What it is

SPGISpeech is a corpus of 5,000 hours of professionally-transcribed financial audio, containing company earnings calls, released by Kensho Technologies (an S&P Global subsidiary) and published via the [SPGISpeech paper](https://arxiv.org/abs/2104.02014) (O'Neill et al., 2021). It's the standard "formal business speech" benchmark in the ASR world — it's one of the 8 datasets in the Hugging Face **ESB (End-to-end Speech Benchmark)** and shows up in `hf-audio/open_asr_leaderboard`, so any Whisper/Conformer/wav2vec2 paper you read likely reports WER on it.

## Why it's interesting for ASR training

- Transcripts are fully formatted — capitalization, punctuation, and denormalization of non-standard words (e.g. "twenty seventeen" → "2017", "$5 million" stays as digits+symbol). This is the key differentiator vs. LibriSpeech-style lowercase-no-punctuation corpora — it trains a model to output publish-ready text, not just phonetic transcription.
- Approximately 50,000 speakers — huge speaker diversity, a broad cross-section of L1 and L2 English accents, mixed spontaneous (Q&A) and narrated (prepared remarks) speech.
- Original calls were split into slices ranging from 5 to 15 seconds using Gentle, a double-pass forced aligner, boundaries refined with py-webrtc voice activity detection. Audio format: single channel, 16kHz, 16 bit — matches what Whisper/wav2vec2/Conformer expect natively.
- Known bias: close to 90% of speakers are male — expected on earnings calls (execs skew male), worth knowing before you eval fairness. Also domain is formal/scripted, so needs augmentation if you want a model that handles informal speech.

## Gotchas

1. **Gated dataset.** You must accept Kensho's Terms of Usage on the HF page before `load_dataset` will work — it's not a simple click-through, it's a legal agreement restricting redistribution and re-identification attempts. Once accepted, standard HF auth (`huggingface-cli login` or `HF_TOKEN` env var) unlocks the download.
2. **Size.** Total is 781 GB, but there are three train configs so you don't have to pull it all:

| Subset | Size |
|---|---|
| S | 22GB |
| M | 107GB |
| L | 530GB (superset of M, which is superset of S) |
| dev | 11GB |
| test | 11GB |

## Minimal usage

```python
from datasets import load_dataset

# S config for quick iteration/fine-tuning experiments
spgi = load_dataset("kensho/spgispeech", "S")

sample = spgi["train"][0]
audio_array = sample["audio"]["array"]     # np.float32, 16kHz mono
sampling_rate = sample["audio"]["sampling_rate"]
transcript = sample["transcript"]

# dev/test only, without pulling any train split
spgi_test = load_dataset("kensho/spgispeech", "test")
```

Given your training work on GPT-2/MoE from scratch, this dataset is a decent choice if you ever want to fine-tune or eval a Whisper/Conformer-style encoder-decoder on formatted-text ASR — the punctuation/capitalization requirement makes the task strictly harder than raw phoneme transcription, closer to what a production dictation or meeting-transcription product needs.

References:

- [kensho/spgispeech dataset card](https://huggingface.co/datasets/kensho/spgispeech)
- [SPGISpeech paper (arXiv:2104.02014)](https://arxiv.org/abs/2104.02014)
