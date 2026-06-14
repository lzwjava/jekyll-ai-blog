---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pyannote Segmentation 3.0 概述
translated: true
type: note
---

**问题：** Hugging Face 上的 `pyannote/segmentation-3.0` 是什么？

**答案：**

`pyannote/segmentation-3.0` 是一个**神经说话人分割模型** —— 它是 [pyannote.audio](https://github.com/pyannote/pyannote-audio) 说话人日志生态系统的基础。

### 它的功能

它接收 **10 秒单声道 16kHz 音频**，输出一个 `(num_frames, num_classes)` 矩阵，表示谁在什么时候说话。该架构采用 **powerset 多类编码** —— 不是为每个说话人设置独立的二分类标签，而是将所有说话人组合编码为一个多类问题：

| Class index | 含义 |
|---|---|
| 0 | 非语音 |
| 1 | 仅说话人 #1 |
| 2 | 仅说话人 #2 |
| 3 | 仅说话人 #3 |
| 4 | 说话人 #1 和 #2 重叠 |
| 5 | 说话人 #1 和 #3 重叠 |
| 6 | 说话人 #2 和 #3 重叠 |

每个片段最多 3 个说话人，最多 2 个同时活跃 —— 得到 `C(3,0)+C(3,1)+C(3,2) = 1+3+3 = 7` 个类别。

### 为什么 powerset 重要

传统的多标签说话人日志（每个说话人独立的 sigmoid）将说话人视为独立，难以正确建模互斥性和重叠。Powerset 将其转化为对所有有效说话人子集的 softmax —— 一个干净的交叉熵损失，对重叠有更好的校准。论文：[Plaquet & Bredin, INTERSPEECH 2023](https://www.isca-speech.org/archive/interspeech_2023/plaquet23_interspeech.html)。

### 训练数据

在 9 个数据集的混合上训练：AISHELL、AliMeeting、AMI、AVA-AVD、DIHARD、Ego4D、MSDWild、REPER E、VoxConverse —— 覆盖多种语言、领域和录音条件。

### 它的用途

该模型是一个**片段级分割原语**。它本身只处理 10 秒窗口。它被集成到：

- **[pyannote/speaker-diarization-3.1](https://hf.co/pyannote/speaker-diarization-3.1)** —— 添加说话人嵌入模型 + 聚类以处理全长录音
- **VAD** —— 语音活动检测管线
- **OSD** —— 重叠语音检测管线

### 快速使用

```python
from pyannote.audio import Model
from pyannote.audio.pipelines import VoiceActivityDetection

model = Model.from_pretrained(
    "pyannote/segmentation-3.0",
    use_auth_token="<HF_TOKEN>"
)

# 完整的说话人日志需要更高级的管线
# （仅此模型 = 仅 10 秒片段）
pipeline = VoiceActivityDetection(segmentation=model)
pipeline.instantiate({"min_duration_on": 0.0, "min_duration_off": 0.0})
vad = pipeline("audio.wav")  # pyannote.core.Annotation
```

### 对你的意义

如果你正在构建任何音频管线 —— 会议转录、说话人属性的 ASR（whisper + 说话人日志）、播客处理 —— 这是标准的开源入口点。它被用于 100 多个 HF Spaces，每月约 1370 万次下载。你会将其与 Whisper 配对，用于说话人属性的转录，这是处理语音录制的代理工具中的常见模式。

**参考文献：**

- [pyannote/segmentation-3.0 on HuggingFace](https://huggingface.co/pyannote/segmentation-3.0)
- [Plaquet & Bredin — Powerset multi-class cross entropy loss for neural speaker diarization (INTERSPEECH 2023)](https://www.isca-speech.org/archive/interspeech_2023/plaquet23_interspeech.html)
- [pyannote.audio GitHub](https://github.com/pyannote/pyannote-audio)