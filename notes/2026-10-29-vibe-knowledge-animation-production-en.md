---
audio: false
generated: true
image: false
lang: en
layout: post
title: Vibe Knowledge Animation Production
translated: false
type: note
---

**Question:** How are "vibe 知识鉴赏" (vibe knowledge-appreciation) animation videos on WeChat Video Channel made?

**Answer:**

These are a genre of aesthetic knowledge-education short videos blending **lofi/cozy animation visuals** with informational content. Here's how they're typically produced:

---

## 🎨 What the Style Is

- **Lofi anime aesthetic** — warm lamp light, cozy rooms, rain on windows, soft color palettes
- **Knowledge overlay** — art history, science, culture explained via animated text or voiceover
- **Ambient/lofi background music** — non-intrusive, study-mood tracks
- Often **looping or slow-panning** visuals to hold attention

---

## 🛠️ The Common Production Pipeline

### Step 1 — Generate Base Visuals (AI Image Tools)

- **Midjourney / 即梦AI (Seedance 2.5) / 可灵AI (Kling)** — generate the cozy/aesthetic scene images
- A common workflow: use `/describe` in Midjourney to extract prompt keywords from reference images, then `/imagine` to generate original illustrations in the same style

### Step 2 — Animate the Visuals (AI Video / Motion Tools)

Tools like Morphic let you describe a lofi anime scene (e.g., "a girl studying by a rainy window under warm lamp light") and generate looping animated clips directly in the browser — no After Effects required

For more structured **knowledge-type animations** (diagrams, concept flows, math), the open-source tool **Manim** (made famous by 3Blue1Brown) is widely used:

- Manim is described as the "same engine as 3Blue1Brown" — it turns text descriptions into precise mathematical/knowledge animations; if your video involves concept derivations, physics simulations, or programming visualizations, Manim's precision is irreplaceable
- A popular "vibe coding" approach: using AI (like Gemini or Claude) combined with Manim to generate animated teaching/drawing videos purely from text prompts — the whole production is just prompt words handed to the model

### Step 3 — Edit & Package (剪映 / CapCut)

After generating the AI image, import it into 剪映 (CapCut), add animation effects like light flares, smoke, or moving leaves/elements to enrich the scene, then layer in the lofi music track and export

For advanced creators: a higher-quality workflow uses Midjourney → Photoshop GenFill (for extending/compositing) → Magnific AI (upscaling) → After Effects (layered animation) — this approach took one creator ~18 hours to produce a single piece

### Step 4 — Add Knowledge Content

- Text overlays / 字幕 with key facts
- AI voiceover (科大讯飞, ElevenLabs, 即梦数字人)
- Narration synced to visual beats

---

## ⚡ Quick Tool Map

| Goal | Tool |
| --- | --- |
| Generate cozy scene art | 即梦AI / 可灵AI / Midjourney |
| Animate static images | Morphic / Runway / Pika / Vidu |
| Knowledge concept animation | **Manim** (AI-generated scripts) |
| Final editing + effects | **剪映 (CapCut)** |
| Lofi music | Soundful / YouTube Audio Library |
| Voiceover | 科大讯飞 / ElevenLabs |

---

**Bottom line:** Most creators combine **AI image generation → AI video animation → 剪映 editing**. The "vibe" aesthetic comes from lofi scene prompts; the "知识鉴赏" layer comes from text/voiceover or Manim-style concept animations layered on top.

---

**References:**

- [如何用AI制作lofi anime视频 — Morphic](https://morphic.com/zh/resources/videos/lofi-anime-videos)
- [在小红书用AI做动态Lofi音乐号完整教程 — 知乎](https://zhuanlan.zhihu.com/p/686529764)
- [2026年开源AI视频工具全景拆解 — 知乎](https://zhuanlan.zhihu.com/p/2058330553322058463)
- [用AI制作Lofi治愈视频 — 知乎](https://zhuanlan.zhihu.com/p/690904102)
- [Manim + Vibe Coding for animations — Learn By Doing with Steven](https://learnbydoingwithsteven.bearblog.dev/shocking-results-from-manim-and-antigravity/)
