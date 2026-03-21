---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 edge-tts 为教程添加语音
translated: true
type: note
---

当然，这是确切的流程：

### 🎙️ 为教程添加语音

**步骤 1：安装 edge-tts**

```bash
python3 -m pip install --break-system-packages edge-tts
```

这是 Microsoft Edge 的免费 neural TTS — 听起来自然，无需 API key。

**步骤 2：为每个幻灯片生成一个 MP3**

```python
import edge_tts

voice = "en-US-GuyNeural"  # Clear male voice
text = "So what is grep? Grep stands for Global Regular Expression Print..."

communicate = edge_tts.Communicate(text, voice, rate="+0%")
await communicate.save("narration/01_what.mp3")
```

为所有 14 个幻灯片做了这个，每个都有针对屏幕内容的脚本。

**步骤 3：重新调整幻灯片时间以匹配音频长度**

使用 ffprobe 获取每个 MP3 的持续时间，然后重建 concat 文件，使每个幻灯片显示时间为其旁白 + 1.5 秒缓冲时间：

```python
audio_dur = get_duration("narration/01_what.mp3")  # e.g. 12.3s
slide_dur = max(audio_dur + 1.5, 6.0)              # min 6s, pad 1.5s
```

**步骤 4：连接音频轨道**

将所有 MP3 拼接在一起，幻灯片之间有静音间隙：

```
# audio_concat.txt
file '00_title.mp3'
file 'silence_0.mp3'    # padding
file '01_what.mp3'
file 'silence_1.mp3'
...
```

```bash
ffmpeg -f concat -safe 0 -i audio_concat.txt -c:a libmp3lame combined.mp3
```

**步骤 5：将视频 + 音频合并成最终 MP4**

```bash
ffmpeg -i temp_video.mp4 -i combined.mp3 \
  -c:v copy -c:a aac -b:a 128k -shortest \
  grep_tutorial_voiced.mp4
```

`-c:v copy` 表示不对视频重新编码（快速），只需将音频 mux 进去。

### 完整脚本位于：
`tutorial/add_voice.py` — 大约 180 行 Python 代码，协调 edge-tts + ffmpeg。

想换声音吗？一些选项：
- `en-US-JennyNeural` — 友好女性
- `en-GB-RyanNeural` — 英国男性
- `en-AU-WilliamNeural` — 澳大利亚男性
- `zh-CN-YunxiNeural` — 中国男性（用于中文版本！）