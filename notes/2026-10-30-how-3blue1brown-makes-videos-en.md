---
audio: false
generated: true
image: false
lang: en
layout: post
title: How 3Blue1Brown Makes Videos
translated: false
type: note
---

**Question:** How does 3Blue1Brown make his videos, and what tools/projects does he use?

**Answer:**

The most common question Grant Sanderson (3Blue1Brown) gets is what he uses to animate his videos. The short answer is that he wrote a **custom Python library called Manim** — it's all programmatic and very bespoke.

### 🔧 Core Tool — Manim

**Manim** stands for **Mathematical Animation Engine**, created by Grant Sanderson to produce high-precision math animation videos.

What makes it different from standard animation software is that **everything is scripted** — you write Python code describing shapes, positions, and transformations, and Manim renders the frames into a video.

### 🚀 How It Started

Grant started with a scrappy bit of Python code, used it to make the first video on his channel, and as he made more videos the tool improved — as the tool improved he made more videos, and that just continued. He has always posted all the code he makes for videos openly on GitHub, and he also made the underlying tool Manim open source.

### 📦 Two Versions of Manim

There is his personal version, and a community of people who wanted it to be a more robust tool forked the repo and created a version that is attentive to issues and pull requests, has better testing and documentation — it's called the **Manim Community** edition.

### 🎬 Full Workflow

Manim is just a tool for making individual clips to be edited together later. He advises that you should use **traditional video-editing software** for as much as you can.

He also uses **MathPix**, an OCR tool that converts screenshots of equations directly into LaTeX code. The workflow becomes: see an equation in a paper → screenshot it → paste the LaTeX into Manim → animate.

### 📁 Code on GitHub

The GitHub repo `3b1b/videos` contains all the code used to generate the explanatory math videos found on 3Blue1Brown, organized by year from 2015 onward.

---

**Summary of tools:**

| Tool | Purpose |
| ------ | --------- |
| **Manim** (Python library) | Core animation engine |
| **LaTeX** | Math equations rendering |
| **MathPix** | Convert equations → LaTeX |
| **Video editor** (e.g. Premiere) | Final video editing & narration sync |
| **GitHub** | Open source code sharing |

**References:**

- [3Blue1Brown FAQ (official)](https://www.3blue1brown.com/faq/)
- [How I animate 3Blue1Brown — Manim demo](https://recapio.com/digest/how-i-animate-3blue1brown-a-manim-demo-with-ben-sparks-by-3blue1brown)
- [Manim on Wikipedia](https://www.wikiwand.com/en/articles/Manim)
- [3b1b/manim on GitHub](https://github.com/3b1b/manim)
- [3b1b/videos (scene code) on GitHub](https://github.com/3b1b/videos)
