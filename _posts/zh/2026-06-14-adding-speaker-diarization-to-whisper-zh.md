---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为Whisper添加说话人日志功能
translated: true
type: note
---

**问题：** 如何向我的 OpenAI Whisper 转录脚本添加说话人分离（说话人标签）？

**答案：**

你当前的脚本直接调用 `whisper` CLI —— 不包含说话人分离。Whisper 本身没有内置说话人标签功能。标准做法是将 Whisper 的输出通过一个说话人分离流水线。两个可行的方案：

---

## 选项 1：`pyannote.audio` + Whisper（最准确，开源）

这是黄金标准。`pyannote` 单独进行说话人分离，然后将时间戳与 Whisper 片段对齐。

### 架构

```
音频 → Whisper（片段 + 时间戳） → pyannote（说话人片段） → 按时间戳重叠合并
```

### 安装

```bash
pip install pyannote.audio openai-whisper
# 需要 HuggingFace token —— 在以下地址接受 pyannote 模型许可证：
# https://huggingface.co/pyannote/speaker-diarization-3.1
```

### 可直接替换你的脚本

```python
#!/usr/bin/env python3
"""
whisper_diarize.py — 带有 pyannote 说话人标签的 Whisper 转录
"""

import argparse
import os
import sys
import whisper
from pyannote.audio import Pipeline
import torch

def assign_speakers(diarization, whisper_segments):
    """
    对于每个 Whisper 片段，从 pyannote 的说话人分离结果中找到占比最大的说话人。
    使用最大重叠策略。
    """
    results = []
    for seg in whisper_segments:
        seg_start, seg_end = seg["start"], seg["end"]
        speaker_times = {}

        for turn, _, speaker in diarization.itertracks(yield_label=True):
            overlap_start = max(turn.start, seg_start)
            overlap_end = min(turn.end, seg_end)
            overlap = max(0, overlap_end - overlap_start)
            if overlap > 0:
                speaker_times[speaker] = speaker_times.get(speaker, 0) + overlap

        dominant = max(speaker_times, key=speaker_times.get) if speaker_times else "UNKNOWN"
        results.append({
            "start": seg_start,
            "end": seg_end,
            "speaker": dominant,
            "text": seg["text"].strip(),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="Whisper + 说话人分离")
    parser.add_argument("input_file")
    parser.add_argument("--model", default="large")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--hf-token", required=True, help="用于 pyannote 的 HuggingFace token")
    parser.add_argument("--num-speakers", type=int, default=None, help="提示：说话人数量")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"Error: {args.input_file} not found"); sys.exit(1)

    print(f"[1/3] 正在加载 Whisper {args.model} 于 {args.device}...")
    model = whisper.load_model(args.model, device=args.device)

    print("[2/3] 正在转录...")
    result = model.transcribe(args.input_file, language=args.language, verbose=False)

    print("[3/3] 正在运行说话人分离...")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=args.hf_token
    ).to(torch.device(args.device))

    diarize_kwargs = {}
    if args.num_speakers:
        diarize_kwargs["num_speakers"] = args.num_speakers

    diarization = pipeline(args.input_file, **diarize_kwargs)

    segments = assign_speakers(diarization, result["segments"])

    output_path = os.path.splitext(args.input_file)[0] + "_diarized.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            line = f"[{seg['start']:.1f}s → {seg['end']:.1f}s] {seg['speaker']}: {seg['text']}"
            print(line)
            f.write(line + "\n")

    print(f"\n已保存到 {output_path}")


if __name__ == "__main__":
    main()
```

**用法：**

```bash
python whisper_diarize.py meeting.mp4 \
  --model large \
  --language Chinese \
  --device cuda \
  --hf-token hf_xxx \
  --num-speakers 2
```

---

## 选项 2：`whisperx`（最快，单一包）

`whisperx` 将 Whisper + faster-whisper + pyannote 整合为一个 CLI。如果你只想让它工作，更简单。

```bash
pip install whisperx
```

```bash
whisperx meeting.mp4 \
  --model large-v3 \
  --language zh \
  --diarize \
  --hf_token hf_xxx \
  --output_dir ./out
```

输出包含一个 `_diarize.json` 和带有 `SPEAKER_00:`、`SPEAKER_01:` 标签的 `.txt` 文件，每个片段都有标注。

要集成到你现有的脚本模式中：

```python
import subprocess

def run_whisperx(input_file, model="large-v3", language="zh", hf_token="hf_xxx", output_dir="."):
    cmd = [
        "whisperx", input_file,
        "--model", model,
        "--language", language,
        "--diarize",
        "--hf_token", hf_token,
        "--output_dir", output_dir,
        "--device", "cuda",
    ]
    subprocess.run(cmd, check=True)
```

`whisperx` 还使用 `wav2vec2` 进行**词级对齐** —— 时间戳比原始 Whisper 精确得多，这对说话人分离边界分配很重要。

---

## 比较

| | pyannote DIY | whisperx |
|---|---|---|
| 控制度 | 完全 | 固定 |
| 速度 | 慢（两次处理） | 快（faster-whisper 后端） |
| 词级对齐 | 手动 | 内置 |
| CLI 友好 | 否 | 是 |
| 自定义分离模型 | 是 | 部分 |

---

## 关键注意点

两者都需要在 HuggingFace 上接受 pyannote 模型许可证：

- <https://huggingface.co/pyannote/speaker-diarization-3.1>
- <https://huggingface.co/pyannote/segmentation-3.0>

你需要一个 HF 账号 + 运行 `huggingface-cli login` 或传递 `--hf_token`。

---

**我的建议（针对你的配置）：** 在你的 RTX 4070 工作站上使用 `whisperx`。只需一个命令，faster-whisper 后端对于长时间会议比原始 Whisper 快得多，并且内置了说话人分离。`large-v3` 模型 + CUDA 应该能在几分钟内处理 1 小时的会议。

**参考：**

- [whisperx GitHub](https://github.com/m-bain/whisperX)
- [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [pyannote.audio docs](https://github.com/pyannote/pyannote-audio)
