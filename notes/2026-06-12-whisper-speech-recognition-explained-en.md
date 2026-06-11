---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whisper Speech Recognition Explained
translated: false
type: note
---

Whisper is an encoder-decoder Transformer trained for speech recognition. Here's how it works end-to-end:

== AUDIO -> TEXT PIPELINE ==

  1. AUDIO PREPROCESSING
     Raw audio (any format) → ffmpeg → 16kHz mono WAV
     Then compute 80-bin log-Mel spectrogram (30-second chunks)
     Each chunk → 3000 frames × 80 frequency bins

  2. ENCODER (processes audio)
     Mel spectrogram → two 1D conv layers → positional embeddings
     → N transformer blocks (self-attention + FFN)
     → output: sequence of audio embeddings

  3. DECODER (generates text)
     Takes encoder output + previously generated tokens
     → N transformer blocks (masked self-attention + cross-attention to encoder + FFN)
     → predicts next token autoregressively

  4. SPECIAL TOKENS drive behavior:
     <|startoftranscript|> <|lang|> <|task|> <|timestamp|> ... <|endoftext|>

== ARCHITECTURE DETAILS ==

  Input: 80-dim log-Mel spectrogram (30s chunks)
         ↓
  Conv1D: 1×1 stride, 384 filters → Conv1D: 1×1 stride, 384 filters
         ↓
  Sinusoidal positional encoding
         ↓
  Encoder: N transformer blocks
    Each block:
      LayerNorm → Multi-Head Self-Attention → Residual
      LayerNorm → FFN (384 → 1536 → 384) → Residual
         ↓
  Decoder: N transformer blocks
    Each block:
      LayerNorm → Masked Self-Attention → Residual
      LayerNorm → Cross-Attention (to encoder) → Residual
      LayerNorm → FFN → Residual
         ↓
  Linear + Softmax → next token probability

== MODEL SIZES ==

  Model    Encoder  Decoder  d_model  Layers  Heads
  tiny       4        4       384       4       6
  base       6        6       512       6       8
  small     12       12       768      12      12
  medium    24       24      1024      24      16
  large     32       32      1280      32      20
  turbo     32        4      1280      32      20  ← encoder-heavy

== HOW LANGUAGE/TASK SELECTION WORKS ==

  It's all in the decoder prompt tokens:

  Transcribe Chinese:
    <|startoftranscript|><|zh|><|transcribe|><|0.00|> ...

  Translate to English:
    <|startoftranscript|><|es|><|translate|><|0.00|> ...

  The model learned during training to condition on these tokens.
  No separate language classifier — just feed <|zh|> and it does Chinese.

== WHY IT'S ROBUST ==

  1. Scale: trained on 680,000 hours of weakly-labeled web audio
  2. Multitask: one model does transcription, translation, lang ID
  3. Encoder-decoder: unlike CTC models (wav2vec), it can attend to
     the full encoder output at each decoding step
  4. 30-second chunks with overlap → handles long audio
  5. No language-specific preprocessing needed

== INFERENCE FLOW (what happens when you call model.transcribe) ==

  1. ffmpeg resamples to 16kHz mono
  2. Split into 30s chunks (with overlap)
  3. Each chunk → mel spectrogram → encoder → decoder beam search
  4. Decoder generates tokens: <|start|><|zh|><|transcribe|><|0.00|> 你好...<|end|>
  5. Tokens → text, timestamps extracted from <|timestamp|> tokens
  6. Chunks stitched together with word-level alignment

Key insight: Whisper treats speech recognition as a sequence-to-sequence translation problem — audio tokens in, text tokens out. The "language" and "task" are just special tokens in the decoder prefix, not separate modules. This is why one model handles 99 languages naturally.
