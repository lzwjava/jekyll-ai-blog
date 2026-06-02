---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Comparing Google Cloud Speech-to-Text Models
translated: false
type: note
---

Here’s a clear breakdown of the differences between the various Speech-to-Text models in Google Cloud’s API V2—organized by model family and use case, without tables to keep it readable:

---

## Chirp Family (Universal Speech Models - USM)

### **`chirp`**

* **What it is**: Google’s original Universal Speech Model (USM), supporting diverse multilingual transcription in non-streaming contexts.([Google Cloud][1])
* **Usage**: Works with synchronous (`Recognize`) and batch (`BatchRecognize`) methods; does **not** support streaming.([Google Cloud][1])
* **Limitations**:

  * No streaming support
  * Lacks confidence scores, diarization, adaptation, forced normalization, and word-level confidence([Google Cloud][1])

### **`chirp_2`**

* **What it is**: Next-gen Universal Speech Model, more accurate and efficient than the original, with streaming, synchronous, and batch support. Offers multilingual transcription and translation, as well as model adaptation.([Google Cloud][2], [Medium][3])

### **`chirp_3`**

* **What it is**: The latest generation with further improvements in accuracy and speed. Supports streaming, synchronous, and batch recognition, plus speaker diarization and automatic language detection.([Google Cloud][4])
* **Feature support**:

  * Streaming (`StreamingRecognize`), synchronous (`Recognize`), and batch (`BatchRecognize`) all supported([Google Cloud][4])
  * Supports diarization and language detection([Google Cloud][4])
  * Doesn’t support word-level timestamps or adaptation([Google Cloud][4])

---

## Legacy / General-Purpose Models

These are older architecture models maintained primarily for backward compatibility:

* **`long`**: Good for long-form content like media or spontaneous conversations.([Google Cloud][2])
* **`short`**: Optimized for very short utterances (a few seconds)—ideal for commands.([Google Cloud][2])
* **`telephony` / `telephony_short`**: Tailored for phone-call audio (typically 8kHz). The “short” variant handles short or single-word utterances.([Google Cloud][2])
* **Medical models**:

  * `medical_conversation`: For dialogs between provider and patient, with speaker separation.
  * `medical_dictation`: For single-speaker dictated notes.([Google Cloud][2])

---

## Summary of Model Differences by Use Case

* **Need best accuracy in non-streaming, multilingual?** → **`chirp`**
* **Need streaming support + multilingual + adaptation?** → **`chirp_2`**
* **Want streaming, diarization, auto-language detection, and highest accuracy?** → **`chirp_3`**
* **Just simple long content transcription?** → **`long`**
* **Processing short spoken commands?** → **`short`**
* **Phone call recordings?** → **`telephony`** or **`telephony_short`**
* **Medical use cases?** → **`medical_conversation`** or **`medical_dictation`**

---

## Context from the Google Documentation

Google’s "Select a transcription model" page (updated September 4, 2025) includes all of the above model identifiers and descriptions. It also notes that the legacy models are not actively maintained but retained for backward compatibility.([Google Cloud][2])

And an earlier note about “latest\_long” / “latest\_short” refers to another set of conformer-based models—but these are outside the Chirp lineage and not relevant if you're focused specifically on the Chirp or legacy models.([Google Cloud][5])

---

## TL;DR—How to Pick

* **Highest quality + new features (diarization, streaming, etc.)** → **`chirp_3`**
* **Streaming & model adaptation support** → **`chirp_2`**
* **Non-streaming multilingual baseline** → **`chirp`**
* **Short utterances, long audio, phone, medical** → use appropriate legacy model (`short`, `long`, `telephony`, `medical_*`)

---

Let me know if you'd like help choosing the right model based on your specific audio type, language, or need streaming vs batch processing!

[1]: https://cloud.google.com/speech-to-text/v2/docs/chirp-model?utm_source=chatgpt.com "Chirp: Universal speech model"
[2]: https://cloud.google.com/speech-to-text/v2/docs/transcription-model?utm_source=chatgpt.com "Select a transcription model - Cloud Speech-to-Text"
[3]: https://medium.com/google-cloud/transcribe-everything-everywhere-all-at-once-with-chirp-2-615ac362947d?utm_source=chatgpt.com "Transcribe everything everywhere all at once with Chirp 2"
[4]: https://cloud.google.com/speech-to-text/v2/docs/chirp_3-model?utm_source=chatgpt.com "Chirp 3 Transcription: Enhanced multilingual accuracy"
[5]: https://cloud.google.com/speech-to-text/docs/latest-models?utm_source=chatgpt.com "Introduction to Latest Models | Cloud Speech-to-Text ..."
