---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用OpenAI Whisper转录MP4
translated: true
type: note
---

`ww main.py` 中尚未集成转录命令。现有的 `ww/audio/speech_to_text.py` 使用 Google Cloud Speech-to-Text 并借助 GCS 上传——对于一次性本地文件来说过于笨重。

对于一个 2 小时的 MP4 文件，最简单的方案是 **OpenAI Whisper**（本地、免费、无需云配置）：

```bash
# 一次安装
pip install openai-whisper

# 运行（large 模型精度最高，CPU 上约需 10-20 分钟）
whisper ~/Downloads/your-video.mp4 --model large --output_dir ~/Downloads
```

或者，如果你希望工具包内置一个 `ww transcribe` 命令（使用 Whisper 或 OpenAI Whisper API），我可以添加一个。你更倾向于哪种方式？