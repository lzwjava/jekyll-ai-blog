---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bilingual and Theme Toggle Added
translated: false
type: note
---

Done. Both features are live in the single `index.html` (86.5 KB, still no build step).

## What was added

**🌐 EN / 中文 toggle** (pill switch in the header)

- Full, hand-translated Chinese version of every section — hero, stats, focus areas, experiments, the entire lab notebook (training tables, statuses, GPU builds), services, about timeline, contact, footer, nav
- Instant in-place switch (no reload), animated anchor navigation that jumps to the matching section in the *active* language block
- Language persists in `localStorage`; auto-detects `zh` browsers; pre-paint script prevents any flicker; `<html lang>` and page title/meta description swap correctly
- Brand/project names (vLLM, nanoGPT, SEC-EDGAR-GPT…) intentionally stay in English

**☀/☾ Dark / light mode toggle**

- Light theme via CSS variables — warm paper background, dark-ink text, adjusted amber accent for contrast
- Persists in `localStorage`; defaults respect `prefers-color-scheme`; pre-paint script prevents white flash; `theme-color` meta and header blur adapt

## Verified

- HTML valid: no unclosed/mismatched tags, no duplicate IDs
- Both scripts pass `node --check`
- Simulated the full control flow in Node with a DOM stub:
  - EN→中文→EN switching, `lang="zh-CN"`, titles, stored prefs
  - theme light↔dark with `theme-color` meta updates
  - reload with stored prefs restores `zh` + `light`
  - anchor scroll resolves against the active language block
- All 7 sections present in both languages

To preview:

```bash
cd /Users/lzwjava/projects/truth-labs && python3 -m http.server 8080
```

One thing worth a skim: I translated everything myself, so give the Chinese copy a once-over for tone — especially the manifesto quote and tagline translations.
