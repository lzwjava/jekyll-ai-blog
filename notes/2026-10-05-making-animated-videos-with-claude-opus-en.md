---
audio: false
generated: true
image: false
lang: en
layout: post
title: Making Animated Videos with Claude Opus
translated: false
type: note
---

Question: How are people using Claude Opus 5.5 to make good videos, like the animated motion-graphics clips going around?

Answer:

**The key point: Opus 5.5 doesn't output video.** It reads text and images and returns text, so it can't directly produce an MP4. What it writes is a program, and a browser automation library turns that program into frames one at a time. The model writes HTML, CSS and a JavaScript animation library, or React, and a render engine captures the frames.

**The usual workflow**

1. **Use a coding agent (Claude Code is the common choice).** People give it a long, detailed brief and let it work for hours. Claude Code reportedly worked autonomously for twelve hours on the most-cited music video, correcting itself by looking at its own outputs.
2. **Pick a render route.** HyperFrames suits HTML and GSAP work, Manim suits math and data explainers, Blender (via its official Claude connector) suits 3D, and Remotion suits people who already write React. Independent tests found Opus 5.5 tends to default to the simplest route on its own: one HTML file, a seek function, and Playwright to capture frames.
3. **Install the Remotion plugin if you want editable projects.** Remotion's official Claude Code plugin helps Claude Code create and edit Remotion projects. The setup commands are:

   ```
   claude plugin marketplace add remotion-dev/claude-code-plugin
   claude plugin install remotion@remotion
   ```

4. **Ask for an editable project plus an explicit render step.** A good prompt asks for frame-driven animation and local assets, for example a 15-second product launch video or a 20-second chart animation from a CSV file. Then export, e.g. `npx remotion render src/index.tsx Promo out/promo.mp4 --codec=h264 --pixel-format=yuv420p --muted`
5. **Optionally mix in a video model.** Some projects use a video model for live-action footage and physics, then have Opus 5.5 redraw each frame over that reference to get a consistent style.

**Examples people are making:** explainer-style animations like a history of AI, music-video animations, and brand or product launch videos. One creator said Opus 5.5 made a merch launch video with Remotion, with strong transitions, timing and branding.

**A reality check:** the "one prompt" claim is misleading. An Anthropic Claude Code team member joked that the post says "Claude one-shot this" while the real prompt was 10k characters with skills, examples and API keys. So expect to write a detailed brief, supply assets, and iterate.

**Easy way to start:** begin with a small 10–15 second project in Remotion to confirm the export works, then scale up to a longer piece.

References:

- [Opus 5.5 generates motion design videos by writing a program that draws each frame](https://pasqualepillitteri.it/news/19006/opus-5-5-motion-design-video)
- [Claude Opus 5.5 Motion Graphics: Best Tools, Free and Paid](https://capitalandcompute.net/blog/claude-motion-graphics-tools/)
- [Make videos with Opus 5.5: prompts and MP4 export](https://ofox.ai/blog/opus-5-5-video-prompts-mp4-guide/)
- [Claude Opus 5.5 Is Generating Incredible Animated Motion Graphic Videos: 10 Best Examples](https://officechai.com/ai/claude-opus-5-5-motion-graphic-videos/)
- [BridgeMind Remotion case (Hermes case library)](https://hermes-ai.net/ai-models/claude-opus-5-5/case/2102462889160286423/)
