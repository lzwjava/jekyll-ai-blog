---
audio: false
generated: true
image: false
lang: en
layout: post
title: Depth Beats Breadth in Listening
translated: false
type: note
---

**Question:** Is my advice right — that listening to one piece of material 50 times beats listening to 50 materials once, like 3-5 close friends beat a crowd of acquaintances, or 100 true users beat 10,000 casual ones?

**Answer:**

Mostly right, with one correction on the mechanism and one on when to stop.

The part you got right: depth beats breadth *early on*. This matches what SLA researchers call **narrow listening** (Krashen's term) — repeated exposure to a small set of familiar material. Why it works, from first principles: listening comprehension is a real-time decoding problem. Your brain has to segment a continuous audio stream into phonemes → words → phrases fast enough to keep up. With novel material every time, you're paying the segmentation cost *and* the vocabulary/context cost simultaneously — cognitive overload, nothing sticks. With looped material, context becomes free after a few passes, so all remaining attention goes to acoustic decoding: connected speech, reductions ("wanna", "gonna", dropped t's), stress patterns. That's the skill that actually transfers to new material.

Two corrections:

1. **Returns aren't linear to 100 loops.** Loops 1-15 give most of the gain. Around loop 20-30 you've memorized the audio and you're doing recall, not decoding — comprehension stops improving because there's nothing left to comprehend. The "100 loops" framing works as motivation, but the better stopping rule is: **loop until you understand ~95% without the transcript, then switch** to adjacent material — same speaker, same topic. Another Jobs speech. Another Lex episode with the same guest. That keeps ~70% of the context free while forcing fresh decoding. This is the actual narrow listening protocol: a *cluster* of related materials, not literally one file forever.

2. **Add one transcript pass early.** Pure blind looping of material you understand 20% of is slow — you can loop a misheard phrase 100 times and never fix it. The high-leverage move: listen 2-3 times blind → read transcript once, mark what you misheard → loop blind again. The transcript pass converts "unknown noise" into "known words I couldn't hear," which is exactly what repetition then fixes. Your friend can script this: `yt-dlp` the audio + Whisper for the transcript, one command.

So the refined version of your line: **one material 15 times, then 5 related materials 15 times each, beats 50 random materials once.** Same philosophy — 5 close friends, not 50 acquaintances — but the friends should know each other.

Your "listen even if you don't understand" advice needs the same caveat: input has to be *comprehensible-ish* (Krashen's i+1). Jobs at Stanford is perfect — clear, slow, emotional anchoring. Raw Lex Fridman 3-hour technical episodes at 1x with 20% comprehension is mostly noise for a beginner; that's where transcript-assisted looping matters most.
