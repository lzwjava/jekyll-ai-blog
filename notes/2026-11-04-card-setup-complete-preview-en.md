---
audio: false
generated: true
image: false
lang: en
layout: post
title: Card Setup Complete Preview
translated: false
type: note
---

Got it — I'll respond in English from now on.

To recap where we are: `ww card` is fully set up and committed with:

- **Avatar extraction** from your photo (macOS Vision face detection) → `card_output/avatar.jpg`
- **Bilingual cards** — `ww card --lang en` (English only, no Chinese) and `ww card --lang zh` (Chinese)
- **3-paragraph About Me**: career trust (TruthSoft founder, LeanCloud/TEKsystems, Fun Live/Square Root, 50+ delivered projects incl. Yuanfudao/Fenbi/Jiangsu TV/DBS/HSBC) · tech stack (Android/iOS, Vue/React/Angular, Java/Spring/Python, small-model training & inference, Alibaba Cloud/AWS/Azure) · profile + impact (b.1995 Guangzhou, NOIP top 300, IELTS 6.5, BFU dropout / GDUFS associate degree / CSTU MSc, 16K+ engineers, ~100K monthly views)
- **Contacts** (left panel): TruthSoft · Email · WeChat/WhatsApp · GitHub
- **High pixel density**: default 4200×2400 (2×), `--scale N` 1–8
- **Warm espresso/caramel theme** matched to your avatar's tones (last commit `44b18b3`)

All committed on `main`. The previews are open — take a look and let me know what you'd like next, e.g.:

- tweak the caramel accent (lighter/darker)
- try a light cream theme
- change any wording on either card
- add a `--theme` option to switch palettes

All commands you can run:
```bash
ww card --lang zh        # Chinese card
ww card --lang en        # English card
ww card --scale 3        # higher resolution
ww card avatar           # avatar only
```
