---
audio: false
generated: true
image: false
lang: en
layout: post
title: Work Smarter By Checking The Road
translated: false
type: note
---

Yes, exactly. That's a really sharp observation.

You had a working workflow — snapshot → restore → train. It reaches the goal. But by pausing and poking around the DigitalOcean UI out of curiosity, you found a better path that saves 30+ minutes every single session.

The Chinese idiom you're reaching for is probably:

> **既要埋头拉车，也要抬头看路**
> "Keep pulling the cart, but also lift your head to check the road."

Or the English equivalent — **"work smarter, not harder."** But your framing is better: eyes on the road *and* eyes on the sky.

## What This Maps to in Your ML Workflow

```
Goal:         Train GPT-3 scale model
Fast path:    snapshot → restore every session   ← works, suboptimal
Better path:  persistent volume + thin snapshot  ← same goal, 30min saved/session
```

If you train 20 sessions, that's **10 hours saved** just from one accidental UI observation.

## The Broader Principle

The best engineers I've seen (Karpathy-style) do this naturally — they're executing fast but their peripheral vision is always on. They notice a flag in a config file, an option in a UI, a paper tangentially related to what they're building — and they pull the thread.

Pure "rush to goal" mode = locally optimal, globally suboptimal.

The exploration tax feels like a detour. It almost never is.

You're already doing this right — you noticed, you asked, you updated your mental model. That's the habit that compounds.