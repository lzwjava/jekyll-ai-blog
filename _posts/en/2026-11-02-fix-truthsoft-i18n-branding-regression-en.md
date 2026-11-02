---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix TruthSoft i18n branding regression
translated: false
type: note
---

Done. The previous commit had replaced the brand with the literal text "TruthSoft" directly in the HTML, which broke i18n: the Chinese site is source-first, and `i18n.js` swaps exact "求真软件" → "TruthSoft" when switching to English. With the literal swap, Chinese mode showed "TruthSoft" and the translation key no longer matched.

What I corrected:

- **index.html / portfolio.html** — restored 求真软件 in the Chinese-source spots (page `<title>`, nav brand, footer). i18n.js already maps 求真软件 → TruthSoft, so English mode renders the English name correctly.
- **TruthSoft** now only appears in genuinely English-facing places, which is correct:
  - i18n EN dictionary (求真软件 → TruthSoft), EN_TITLE, EN_META
  - per-page `i18nTitleEn` / `i18nMetaEn` on portfolio
  - the decorative English about-section kicker (`TruthSoft · Think clearly. ...`)
  - meta description keeps both: 求真软件（TruthSoft）
- **scripts/build_cases.py** — fixed the stale "Truth Software" → "TruthSoft" in the generated portfolio EN meta, then regenerated all cases/portfolio
- **README.md** — updated header and about section to TruthSoft

Verified: no more "Truth Software" anywhere, and every nav/footer in the Chinese source now reads 求真软件 across index, portfolio, and all 12 case pages.

为新改动已提交为 `5b8b3b8`。
