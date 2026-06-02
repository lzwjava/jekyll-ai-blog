---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add Voice to Tutorials With edge-tts
translated: false
type: note
---

Sure, here's the exact process:

### 🎙️ Adding Voice to the Tutorial

**Step 1: Install edge-tts**

```bash
python3 -m pip install --break-system-packages edge-tts
```

This is Microsoft Edge's free neural TTS — sounds natural, no API key needed.

**Step 2: Generate an MP3 per slide**

```python
import edge_tts

voice = "en-US-GuyNeural"  # Clear male voice
text = "So what is grep? Grep stands for Global Regular Expression Print..."

communicate = edge_tts.Communicate(text, voice, rate="+0%")
await communicate.save("narration/01_what.mp3")
```

Did this for all 14 slides, each with a script tailored to what's on screen.

**Step 3: Re-time slides to match audio length**

Got each MP3's duration with ffprobe, then rebuilt the concat file so each slide stays up as long as its narration + 1.5s breathing room:

```python
audio_dur = get_duration("narration/01_what.mp3")  # e.g. 12.3s
slide_dur = max(audio_dur + 1.5, 6.0)              # min 6s, pad 1.5s
```

**Step 4: Concatenate audio tracks**

Stitched all MP3s together with silence gaps between slides:

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

**Step 5: Merge video + audio into final MP4**

```bash
ffmpeg -i temp_video.mp4 -i combined.mp3 \
  -c:v copy -c:a aac -b:a 128k -shortest \
  grep_tutorial_voiced.mp4
```

`-c:v copy` means no re-encoding the video (fast), just muxes the audio in.

### The full script is at

`tutorial/add_voice.py` — ~180 lines of Python orchestrating edge-tts + ffmpeg.

Want to swap the voice? Some options:

- `en-US-JennyNeural` — friendly female
- `en-GB-RyanNeural` — British male
- `en-AU-WilliamNeural` — Australian male
- `zh-CN-YunxiNeural` — Chinese male (for a Chinese version!)
