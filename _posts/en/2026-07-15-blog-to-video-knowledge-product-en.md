---
audio: false
generated: true
image: false
lang: en
layout: post
title: Blog to Video Knowledge Product
translated: false
type: note
---

Question: Turn `jekyll-ai-blog` into a video-first knowledge product — a "Geek + Gary Vee + 稚晖君 + BPS Space" style channel. Is this a good idea?

Answer:

I think this idea is **very aligned with your current trajectory**. The key insight is:

> Your blog is already a knowledge production engine. The next evolution is not "make videos randomly"; it is to build a **multimodal knowledge distribution system**.

Your existing repo `lzwjava/jekyll-ai-blog` is essentially:

```
Research → Notes → Markdown → Static Website → Readers
```

The video version becomes:

```
Research
   ↓
AI agent summarizes + structures
   ↓
Script
   ↓
Voice/avatar/screen recording
   ↓
Short video
   ↓
YouTube / Bilibili / TikTok / WeChat Channels
   ↓
Backlinks → blog → community → business
```

The important part: **the source of truth remains the blog**. Video is just another rendering target.

---

## Positioning

The closest mental model:

### Geek + Gary Vee

Gary Vee:

* high frequency
* personal brand
* opinion + distribution

Geek:

* curiosity
* engineering depth
* "I built/tested this"

稚晖君:

* maker credibility
* showing experiments

BPS Space:

* explain frontier technology visually

Your unique angle:

> "An AI engineer building and explaining the future in public."

Not a news commentator.

More like:

```
I read papers
I run models
I buy weird GPUs
I debug hardware
I build agents
I explain what I learn
```

Your MI50 experiments, GPT-2 training on RTX 4070, nanoGPT experiments are actually very suitable content.

---

## Content pillars

I would avoid only "AI news".

AI news is a commodity.

Better:

### 1. Build in public

Example:

"Can a $680 AMD MI50 train an LLM?"

Video:

```
0:00 I bought a $100 GPU nobody wants
0:30 Why this GPU was a datacenter monster
2:00 Hardware teardown
4:00 Installing ROCm
7:00 Training GPT-2
10:00 Result
```

This is very稚晖君-like.

---

### 2. Explain frontier AI

Example:

"Why DeepSeek changed AI economics"

Structure:

```
Problem
  ↓
Old approach
  ↓
New idea
  ↓
Code demonstration
  ↓
Business impact
```

---

### 3. AI engineer life

Example:

"How I trained GPT-2 from zero on one GPU"

This has authenticity because you actually did it.

Many creators explain things they never touched.

---

### 4. AI tools for normal people

This is Gary Vee side.

Example:

"10 minutes: build your own AI employee"

---

## Technical architecture

Your blog can become the content database.

Something like:

```
posts/
  2026-07-mi50-gpt2.md

        |
        v

AI Pipeline

extract:
  - title
  - hook
  - story
  - technical explanation
  - diagrams

        |
        v

video_script.md

        |
        +---- YouTube long video
        |
        +---- Shorts
        |
        +---- Bilibili
        |
        +---- Blog
```

Basically:

**Jekyll → LLM content compiler → video renderer**

---

## AI-native video factory

A simple MVP:

```
article.md

    ↓

Claude/GPT

    ↓

script.json

{
 hook:"",
 scenes:[
   {
    narration:"",
    visual:"",
    code:""
   }
 ]
}

    ↓

Remotion

    ↓

mp4
```

Use:

* Remotion for programmatic video
* ElevenLabs/OpenAI voice
* Whisper for captions
* Mermaid/Manim for diagrams
* ffmpeg pipeline

The advantage:

You can produce 3-5 videos/week without a traditional video team.

---

## But don't copy Gary Vee too much

Your advantage is not energy.

Your advantage is:

```
depth × authenticity × AI acceleration
```

There are already thousands of energetic AI influencers.

Much fewer people can say:

"I trained GPT-2 myself yesterday. Here is the loss curve."

That is your moat.

---

## Possible brand

Something like:

```
AI Engineer Diary

or

Building The Future

or

Geek Lab

or

AI Native Builder
```

The content feeling:

```
Today I bought a $1000 accelerator.
Let's see if it can train a language model.

No slides.
No marketing.
Just experiment.
```

---

I think the strongest strategy is:

**Do not create a video channel first. Create a "knowledge compiler".**

Your blog is the database.

Video, newsletter, Twitter/X, YouTube, Bilibili are different frontends.

You are basically building an AI-era version of a technical media company.

The timing is good because AI makes the production cost collapse.

Your old advantage:

```
one engineer writes one article
```

New advantage:

```
one engineer creates:
- article
- video
- podcast
- course
- community
```

This is exactly the kind of leverage that fits someone who already builds agents and infrastructure.
