---
audio: false
generated: true
image: false
lang: en
layout: post
title: ZenMux Documentation Site
translated: false
type: note
---

This is the **ZenMux documentation site** — the source repo for [docs.zenmux.ai](https://docs.zenmux.ai).

**ZenMux** is an LLM API aggregation service (a unified gateway for multiple AI model providers). This repo builds its documentation site using **VitePress** with:

- **Bilingual** — Chinese-first workflow, auto-translated to English
- **Custom vitepress plugins** — tabbed API examples (`api-request` container), compressed page data via LZ-String, locale-based rewrites
- **AI-powered translation pipeline** — scripts that use the ZenMux API itself (via `openai/gpt-5`) to translate `zh/` → `en/`
- **GitHub Pages deployment** — `pnpm run build` outputs to the `docs/` directory, auto-deploys on push to `main`
- **Custom domain** — docs.zenmux.ai
