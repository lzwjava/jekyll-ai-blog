---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenAI Whisper：语音识别模型
translated: true
type: note
---

这是 **OpenAI 的 Whisper**——一个通用的语音识别模型和代码库。具体来说：

**功能**
- **多语种语音识别**（支持99种语言）转写为文本
- **语音翻译**（非英语语音 → 英语文本）
- **语言识别**和语音活动检测
- 所有功能均由单个 Transformer 序列到序列模型处理，使用特殊标记作为任务指示符（参见仓库中的 `approach.png` / `language-breakdown.svg`）

**关键信息**
- 使用 OpenAI 的 `tiktoken` 分词器、PyTorch，并依赖 `ffmpeg` 进行音频解码
- 提供 **6 种模型尺寸**：`tiny`、`base`、`small`、`medium`、`large` 和 `turbo`（优化的 `large-v3`），部分有纯英文变体（如 `tiny.en`）
- 可通过命令行（`whisper audio.mp3 --model turbo`）或作为 Python 包（`whisper.load_model(...)` / `transcribe`）使用

**代码结构**（`whisper/` 目录，约 14 个源文件）：
- `model.py` — Transformer 模型定义
- `transcribe.py` — 转录流水线（分段、VAD 风格检测）
- `decoding.py` — 束搜索/贪婪解码及 logit 处理
- `audio.py` — 通过 ffmpeg 加载音频
- `tokenizer.py` — 分词器设置
- `timing.py` — 词级时间戳（基于 DTW）
- `triton_ops.py` — 可选的 NVIDIA Triton CUDA 内核以加速

**仓库状态**
- `main` 分支工作树干净，与 `origin/main` 同步
- 最近的提交包括 JSONL 输出支持、针对束搜索的 SDPA 交叉注意力修复，以及 `torch.load` 的安全修复（`weights_only=True`）——此外还有一个 `Release 20250625` 标签
- 还包含测试、笔记本（例如 LibriSpeech 示例）和模型卡片

这是官方的 OpenAI Whisper 代码库（MIT 许可证），可直接用于语音转文本任务。