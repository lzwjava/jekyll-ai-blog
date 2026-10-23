---
audio: false
generated: true
image: false
lang: en
layout: post
title: Truth Labs One-Person AI Research Lab
translated: false
type: note
---

Done. I've built **Truth Labs** — a one-person AI research lab site in `/Users/lzwjava/projects/truth-labs`, modeled on the Thinking Machines Lab aesthetic (dark, minimal, serif typography, evidence over hype) and powered by the same Jekyll toolchain as your blog.

## What was created

**5 pages**, all drawn from `2026-06-02-ai-portfolio-en.md`, `2025-01-11-resume-en.md`, and your `notes/`:

- **`index.html`** — hero ("Truth through compute — nothing but truth"), a stats row pulled from hard numbers (52 GB VRAM cluster, 13 models trained, ~5B tokens, 12 years), the four lab pillars, selected experiments, and a one-person lab manifesto.
- **`research.html`** — the open lab notebook: your full **13-run training log table**, nanoGPT fork (45 commits, 6 configs), SEC-EDGAR-GPT, inference work (nano-vLLM 506 tok/s, SGLang from source, llama.cpp GGUF, MoE tracing), the **M40/P100 BIOS breakthrough** writeup, GPU teardowns, and the token-usage tables.
- **`services.html`** — four hireable lines: AI inference, GPU & hardware, training & fine-tuning, consulting — each backed by public evidence, plus engagement models and references.
- **`about.html`** — the full path from NOIP 2011 → LeanCloud → DBS/HSBC → turning point in 2023 → Truth Labs, rendered as a timeline; quick facts, papers, and why a lab of one.
- **`contact.html`** — email, GitHub, blog, portfolio links + what to send for each service.

## Design

- Dark theme (`#0a0a0b`), Newsreader serif + Inter, amber "truth gold" accent `#e3b341`
- Sticky glass header, stat bands, pillar/experiment cards with status badges, hover states, mono labels
- Fully responsive (2-col → 1-col on mobile), custom SVG favicon

## Verified

`bundle install` + `bundle exec jekyll build` compile cleanly; all 5 pages and CSS return 200 from `jekyll serve`.

To preview locally:

```bash
cd /Users/lzwjava/projects/truth-labs && bundle exec jekyll serve --livereload
```

One note: I worked entirely from the facts in your portfolio/resume so nothing is invented — worth a skim in case you want to adjust specifics (e.g. the paper date on the about page, which I wrote as 2025 from the resume's Aug 2026 citation).
