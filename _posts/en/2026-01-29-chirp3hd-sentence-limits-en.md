---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Chirp 3 HD Sentence Length Limits Explained
translated: false
type: note
---

Question: What is the limit for Chirp 3 HD voices in Google Cloud Text-to-Speech, especially regarding sentence length, and why does WaveNet not have this issue?

Answer:

**Chirp 3 HD voices** (the premium tier of Chirp 3 in Google Cloud Text-to-Speech) have a stricter internal limit on **maximum sentence length** compared to older models like WaveNet. This results in the error:

> 400 This request contains sentences that are too long. Consider splitting up long sentences with sentence ending punctuation e.g. periods.

This is **not** the same as the overall request character limit (which is typically ~5000 characters/bytes per synchronous request for most voices). Instead, it's a model-specific constraint on how long a single sentence (text between punctuation marks like periods, question marks, etc.) can be before the model refuses to process it or produces artifacts/errors.

### Key Limits Comparison

- **Overall request size (synchronous synthesizeSpeech)**
  ~5000 characters (including spaces, SSML tags count too) for most voices, including Chirp 3 HD and WaveNet.
  Exceeding this gives a different error (e.g., quota exceeded or payload too large).

- **Per-sentence length limit**
  - Chirp 3 HD (and many Neural2 / newer neural voices): Appears to enforce a much lower per-sentence threshold — often failing on sentences longer than roughly **200–500 characters** (exact threshold varies by language, voice, and content complexity).
    This is especially noticeable in languages like Japanese, Chinese, or when sentences contain long numbers, lists, or run-on structures.
    Workarounds:
    - Split long sentences with periods, question marks, or exclamation points.
    - Add line breaks or extra punctuation.
    - Break input into multiple shorter requests and concatenate audio.

  - WaveNet (older premium voices): Does **not** enforce this strict per-sentence limit (or enforces a much higher one).
    It can usually handle much longer individual sentences without the "sentences too long" error, which is why you see the issue only with Chirp 3 HD and not WaveNet.

- **Long-form synthesis** (asynchronous, via Long Audio Synthesis)
  Up to ~1 million characters total input (stored in GCS).
  However, user reports indicate Chirp 3 HD sometimes gets stuck or fails on moderately long inputs (e.g., 15k characters), while standard/WaveNet voices complete successfully.

### Why the Difference?

- Chirp 3 HD is a more advanced generative model optimized for naturalness, expressiveness, and low latency (especially in streaming/real-time use cases like Gemini Live).
- These models are more sensitive to input structure — very long sentences without breaks can lead to poor prosody, unstable generation, or internal processing failures (e.g., attention mechanisms or transformer context limits).
- To maintain high quality and avoid bad outputs, Google added a hard check that rejects overly long sentences in Chirp 3 HD.
- WaveNet (older concatenative/neural architecture) was more tolerant of long inputs but sounded less natural in many cases.

### Practical Advice (as of early 2026)

- For Chirp 3 HD: Keep individual sentences under ~300–400 characters when possible. Use punctuation aggressively for natural pauses.
- If you need very long uninterrupted text → fall back to WaveNet voices (if still available in your locale) or split synthesis requests.
- For very long content → use the long-form async API, but test thoroughly with Chirp 3 HD as stability isn't guaranteed for all voices/inputs.
- SSML support in Chirp 3 HD is limited (subset of tags), so you can't always use `<s>` or `<p>` to force breaks like in older models.

References:

- <https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd>
- <https://discuss.google.dev/t/this-request-contains-sentences-that-are-too-long-consider-splitting-up-long-sentences/130332>
- <https://calvincchan.com/blog/250531-google-tts-with-chirp3-hd-in-japanese>
- <https://discuss.google.dev/t/long-form-audio-does-not-work-with-chirp3-hd-voices/194335>
- <https://cloud.google.com/text-to-speech/quotas>
