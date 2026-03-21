---
audio: false
generated: true
image: false
lang: en
layout: post
title: Making a Grep Video Using FFmpeg
translated: false
type: note
---

Sure! Here's the full breakdown:

### 🦞 How I Made the Grep Tutorial Video

**1. Install ffmpeg**
```
sudo apt-get install -y ffmpeg
```

**2. Generate slide PNGs using ffmpeg's `drawtext` filter**

Each "slide" is a PNG image created with ffmpeg's `lavfi` (libavfilter) virtual input + `drawtext` overlays. No GUI needed — all pure CLI.

```bash
ffmpeg -y -f lavfi -i "color=c=0x1a1b26:s=1280x720:d=1" \
  -vf "drawtext=fontfile=FONT:text='Title':fontsize=42:fontcolor=0x7dcfff:x=(w-text_w)/2:y=30, \
       drawtext=fontfile=FONT:text='Some line':fontsize=24:fontcolor=0xc0caf5:x=70:y=105" \
  -frames:v 1 slide.png
```

Key tricks:
- **`color=c=0x1a1b26`** — Tokyo Night dark background
- **`drawtext`** chained with commas — stacks multiple text lines on one image
- **`(w-text_w)/2`** — centers text horizontally
- Color-coded: green=commands, blue=output, yellow=tips, grey=comments

**3. Concatenate slides into video with the `concat` demuxer**

Created a `concat.txt` listing each slide + how long to show it:

```
file '00_title.png'
duration 4
file '01_what.png'
duration 6
...
```

Then:
```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=93:d=1.5" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -r 30 \
  grep_tutorial.mp4
```

**4. The script itself**

The whole thing is driven by `tutorial/grep_tutorial.py` (~280 lines of Python). It:
- Defines slide content as structured data (auto-colors `$`, `>`, `#` prefixed lines)
- Calls ffmpeg via `subprocess` for each slide
- Writes the concat file
- Runs final ffmpeg to stitch it all together

Want me to walk through any specific part, or tweak the video (add audio, different colors, more slides)?