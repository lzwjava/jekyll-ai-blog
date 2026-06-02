---
audio: false
generated: true
image: false
lang: en
layout: post
title: Squirrel for macOS Double Pinyin
translated: false
type: note
---

**Question:** Is there an open-source double pinyin (shuangpin) input method for macOS? I currently use WeChat input method but want something open source.

**Answer:**

The answer is **RIME / Squirrel** — it's the definitive open-source choice, and it has first-class shuangpin support built in.

---

## RIME (Squirrel) — The Only Real Answer

RIME is a highly customizable cross-platform (Windows, Mac, Linux) open-source input method engine. It provides the right user experience out of the box and has all the characters you need. On macOS the frontend is called **Squirrel** (鼠须管), powered by the Rime Input Method Engine and other open-source technologies.

GitHub: [rime/squirrel](https://github.com/rime/squirrel)

---

## Install

```bash
brew install --cask squirrel
```

Then log out and log back in. Go to **System Settings → Keyboard → Text Input → Edit**, search "Squirrel", add it.

---

## Enable Double Pinyin (Shuangpin)

RIME ships with multiple shuangpin schemas out of the box. The most popular ones:

| Schema ID | Layout |
|---|---|
| `double_pinyin` | 自然码 (Ziranma) |
| `double_pinyin_flypy` | 小鹤 (Xiaohe/Flypy) — most popular today |
| `double_pinyin_mspy` | 微软双拼 (Microsoft) |
| `double_pinyin_abc` | 智能ABC |
| `double_pinyin_thunisoft` | 紫光 |

Create `~/.config/rime/default.custom.yaml` (or `~/Library/Rime/default.custom.yaml` on macOS):

```yaml
patch:
  schema_list:
    - schema: double_pinyin_flypy   # or double_pinyin for ziranma
```

Then click the RIME menu bar icon → **Deploy** (重新部署). Done.

---

## Recommended: Weasel/Rime + 雾凇拼音 dict for better word coverage

The default dictionary is lean. The community-maintained **雾凇拼音** (rime-ice) gives you ~2.2M words:

```bash
# Install rime-ice schema pack
cd ~/Library/Rime
curl -fsSL https://git.io/rime-install | bash -s -- iDvel/rime-ice:others/recipes/full
```

Or manually: [iDvel/rime-ice](https://github.com/iDvel/rime-ice) — this is what most power users run. It has a `double_pinyin_flypy` schema pre-configured with a huge dictionary.

---

## Quick config example (`~/Library/Rime/squirrel.custom.yaml`)

```yaml
patch:
  # Candidate window style
  style/horizontal: false
  style/font_face: "PingFang SC"
  style/font_point: 16
  style/candidate_list_layout: linear
```

---

## Summary

- **Squirrel (RIME)** — 100% open source (BSD/GPL), actively maintained, shuangpin built-in, huge community schema ecosystem
- Apple's built-in shuangpin exists but is closed source as you suspected
- WeChat IME: closed, phones home to Tencent — not ideal for a privacy-conscious dev workflow

RIME is the standard choice in the Chinese hacker/programmer community. After installing, navigate to System Preferences → Keyboard → Text Input → Edit, and search for "Chinese" to add "Squirrel" to text input options. The initial setup takes maybe 10 minutes, and after that it's fully local, fully customizable via YAML, and zero telemetry.

**References:**

- [rime/squirrel — GitHub](https://github.com/rime/squirrel)
- [iDvel/rime-ice — 雾凇拼音 (large dict + shuangpin configs)](https://github.com/iDvel/rime-ice)
- [Configuring Rime on macOS — bdim.moe](https://blog.bdim.moe/posts/configuring-rime-input-method-on-macos/)
