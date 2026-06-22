---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Project Plan: From Markdown to Interactive Charts"
translated: false
type: note
---

Nice! So the plan is clear:

- Wait a few days for the code model to finish training
- This week, convert the blog from markdown → interactive HTML with charts/visualizations
- The survey widget gives you real user signal to justify the effort

When you're ready to start the HTML conversion, a few things worth thinking through:

**Architecture options:**
1. Static site generator (Jekyll/Hugo) → output HTML with embedded JS charts — least friction since you're already on GitHub Pages
2. Build a small Python script that takes your markdown posts + AI summary → generates rich HTML with D3/Chart.js visualizations per post
3. Hybrid — keep markdown as source of truth, add a render layer on top

Given your "ship fast" style, option 2 fits best — a `md2html.py` that calls Claude API to extract key data points from each post and auto-generates charts. You could batch-process your 400 posts overnight on the workstation.

**What makes blog posts actually visual:**
- Code frequency/language breakdown per post → pie/bar
- Timeline of posts → activity heatmap (like GitHub contribution graph)
- Topic clusters → force-directed graph
- Reading time + complexity score per post

When the model finishes training, share the results — curious what dataset and objective you used for the code model.
