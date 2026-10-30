---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码构建的视频与转录
translated: true
type: note
---

完成。所有内容已交付。以下是你在 `/Users/lzwjava/projects/video-factory` 中的内容：

## 🎬 Video (code-built, no CapCut)
**`output/announcement.mp4`** — 1920×1080, 30fps, **55秒**, 静音轨（如果你愿意，可以录制自己的配音）
- 5个场景：Intro → Truth Lab → Truth Software → Blog/Portfolio → CTA
- **双语：每张幻灯片和字幕都显示英文 + 中文**（`求真实验室` / `Truth Lab` 等），因此在微信上静音播放也有效
- 暗色调排版风格，匹配 truthlab.cc（#0a0a0b + 金色 #e3b341），Inter + Menlo + Hiragino 字体，微妙的 Ken-Burns 运动，带有淡入/淡出的字幕条

**随时重建** — 所有内容都在 `scenes.json` 中（时长、标题、要点、字幕英文+中文）。只需编辑并运行：
```bash
python3 render_slides.py && python3 build_video.py
```

## 📝 Transcripts
- **`transcript.md`** — 完整的英文旁白脚本（微信 + YouTube文案，hashtags，章节时间戳）
- **`deliver-transcription.md`** — 你的语音备忘录 `deliver.m4a`（8:45）的文字记录，双语：带时间戳的清洁中文 + 英文翻译，以及原始 ASR 附录

## 🔊 About the memo transcription
`deliver.m4a` 是用户的声音——所以我去了 RTX 4070 机箱（`lzw@192.168.1.36`），复制了备忘录，并运行了 **openai-whisper large-v3**（GPU，74秒）——比本地小模型清晰得多。本地 CPU 之前看到 90MB 空闲 VRAM，但这是短暂的；large-v3 在重试时正好适用。原始输出：`whisper_out/`（txt/vtt/srt/json）。你的故事传达得很好：平方根科技（2016–19），HSBC 16个月，住房债务，13个考试 + IELTS，CSTU 硕士，重新推出求真软件 + 求真实验室，token-based pricing。

注意：你的语音备忘录（8:45）讲述的故事比55秒的视频宏大得多——如果你想要更长的版本或将备忘录翻译成英文配音稿，只要说一声。