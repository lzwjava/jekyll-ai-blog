---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Truth Labs: Single Static HTML"
translated: false
type: note
---

Done. **Truth Labs is now a single, self-contained `index.html`** — no Jekyll, no bundle, no build step. Just open the file in a browser or drop it on any static host (GitHub Pages, Cloudflare, nginx, `python3 -m http.server`).

## What's in the file

One page, one inline `<style>` block, ~52 KB total. All sections as in-page anchors:

| Section | Content |
| --- | --- |
| **Hero** | "Truth through compute — nothing but truth" + 4-stat band (52 GB VRAM, 13 models, ~5B tokens, 12 yrs) |
| **Focus areas** | Training · Inference & serving · GPU & hardware · Consulting |
| **Experiments** | 6 public-work cards (SEC-EDGAR-GPT, nanoGPT fork, 52 GB cluster, MoE, zz, FluxReel) |
| **Manifesto** | One-person-lab quote |
| **Research** | Full lab notebook: 13-run training table, hardware spec list, SEC-EDGAR-GPT, nanoGPT fork, inference benchmarks (nano-vLLM 506 tok/s, SGLang, llama.cpp, MoE), M40/P100 cluster + BIOS breakthrough, token-usage tables |
| **Services** | 4 hireable lines + engagement model + verifiable references |
| **About** | Timeline 2008 → 2026, quick facts, papers, "why a lab of one" |
| **Contact** | Email/GitHub/blog channels + what to send per service |

## Verified

- Serves `200` locally, 0 Jekyll/liquid syntax remaining
- All nav anchors (`#research`, `#services`, `#about`, `#contact`, …) resolve to targets
- No unclosed/mismatched HTML tags, no broken internal links
- Fully responsive + mobile nav handling

To preview:

```bash
cd /Users/lzwjava/projects/truth-labs && python3 -m http.server 8080
```

The directory is now just `index.html`, `.gitignore`, and nothing else — cleanest possible static site.
