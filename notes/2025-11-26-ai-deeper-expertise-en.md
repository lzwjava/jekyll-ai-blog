---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AI Demands Deeper Expertise, Not Less
translated: false
type: note
---

You're absolutely right — and you've hit the core truth that a lot of people are still slow to admit in the AI/LLM hype era.

Even with powerful models like Grok, Claude, GPT-4o, etc., **you still need deep understanding to ask the right questions and to build anything serious**. The AI didn’t magically remove the need for expertise; it just moved where the expertise is required.

Here’s how it actually works in practice, using your Apple Vision Pro (VisionOS) example:

### Old world (pre-2023):
- You Google “VisionOS SwiftUI tutorial”
- Read Apple docs for 10–20 hours
- Try examples, fail a lot, search Stack Overflow
- Slowly figure out RealityKit, ARKit differences, spatial computing concepts, room tracking, hand input, etc.

### New world (2025, with good LLMs):
You can now ask:
- “Act as a senior VisionOS engineer. I have iOS/SwiftUI experience. Give me the minimal working RealityKit + SwiftUI app that shows a 3D model floating in space, responds to hand tap, and uses volumetric window.”
- Then: “Now convert this to an immersive space with passthrough.”
- Then: “How do I add eye-tracking gaze selection?”
- Then: “Best practices for performance with high-poly models on Vision Pro?”

The AI can generate 90% correct, up-to-date code instantly, explain the new paradigms (like Ornaments, HoverEffect in 3D, EntityComponent system vs SwiftUI, etc.), and even warn you about common pitfalls Apple doesn’t document well.

But here’s the catch — **you still need to know what to ask, and you need to be able to read the generated code and spot when it’s wrong or outdated**.

If you don’t already understand:
- the difference between a WindowGroup, Volume, and ImmersiveSpace
- how hand input works vs touch
- that @Environment(\.dismissImmersiveSpace) exists
- the coordinate system differences
…then even perfect AI code will confuse you, and you won’t know if it’s good or dangerous.

So yes, AI is now like having a very patient senior engineer sitting next to you 24/7, but **you still need enough domain knowledge to steer the conversation and verify the output**.

That’s actually the new bottleneck skill:
**Prompt engineering + critical evaluation** has partially replaced “reading 500 pages of documentation,” but it has **not** replaced understanding.

People who think “I don’t need to learn anything anymore, AI will do it” are the ones who will ship broken, insecure, unperformant, or just weird apps.

People who already have solid foundations (like your 1 year of iOS experience) are now 5–10× faster and can compete with teams of 10.

So your intuition is spot-on:
AI didn’t remove the need to learn.
It raised the bar for what “learning” means — now it’s about judgment, taste, and knowing which questions reveal the real constraints.

Keep learning the fundamentals. The AI will multiply your power, not replace your brain.
