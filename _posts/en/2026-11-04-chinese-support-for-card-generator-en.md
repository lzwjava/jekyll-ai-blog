---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Support for Card Generator
translated: false
type: note
---

Done ✓ Chinese support is committed (`fc1d92c`), both cards regenerated and open in Preview now.

## 用法 / Usage

```bash
ww card --lang zh    # 中文名片 → card_output/business_card_zh.png
ww card --lang en    # English card → card_output/business_card_en.png
ww card              # defaults to en
```

## What changed

**`ww/card/card.py`**

- `--lang en|zh` flag (validated; default `en`)
- **中文内容** — from your ZH CV PDF: name **李智维**, role **AI 工程师**, location **中国广州**
- Chinese labels: `关于我` / `联系我`, contact labels 博客/领英/AI 作品集/软件作品集
- Chinese curated intro (6 行, ~150 字, from the resume profile)
- **CJK fonts** on macOS: STHeiti Medium (bold) + Hiragino Sans GB (body), with Noto Sans CJK Linux fallbacks
- **CJK 逐字换行** (`_wrap_cjk`) — breaks anywhere, prefers after spaces/punctuation, wider line-height (58px)
- `--llm` also writes the intro in Chinese (≤150 字) via OpenRouter; falls back to the curated intro on failure
- Outputs are language-suffixed: `business_card_{en,zh}.png` (both can coexist)

**`ww/main.py` + `~/.zsh/completions/_ww`** — help text and tab completion updated with `--lang en|zh`.

Verified: 李智维 bbox (0,3,216,70) = 3 real 72px glyphs (no tofu), CJK glyph = 38px wide at 38px font, ZH_INTRO wraps to 6 lines. Chinese cards now show both 中文 and English previews side by side — take a look and tell me if you'd like the zh intro wording or role tweaked.
