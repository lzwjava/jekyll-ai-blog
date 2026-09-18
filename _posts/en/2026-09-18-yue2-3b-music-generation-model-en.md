---
audio: false
generated: true
image: false
lang: en
layout: post
title: YuE2-3B Music Generation Model
translated: false
type: note
---

**Question:** What is the YuE2-3B model, and what can it do?

**Answer:**

**YuE2-3B** is an open-source frontier music generation model developed by **m-a-p (Multimodal Art Projection)**. Here's a structured overview:

---

### 🎵 What It Is

YuE2-3B is a text-to-audio model supporting both Chinese and English, designed for music generation with symbolic planning and agentic editing capabilities. In the team's own words, YuE2 is an open music generation model with frontier song quality competitive with Suno v5/v6 — it turns lyrics and a style prompt into a complete song with vocals and accompaniment, then lets you shape its melody and chords through an editable score.

---

### 🏗️ Architecture

YuE2 uses a single AR–NAR (autoregressive / non-autoregressive) Mixture-of-Transformers backbone that writes a score and semantic tokens, then generates acoustic latents through flow matching. A VAE (Variational Autoencoder) then converts those latents into stereo audio.

---

### 🎛️ Key Capabilities

The model supports three main use cases: **text-to-music** (compose with melody + chords, melody-only, or direct generation), **cover song generation** (reimagine an existing recording in a new style), and **agentic editing** (turn musical feedback into score, style, and lyric revisions, then let YuE2 render the next version).

---

### ⚡ Performance

YuE2-3B can generate a 3.6-minute song in 71 seconds on an RTX 4090, using about 11 GiB of VRAM, with no quantization required. It runs on a 24GB GPU producing 48 kHz stereo audio.

---

### 📊 Benchmark Results

On WildSongBench (192 prompts), YuE2 (best-of-8) achieves a SongBench average of **6.9632**, surpassing Suno v5 (6.8721), Suno v6 (6.5562), and Suno v6 Wild (6.4195). This makes it the **top-ranked model** among both open and proprietary models evaluated on that benchmark.

---

### 📜 License

The model weights are released under **CC BY-NC 4.0** (non-commercial use).

---

**References:**
- [m-a-p/YuE2-3B · Hugging Face](https://huggingface.co/m-a-p/YuE2-3B)
- [YuE2 Demo Page](https://map-yue2.github.io/)
- [YuE Paper (arXiv:2503.08638)](https://arxiv.org/abs/2503.08638)
