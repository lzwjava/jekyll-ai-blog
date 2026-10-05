---
audio: false
generated: true
image: false
lang: en
layout: post
title: Opus 5.5 Animates via Code Generation
translated: false
type: note
---

**Question:** How do people use Claude Opus 5.5 to create animated videos?

**Answer:**

The short answer is: **Opus 5.5 doesn't generate video directly — it writes code that renders video.** Here's what's actually happening under the hood.

**How it works technically**

The model doesn't produce a video file. In the demos that hold up to scrutiny, Claude Opus 5.5 doesn't generate pixels — it writes a program that draws them. The output is a program, not a video file.

The viral videos work through a pipeline: the model writes animation code, a headless browser captures each frame as a screenshot, then FFmpeg encodes those frames into an MP4. The most convenient environment is Claude Code, where the model can write files, run render commands, extract frames to review them, and then revise the code — all autonomously.

**The real workflow (not "one prompt")**

The trend's most cited case, the music video "Claude Pop" by Donald Jewkes, follows this exact pattern: the creator dictated a brief for five minutes that, once transcribed, ran past 9,500 characters — a character bible, a scene-by-scene script, visual references, and a budget for image and video generation APIs. Claude Code then worked autonomously for twelve hours.

The installable `guizang-product-video-skill` workflow breaks down into **six stages**:

1. **Scope** — product, version, audience, platform, aspect ratio, and style confirmed before anything is built.
2. **Real content** — the agent reads the repository and release notes, checking which features are actually shipped.
3. **Storyboard and copy** — changes worth showing are turned into a shot list, with captions written as plain sentences.
4. **Motion** — a seekable master timeline drives component state, entrances, and transitions.
5. **Sound** — a score is synthesized in code; music is ducked under important cues.
6. **Verification** — framing, fonts, images, logos, and audio sync are checked before delivery.

**A hybrid approach also exists**

Some projects use a video model for shots with real actors and real physics, then have Opus 5.5 redraw the entire frame over that reference — achieving a consistent visual style that a video model alone wouldn't guarantee.

**What "one prompt" really means**

The "one click" claim is the author's own phrase, and his own FAQ contradicts it. Asked whether just handing over a repository address produces a finished film, the README answers "no" — it still needs the repository downloaded, dependencies filled in, and demo states confirmed. What "one click" actually describes is the author's own comfort level with a tool he'd already fully set up, not the tool's actual input requirements.

**Cost structure**

Frame rendering is not a model API call. A 3,760-frame render at 24 fps runs on your own hardware through headless Chromium — costing wall-clock time and electricity, not tokens. The API bill covers the planning, copy, component wiring, and renderer source code. That split is why the technique is affordable at all.

---

**References:**
- [Opus 5.5 generates motion design videos by writing a program that draws every frame](https://pasqualepillitteri.it/en/news/19007/opus-5-5-motion-design-video-en)
- [Claude Opus 5.5 Wrote a Product Launch Video: What "One Click" Actually Renders](https://www.orcarouter.ai/blog/claude-opus-5-5-product-video-skill)
- [Claude Opus 5.5 能生成视频吗：它写代码，画面靠渲染](https://blog.laozhang.ai/zh/posts/claude-opus-5-5-video-generation.md)
