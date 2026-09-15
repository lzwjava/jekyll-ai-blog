---
audio: false
generated: true
image: false
lang: en
layout: post
title: Digital Fly Brain Model
translated: false
type: note
---

Question: **What’s the new “fly model” released on September 3, 2026, with motion capability?**

Answer: I think you’re referring to the **fruit-fly brain / digital-fly work announced around Sept. 3**, rather than a generative AI model.

On Sept. 3, Google Research + HHMI Janelia published the **first complete connectome of an adult male fruit fly**: about **166,700 neurons and ~125M synapses**, covering the brain plus ventral nerve cord. The interesting part is that this gives researchers a wiring diagram detailed enough to build a **computational/digital fly capable of modeling behavior and movement**. ([explainx.ai][1])

The key distinction:

```text
real fly
   │
   ├── sensory input
   │       ↓
   │   neural circuit
   │       ↓
   └── motor output
           ↓
       movement

connectome
   ↓
digital neural circuit
   ↓
simulate neural dynamics
   ↓
predict / reproduce behavior
```

So if the thing you saw was described as **“a fly model with movement ability”**, it is probably this **digital-fly / whole-connectome simulation direction**, not a video-generation model. The AI was primarily used to reconstruct the neural wiring from electron-microscopy data; it isn't an LLM that directly “understands” the fly. ([explainx.ai][1])

There is also a separate Sept. 3 release from Runway, **GWM Worlds 2**, which *does* generate interactive worlds with controllable motion in real time, so I don't want to conflate the two. ([runway.com][2])

If you give me the screenshot/name you saw, I can pin down the exact model and dig into its architecture/training setup.

[1]: https://explainx.ai/blog/google-fruit-fly-brain-connectome-ai-2026?utm_source=chatgpt.com "Google and Janelia Mapped a Fruit Fly Brain"
[2]: https://runway.com/research/introducing-gwm-worlds-2?utm_source=chatgpt.com "Introducing GWM Worlds 2 - Research"
