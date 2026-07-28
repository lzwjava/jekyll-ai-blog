---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes video agent concept
translated: false
type: note
---

Question: How about building `hermes-video-agent`: a Hermes/pi-agent style coding agent, but specialized for video editing and generation using prompts + ffmpeg?

Answer:

I think this idea is **more focused and technically interesting** than a full TikTok platform.

The key insight:

> Don't build "AI video editor UI". Build a **video-native agent**.

Similar to:

* Anthropic Claude Code → software engineering agent
* pi-agent → lightweight agent runtime
* Hermes → your own agent workflow

Then:

```
hermes-video-agent

User:
"Make this video more like a YouTube Short"

Agent:
- inspect video
- understand timeline
- cut boring parts
- add captions
- add music
- generate B-roll
- render with ffmpeg
```

---

## Core idea

Current video tools:

```
Human
 |
 | clicks buttons
 |
Premiere / CapCut / DaVinci
```

Your idea:

```
Human
 |
 | natural language
 |
hermes-video-agent
 |
 +-- ffprobe
 +-- whisper
 +-- vision model
 +-- ffmpeg
 +-- image/video generation
 |
output.mp4
```

The agent owns the timeline.

---

## The "filesystem as memory" model

Like coding agents:

Coding agent:

```
repo/
 ├── main.py
 ├── tests/
 └── package.json
```

Video agent:

```
project/
 |
 ├── input.mp4
 ├── transcript.json
 ├── scenes.json
 ├── assets/
 │    ├── broll01.mp4
 │    └── image01.png
 |
 ├── edit_plan.json
 └── output.mp4
```

The agent edits files.

---

## Example session

User:

```
hermes-video edit interview.mp4

Make it a 60 second AI news short.
Remove silence.
Add subtitles.
Highlight important sentences.
```

Agent:

```
Analyzing video...

Duration: 48 minutes

Transcript:
- 12000 words

Finding highlights...

Selected:
03:21-04:05
12:44-13:20
27:10-27:55

Creating edit plan...
```

Generates:

```json
{
 "cuts":[
   ["03:21","04:05"],
   ["12:44","13:20"]
 ],
 "captions":true,
 "style":"youtube-short"
}
```

Then:

```bash
ffmpeg \
-i input.mp4 \
-filter_complex script.txt \
output.mp4
```

---

## The killer: expose ffmpeg as tools

Agent tools:

```python
tools = [
    ffprobe,
    extract_audio,
    transcribe,
    detect_scene,
    cut_video,
    merge_video,
    add_caption,
    add_music,
    generate_image,
    generate_video
]
```

Example:

```
User:
"Make Elon Musk style intro"

Agent:

1. generate intro image
2. create motion effect
3. combine
4. render
```

---

## Architecture

Minimal:

```
                 LLM
                  |
                  |
          hermes-video-agent
                  |
     +------------+-------------+
     |            |             |
  Vision       Audio        Editing
     |            |             |
 GPT-4.1     Whisper       ffmpeg
 Qwen-VL                  MoviePy
                           Remotion
```

---

## Why ffmpeg is important

Most AI video startups hide ffmpeg.

I would make ffmpeg the "assembly language".

Example:

Agent creates:

`edit.sh`

```bash
ffmpeg \
-i input.mp4 \
-vf "
scale=1080:1920,
subtitles=sub.srt,
drawtext=text='AI NEWS'
" \
-c:a copy \
output.mp4
```

The LLM is basically a compiler:

```
Prompt
  |
  v
Edit plan
  |
  v
ffmpeg program
  |
  v
video
```

Very similar to:

```
Natural language
       |
       v
Code
       |
       v
Machine
```

---

## Big opportunity: video MCP server

I would make:

```
video-mcp-server
```

Then every agent can use video abilities.

Tools:

```
video.inspect()
video.cut()
video.caption()
video.translate()
video.generate()
video.render()
```

Then:

Claude Code:

```
"Turn this demo into a launch video"
```

Cursor:

```
"Create tutorial video from README"
```

Your own agents:

```
"Generate daily AI news video"
```

---

## MVP I would build

Don't start with generation.

Start with editing.

Because generation is expensive and unstable.

Phase 1:

```
Input:
mp4

Commands:

"remove silence"
"make shorts"
"add captions"
"translate subtitles"
"cut highlights"

Output:
mp4
```

Stack:

```
Python
FastAPI
ffmpeg
Whisper
Qwen-VL / Gemini vision
LLM planner
```

Maybe 1-2 weeks.

---

Phase 2:

Add generation:

```
"Explain CUDA"

Agent:

generate:
 - diagrams
 - images
 - B-roll
 - narration

assemble video
```

---

The interesting positioning:

Not:

> "AI video generator"

Too crowded.

Instead:

> "Claude Code for video."

A terminal-first autonomous video engineer.

`hermes-video-agent` is actually a very natural extension of your `ww` ecosystem. The same agent loop:

```
observe
 -> plan
 -> execute tools
 -> verify output
 -> iterate
```

but the artifact is:

```
software -> video
```

This is a much cleaner product boundary.
