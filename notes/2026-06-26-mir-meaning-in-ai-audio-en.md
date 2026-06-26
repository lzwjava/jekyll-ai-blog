---
audio: false
generated: true
image: false
lang: en
layout: post
title: MIR Meaning in AI Audio
translated: false
type: note
---

Question: What does MIR mean (in the context of AI audio)?

Answer:

In your friend's context — AI audio projects — **MIR** stands for **Music Information Retrieval**.

It's the interdisciplinary field focused on extracting meaningful information from music and audio signals. Core tasks include:

- **Pitch / melody extraction** — fundamental frequency (f0) estimation
- **Beat tracking & tempo estimation** — finding BPM and downbeats
- **Chord recognition & key detection**
- **Music transcription** — audio → MIDI/score
- **Genre / mood / instrument classification**
- **Source separation** — splitting vocals, drums, bass (e.g. Demucs, Spleeter)
- **Audio fingerprinting** — Shazam-style matching
- **Music recommendation & similarity**

Classic toolkit is `librosa` (Python). Modern MIR leans heavily on deep learning — CNNs on spectrograms/mel-spectrograms, and increasingly transformers and self-supervised audio encoders (e.g. MERT, Wav2Vec2 adapted to music).

So your friend is saying: "AI audio has landed in some real projects; I mainly work in the MIR direction" — i.e. they specialize in the music-analysis side rather than, say, speech (ASR/TTS) or generative audio.

Note there's an unrelated **MIR** in ML circles — **Mid-training / Mixed-precision** stuff doesn't apply here; and in robotics MIR can mean Mobile Industrial Robots. But given "AI音频," it's unambiguously Music Information Retrieval.
