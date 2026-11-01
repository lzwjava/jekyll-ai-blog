---
audio: false
generated: true
image: false
lang: en
layout: post
title: Site Restructured into Four Lines
translated: false
type: note
---

Done. Here's what changed — the site is now **truth-software**, reorganized around your four business lines, with the truth-lab content consolidated into it.

## New page structure (one `index.html`)

| Section | Content |
| --- | --- |
| **#lines** (new) | Overview grid of the four business lines |
| **#ml** — 业务线 01 · 模型训练与推理 (new) | Pretraining from scratch (GPT-2 124M/760M), LoRA/SFT/RLHF, vLLM/SGLang/llama.cpp serving, GPU workstations, data pipelines, public evidence (SEC-EDGAR-GPT, benchmarks) |
| **#ai-transform** — 业务线 02 · AI 转型咨询 | kept, re-kickered |
| **#ai-services** — 业务线 03 · AI 应用与智能体开发 | kept (workstation/training cards moved to line 01) |
| **#services** — 业务线 04 · 一般应用开发 | exactly the 4 items you listed: iOS/Android, 微信小程序, Web 平台与后台系统, H5 营销与增长活动 |
| **#lab** (new, from truth-lab) | Truth Lab intro + manifesto quote, stats, 6 experiments, 13-run training table, hardware spec, GitHub links |
| **#team** (new) | Found the founder path timeline *从 NOIP 到 nanoGPT* (8 entries) |

## Also

- Hero/meta/title/nav/footer rewritten around the four lines; nav now: 关于 · 业务线 · 训练与推理 · AI 转型 · AI 应用 · 应用开发 · 案例 · 实验室 · 团队 · 计价 · 联系
- ~130 new EN strings in `i18n.js` (longest-key-first mechanism preserved), plus fixed a few **pre-existing untranslated** works cards (SEC-EDGAR GPT, 趣直播)
- New CSS in `style.css` for lines/lab-table/quote/timeline (light + dark themes)
- `scripts/build_cases.py` re-run — case pages/portfolio unchanged, CI check will pass
- Committed as `c66f342`; verified HTML balance, i18n coverage, and local serving (index + portfolio + cases all 200)

**Not done (your call):** I did **not** push (your CI deploys on push) and did **not** touch the `truth-lab` repo — its content now lives here, so you'll probably want to retire `truth-lab` (local dir + GitHub repo) and redirect truthlab.cc. Say the word and I'll push and/or clean it up.
