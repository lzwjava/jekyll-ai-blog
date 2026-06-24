---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Image Music to MP4 Guide
translated: false
type: note
---

**Question:** When sharing an image with background music in WeChat, is that a WeChat-specific format? And when uploading to YouTube Shorts, you need actual video — so how do you convert that image+music format to a proper video file?

**Answer:**

Yes, WeChat's "image + music" share format is proprietary to WeChat's ecosystem. When you create a "视频动态" (video status) or share via WeChat Channels (视频号) with a still image + BGM, WeChat stores it internally as a composite post — not a standard video file. You can't directly export it as `.mp4`.

For YouTube Shorts, you need a real video file (H.264/MP4, vertical 9:16, ≥1080x1920 recommended).

**Convert image + audio → MP4 using ffmpeg (the correct tool here):**

```bash
ffmpeg -loop 1 -i input.jpg \
       -i music.mp3 \
       -c:v libx264 \
       -t 30 \
       -pix_fmt yuv420p \
       -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
       -c:a aac -b:a 192k \
       -shortest \
       output.mp4
```

Key flags:

- `-loop 1` — loops the still image as video frames
- `-t 30` — duration in seconds (Shorts max 60s)
- `scale + pad` — letterbox/pillarbox to 9:16 without cropping
- `-pix_fmt yuv420p` — required for broad compatibility (YouTube, WeChat, etc.)
- `-shortest` — stops when audio ends

**If you want to extract the music from WeChat first**, that's the harder part — WeChat doesn't give you a clean export. Options:

- Record the audio playing from your phone using another device or screen record with audio
- If you originally had the audio file, just use it directly
- On rooted Android, WeChat caches are in `/data/data/com.tencent.mm/` but obfuscated

**One-liner for a quick test with a color background instead of image:**

```bash
ffmpeg -f lavfi -i color=c=black:s=1080x1920:r=30 \
       -i music.mp3 -t 30 \
       -c:v libx264 -pix_fmt yuv420p -c:a aac \
       -shortest output.mp4
```

Bottom line: WeChat's image+music is not a standard format — it's a platform feature. For cross-platform use, `ffmpeg -loop 1` is your friend.
