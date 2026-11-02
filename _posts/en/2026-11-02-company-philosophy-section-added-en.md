---
audio: false
generated: true
image: false
lang: en
layout: post
title: Company Philosophy Section Added
translated: false
type: note
---

All done. The company philosophy is now featured in the "我们信奉什么" (What We Believe) section.

**Changes:**

1. **`index.html`** — Added a highlighted philosophy band after the six belief cards in the About section:
   - Tag: **公司哲学**
   - Headline: **又快又好 —— 快，绝不牺牲质量** (Fast AND good — speed without sacrificing quality)
   - Description: fast is a promise (small steps, weekly delivery, same-day start, never leaving customers waiting); good is the baseline (clean code, sustainable architecture, every release survives launch and time) — making both true at once via process, automation, and AI leverage.

2. **`style.css`** — New `.philosophy` band styling: centered card with a gradient border (matches the site's orange→pink→purple accent gradient), adaptive `--bg-alt` interior for both light/dark themes, plus responsive sizing at ≤640px.

3. **`i18n.js`** — Added English translations so the band switches correctly with the EN toggle:
   - 公司哲学 → Our Company Philosophy
   - 又快又好 —— 快，绝不牺牲质量 → Fast AND good — speed without sacrificing quality
   - Full description translated as well.

I verified the i18n keys exactly match the HTML text nodes, so the language toggle will translate the new band properly.
