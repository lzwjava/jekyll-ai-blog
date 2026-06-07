---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI视频字幕自动生成管道
translated: true
type: note
---

问题：如何使用 AI 工具为 `smart-auto` 演示改进视频字幕工作流程，而不是手动使用 CapCut 制作字幕？

答案：

你当前的瓶颈在于手动使用 CapCut 制作字幕。以下是原生 AI 工作流程：

## 改进后的工作流程

```
脚本 → ElevenLabs 音频 → Whisper（自动字幕）→ FFmpeg 同步 → CapCut 最终润色
```

**三大关键改进：**

### 1. **使用 Whisper 自动生成字幕（替代手动 CapCut）**

在本地 RTX 4070 上使用 OpenAI Whisper：

```bash
# 安装
pip install openai-whisper ffmpeg-python

# 从 ElevenLabs 音频生成 VTT 字幕
whisper your_audio.mp3 --model base --output_format vtt --language en
```

输出：`your_audio.vtt` 文件，带时间戳。零成本，典型视频在本地运行约 30 秒。

**为什么这比手动更好：** 对于清晰的音频（ElevenLabs 输出很干净），Whisper 的准确率超过 99%。你可以自动获得完美同步的 SRT/VTT 字幕。处理 5 分钟视频仅需 2 分钟。

### 2. **使用 FFmpeg 自动将字幕嵌入视频**

```python
import subprocess
import json

def embed_captions(video_path, caption_path, output_path):
    """将 VTT 字幕嵌入视频，无需重新编码"""
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={caption_path}",
        '-c:v', 'libx264',
        '-preset', 'fast',  # RTX 4070，如果愿意也可用硬件编码
        '-c:a', 'aac',
        output_path
    ]
    subprocess.run(cmd, check=True)

# 或使用硬件编码（在 RTX 4070 上更快）：
# '-c:v', 'hevc_nvenc'  # 用于 4070 的 NVIDIA NVENC
```

这样直接嵌入字幕，这一步不再需要 CapCut。**5 分钟视频：约 30 秒**。

### 3. **完整的流水线脚本**

```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def generate_captions(audio_path: str) -> str:
    """Whisper：音频 → VTT"""
    result = subprocess.run(
        ['whisper', audio_path, '--model', 'base', '--output_format', 'vtt'],
        capture_output=True,
        text=True
    )
    return str(Path(audio_path).stem) + '.vtt'

def embed_captions_ffmpeg(video_path: str, caption_path: str, output_path: str):
    """FFmpeg：将字幕嵌入视频"""
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-vf', f"subtitles={caption_path}",
        '-c:v', 'libx264', '-preset', 'fast',
        '-c:a', 'aac',
        output_path
    ], check=True)

def main():
    audio_file = sys.argv[1]  # ElevenLabs 输出
    video_file = sys.argv[2]  # 源素材

    print(f"[1/2] 从 {audio_file} 生成字幕...")
    vtt = generate_captions(audio_file)

    print(f"[2/2] 将字幕嵌入视频...")
    embed_captions_ffmpeg(video_file, vtt, 'output_with_captions.mp4')

    print("✅ 完成。输出：output_with_captions.mp4")

if __name__ == '__main__':
    main()
```

运行：

```bash
chmod +x caption_pipeline.py
./caption_pipeline.py audio.mp3 video.mp4
```

**总耗时：约 2 分钟**（Whisper 1 分钟 + FFmpeg 30 秒 + 开销）。无需手动使用 CapCut 编辑字幕。

---

## 替代工具与优化

### 比 ElevenLabs 更好的 TTS（考虑成本）

- **本地 TTS**：`tortoise-tts`（在 RTX 4070 上运行，免费，约每 10 秒生成 1 分钟音频）

  ```bash
  pip install tortoise-tts
  ```

- **API 替代方案**：**Hugging Face Inference API**（比 ElevenLabs 便宜，质量相同）
- **如果语音质量很重要，继续使用 ElevenLabs**（它是品牌声音的最佳选择）

### 字幕样式（如果你想要精美字幕）

使用 **ass/ssa 格式** 而非 VTT，支持颜色、位置、字体：

```python
# 生成带样式的字幕
# 更适合 YouTube/TikTok 美学
subprocess.run([
    'ffmpeg', '-i', video_path,
    '-vf', f"ass={styled_subtitle_path}",  # ASS 字幕
    '-c:v', 'libx264', '-preset', 'fast',
    output_path
], check=True)
```

### 完全跳过 CapCut（如果只是添加字幕）

如果满足以下条件，你的工作流程不再需要 CapCut：

- 音频已在 ElevenLabs 中同步
- 字幕由 Whisper 自动生成
- 视频已通过 FFmpeg 嵌入字幕

**只有在以下情况才需要 CapCut：** B-roll 转场、节奏调整、花哨特效。对于像 `smart-auto` 这样的技术演示，直接字幕 + 录屏通常效果最佳。

### 考虑：YouTube 自动字幕

如果你最终要上传到 YouTube，可以上传不带嵌入字幕的 MP4。YouTube 会免费生成字幕（准确度不错）。如果 YouTube 的字幕不够好，再下载为 SRT 并在本地嵌入。

---

## 我对你工作流程的建议

**优化后的流水线（新版）：**

```
编写字幕 → ElevenLabs（语音）→ Whisper（验证/修复 VTT 字幕）
→ FFmpeg 嵌入 → 上传到 YouTube
```

**5 分钟视频的时间分配：**

- 编写字幕：5–10 分钟
- ElevenLabs TTS：2 分钟（可并行、批量处理）
- Whisper 验证：1 分钟（检查，少量修改）
- FFmpeg 嵌入：30 秒
- **总计：约 10 分钟**，主要是等待 API 响应

**对比当前工作流程：**

- 手动 CapCut 字幕：每段视频 20–30 分钟

**提升：约快 2 倍。零 CapCut 摩擦。**

---

## 进阶：完全自动化

如果你定期发布视频，可以将其接入 CLI 工具：

```bash
ww caption-video --script "your_text.md" --voice "alloy" --video "source.mp4"
```

（使用你的自定义 CLI 工具 `ww` + MCP 实现自动化）

这将批量处理：脚本 → 字幕 → 音频 → 视频，一次调用完成。

---

**参考资料：**

- [Whisper 文档](https://github.com/openai/whisper)（pip 安装，约 800MB 模型）
- [FFmpeg 字幕嵌入](https://trac.ffmpeg.org/wiki/Subtitles)
- [ElevenLabs API](https://elevenlabs.io/docs/api/text-to-speech)
