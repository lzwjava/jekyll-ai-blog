---
audio: false
generated: true
image: false
lang: en
layout: post
title: Video Agent Space Still Immature
translated: false
type: note
---

Question: Does a `hermes-video-agent` (Claude Code/pi-agent style agent for video editing with ffmpeg) already exist?

Answer:

**Yes, partially. But the space is still very immature.**

Your idea is basically:

> Claude Code for video.

That exact direction is emerging now. ([Claude][1])

Closest projects:

---

## 1. Vex — probably the closest match

[Vex GitHub repository](https://github.com/AKMessi/vex?utm_source=chatgpt.com)

Vex describes itself as:

> "terminal-first AI video editing, driven by plain English"

It does:

```
User prompt
    |
    v
LLM agent
    |
    +-- FFmpeg
    +-- MoviePy
    +-- transcript analysis
    +-- generated visuals
    |
    v
edited video
```

Examples:

```
"remove awkward intro"

"make this a YouTube short"

"add subtitles"

"cut boring parts"
```

Very close to your Hermes idea. ([GitHub][2])

---

## 2. video-use — Claude Code style

[video-use GitHub repository](https://github.com/browser-use/video-use?utm_source=chatgpt.com)

The concept:

```
raw footage folder

        |
        v

Claude Code

        |
        v

final.mp4
```

It treats video editing like coding:

* files
* scripts
* tools
* iterations

Basically:

```
Claude Code
      |
      +-- edit.py
      +-- ffmpeg
      +-- assets
      +-- output.mp4
```

([GitHub][3])

---

## 3. Research direction: VideoAgent

There are also academic systems moving toward this:

VideoAgent: All-in-One Framework for Video Understanding and Editing

The idea:

```
LLM
 |
 +-- shot planning agent
 +-- editing agents
 +-- retrieval agents
 +-- rendering pipeline
```

It is closer to a multi-agent video editor. ([arXiv][4])

---

## But your idea has a different angle

Most current projects:

```
input video
    |
    v
edit video
```

Your Hermes idea could be:

```
intent
 |
 v
video engineer agent
 |
 +-- understand
 +-- create
 +-- edit
 +-- publish
 +-- learn
```

More like:

```
Claude Code
      +
Midjourney
      +
FFmpeg
      +
YouTube automation
```

---

## The missing pieces

Current tools usually lack:

### 1. Long-term memory

Example:

```
hermes-video-agent/

memory/
   my_channel_style.md
   subtitle_style.json
   favorite_music.json
   audience.json
```

After 100 videos:

```
Agent:
"I know your style."
```

---

### 2. Video project state

Need something like git:

```
video-project/

main.mp4

timeline.json

versions/

v1/
v2/
v3/
```

Not:

```
random ffmpeg command
```

but:

```
video commit history
```

Example:

```bash
hermes-video commit -m "make intro shorter"

hermes-video rollback v2
```

---

### 3. Self-evaluation loop

Coding agents have tests:

```
code
 |
test
 |
fix
```

Video agents need:

```
render
 |
watch
 |
critic model
 |
fix
```

Example:

```
Critic:

- first 5 seconds too slow
- subtitle too small
- no hook

Agent:
regenerate
```

---

## My opinion

I would not compete with:

* CapCut
* Runway
* Pika
* Kling

They optimize **one-shot generation**.

Your better positioning:

```
hermes-video-agent

"the operating system for AI video creators"
```

Start CLI:

```bash
hermes video edit input.mp4 \
"turn this into a viral AI short"
```

Then later:

```bash
hermes channel run \
--topic "AI news"
--daily
```

The natural evolution is:

```
pi-agent
   |
   +-- coding agent
   |
   +-- research agent
   |
   +-- video agent
```

So yes, others are starting this, but there is still a large gap between "AI video editor" and "autonomous video engineer". That gap is where your idea sits.

[1]: https://code.claude.com/docs/en/overview?utm_source=chatgpt.com "Claude Code overview - Claude Code Docs"
[2]: https://github.com/AKMessi/vex?utm_source=chatgpt.com "GitHub - AKMessi/vex: claude code for video editing · GitHub"
[3]: https://github.com/browser-use/video-use?utm_source=chatgpt.com "GitHub - browser-use/video-use: Edit videos with coding agents · GitHub"
[4]: https://arxiv.org/abs/2606.23327?utm_source=chatgpt.com "VideoAgent: All-in-One Framework for Video Understanding and Editing"
