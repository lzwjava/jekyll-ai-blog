---
audio: false
generated: true
image: false
lang: en
layout: post
title: Download Speed During Whisper Model Re-download
translated: false
type: note
---

Question: How do I understand the download speed shown in the Whisper large-v3 model re-download progress on an RTX 4070?

Answer:

## What's Actually Happening

What you're seeing is **not GPU transcription speed** — it's a **model file re-download**. Here's why:

```
UserWarning: /home/lzw/.cache/whisper/large-v3.pt exists,
but the SHA256 checksum does not match; re-downloading the file
```

The previously cached `large-v3.pt` file is **corrupted or incomplete**, so Whisper is re-downloading it from the internet. The `6.42 MiB/s` is your **internet download speed**, not GPU speed.

---

## Breaking Down the Progress Bar

```
38%|████████████████                     | 1.09G/2.88G [01:45<04:57, 6.42MiB/s]
```

| Field | Value | Meaning |
|---|---|---|
| `38%` | Progress | 38% of the file downloaded |
| `1.09G / 2.88G` | Bytes | Downloaded 1.09 GB out of 2.88 GB total |
| `01:45` | Elapsed | 1 min 45 sec elapsed |
| `04:57` | Remaining | ~5 minutes left |
| `6.42 MiB/s` | Speed | ~6.42 MB/s internet download speed |

The `large-v3` model file is **2.88 GB** — that's the full model weight checkpoint.

---

## What to Do After Download Completes

Once the download finishes, Whisper will start actual transcription on your **RTX 4070**, which is a very capable GPU for this task. Benchmarks show the RTX 4070 has the best price-to-performance ratio for Whisper transcription among comparable GPUs.

You can expect roughly **15–30x real-time speed** with `large` model on an RTX 4070 (e.g., a 60-minute audio file transcribed in 2–4 minutes).

---

## How to Avoid This Problem Next Time

The checksum mismatch usually means the previous download was interrupted. To prevent re-downloads:

1. **Let the download fully complete** without interruption.
2. Or pre-download the model manually and verify integrity:

```bash
# Check if the file is complete after download
ls -lh ~/.cache/whisper/large-v3.pt
# Should be ~2.88 GB
```

---

## Bonus: Use `faster-whisper` for Better Speed

If you want significantly faster transcription on your RTX 4070, consider switching to `faster-whisper`:

```bash
pip install faster-whisper
```

Faster-whisper uses CTranslate2 and can automatically download the model from Hugging Face Hub when loading by size, supporting `float16` quantization for better GPU performance.

References:

- [Performance benchmark of different GPUs · openai/whisper · Discussion #918](https://github.com/openai/whisper/discussions/918)
- [GitHub - SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)