---
audio: false
generated: true
image: false
lang: en
layout: post
title: RIME Sogou Shuangpin Setup Summary
translated: false
type: note
---

Here's a comprehensive summary of what's been set up and what you now have:

---

## What Was Installed

**Squirrel (鼠须管) v1.1.2** — the macOS frontend for the RIME Input Method Engine.

- Installed via `brew install --cask squirrel`
- Location: `/Library/Input Methods/Squirrel.app`
- Config dir: `~/Library/Rime/`

**rime-ice (雾凇拼音)** — the best community-maintained RIME dictionary/schemas package.

- Installed via plum (RIME package manager) into `~/Library/Rime/`
- Source: [iDvel/rime-ice](https://github.com/iDvel/rime-ice)

---

## What's In Your ~/Library/Rime/

```
default.custom.yaml          ← Your schema selection (Sogou shuangpin)
double_pinyin_sogou.schema.yaml  ← Sogou shuangpin schema (from rime-ice)
cn_dicts/                    ← 6 Chinese dictionaries (~2.2M words)
  ├── 41448.dict.yaml        ← 41,448 most common chars
  ├── 8105.dict.yaml         ← 8,105 standard chars (GB2312+)
  ├── base.dict.yaml         ← Base dictionary
  ├── ext.dict.yaml          ← Extended vocabulary
  ├── others.dict.yaml       ← Supplementary words
  └── tencent.dict.yaml      ← Tencent corpus (modern slang, names)
en_dicts/                    ← English mixed-input dictionaries
  ├── en.dict.yaml           ← English words
  ├── en_ext.dict.yaml       ← Extended English
  └── cn_en_sogou.txt        ← Chinese-English mixed terms (Sogou-specific)
lua/                         ← Lua plugins (auto-cap, date, emoji, etc.)
opencc/                      ← OpenCC (emoji, traditional/simplified conversion)
squirrel.yaml                ← Squirrel appearance config (from rime-ice)
symbols_v.yaml               ← Press V for symbol picker
symbols_caps_v.yaml          ← CapsLock+V for more symbols
custom_phrase.txt            ← Your custom phrases (empty, for you to fill)
```

---

## Features You Get Out of the Box

| Feature | How to use |
|---|---|
| Sogou double pinyin | Just type normally — it's your default schema |
| Huge dictionary | 2.2M+ Chinese words, modern slang, internet terms |
| English mixed input | Type English words inline without switching (e.g. "hello" works) |
| Emoji input | Type emoji names in Chinese, get emoji candidates |
| Symbol picker | Press `V` then a key for symbols (arrows, math, currency) |
| Date/time | Type `rq` (日期) for date, `sj` (时间) for time, `xq` (星期) for weekday |
| Custom phrases | Edit `~/Library/Rime/custom_phrase.txt` to add your own |
| Traditional Chinese | Built-in OpenCC conversion available |

---

## Key Shortcuts (Default Squirrel Keybindings)

| Shortcut | Action |
|---|---|
| `Ctrl+Space` or `Ctrl+`` | Toggle input method (macOS system) |
| `Shift` | Toggle Chinese/English |
| `Enter` | Commit raw pinyin as-is |
| `Escape` | Clear current input |
| `[` / `]` | Page up / down candidates |
| `Shift+Enter` | Commit as uppercase English |
| `Ctrl+.` | Toggle full/half-width punctuation |

---

## RIME Deploy Workflow

Whenever you edit any file in `~/Library/Rime/`:

1. Click the Squirrel icon in the menu bar
2. Click **"重新部署" (Deploy)**
3. Wait for compilation (~10-30s first time, instant after)

Or use keyboard: `Ctrl+Option+`` (if configured).

---

## Customization Tips

**Appearance** — edit `~/Library/Rime/squirrel.custom.yaml`:

```yaml
patch:
  style/font_face: "PingFang SC"
  style/font_point: 16
  style/horizontal: false          # vertical candidate list
  style/candidate_format: "%c. %@" # show number labels
```

**Add more schemas** — edit `~/Library/Rime/default.custom.yaml`:

```yaml
patch:
  schema_list:
    - schema: double_pinyin_sogou
    - schema: rime_ice          # full pinyin as fallback
```

**Custom phrases** — edit `~/Library/Rime/custom_phrase.txt`:

```
# format: word<Tab>pinyin<Tab>priority
github	github	100
```

**Update rime-ice** (pull latest dicts/schemas):

```bash
cd ~/Library/Rime && bash plum/bin/rime-install iDvel/rime-ice:others/recipes/full
```

---

## Switching From WeChat IME

- WeChat IME is closed-source and phones home to Tencent
- Squirrel is 100% local, zero telemetry, fully offline
- All config is plain YAML — version-controllable, portable
- Your Sogou muscle memory transfers directly (same key mappings)

---

## Next Steps After Login

1. Log out / log back in
2. System Settings → Keyboard → Text Input → Edit → add "Squirrel"
3. Switch to Squirrel via menu bar or `Ctrl+``
4. Click Deploy (重新部署) — wait for dictionary build
5. Start typing — you should see Sogou shuangpin working with rich candidates