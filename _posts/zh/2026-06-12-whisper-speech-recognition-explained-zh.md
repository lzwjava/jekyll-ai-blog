---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper语音识别详解
translated: true
type: note
---

Whisper 是一个用于 speech recognition 的 encoder-decoder Transformer。以下是它的端到端工作方式：

== AUDIO -> TEXT PIPELINE ==

  1. AUDIO PREPROCESSING
     Raw audio (any format) → ffmpeg → 16kHz mono WAV
     然后计算 80-bin log-Mel spectrogram（30 秒片段）
     每个片段 → 3000 frames × 80 frequency bins

  2. ENCODER（处理音频）
     Mel spectrogram → 两个 1D conv 层 → positional embeddings
     → N 个 transformer blocks（self-attention + FFN）
     → 输出：audio embeddings 序列

  3. DECODER（生成文本）
     接收 encoder 输出 + 之前生成的 tokens
     → N 个 transformer blocks（masked self-attention + cross-attention to encoder + FFN）
     → 自回归地预测下一个 token

  4. SPECIAL TOKENS 驱动行为：
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

  一切都在 decoder prompt tokens 中：

  Transcribe Chinese:
    <|startoftranscript|><|zh|><|transcribe|><|0.00|> ...

  Translate to English:
    <|startoftranscript|><|es|><|translate|><|0.00|> ...

  模型在训练过程中学会了根据这些 tokens 进行条件生成。
  没有独立的语言分类器——只需输入 <|zh|> 即可执行中文识别。

== WHY IT'S ROBUST ==

  1. Scale: 在 680,000 小时的弱标注网络音频上训练
  2. Multitask: 单个模型同时完成 transcription、translation、lang ID
  3. Encoder-decoder: 与 CTC 模型（如 wav2vec）不同，它可以在每个解码步骤关注完整的 encoder 输出
  4. 30 秒片段带重叠 → 处理长音频
  5. 无需特定语言的预处理

== INFERENCE FLOW（调用 model.transcribe 时发生的过程）==

  1. ffmpeg 重采样为 16kHz mono
  2. 分割为 30s 片段（带重叠）
  3. 每个片段 → mel spectrogram → encoder → decoder beam search
  4. Decoder 生成 tokens: <|start|><|zh|><|transcribe|><|0.00|> 你好...<|end|>
  5. Tokens → 文本，从 <|timestamp|> tokens 中提取时间戳
  6. 片段通过词级对齐拼接在一起

关键洞察：Whisper 将语音识别视为一个 sequence-to-sequence 翻译问题——输入 audio tokens，输出 text tokens。"language" 和 "task" 只是 decoder 前缀中的特殊 tokens，而不是独立的模块。这就是单个模型自然处理 99 种语言的原因。
