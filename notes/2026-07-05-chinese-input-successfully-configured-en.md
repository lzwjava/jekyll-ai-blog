---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Input Successfully Configured
translated: false
type: note
---

Done. Chinese input is now **fully set up and working**. Here's the summary:

---

## Status: Already Installed & Configured

| Item | Status |
| ------ | -------- |
| **IBus** + **ibus-libpinyin** | Installed |
| **GNOME input source** | Added (`ibus libpinyin`) |
| **IBus daemon** | Running |
| **Active engine** | `libpinyin` ✅ |

## How to use

**Switch input method**: `Super` + `Space` (or click top bar where it shows "EN")

**Type pinyin**: just start typing `nihao` → candidates appear

**Back to English**: `Super` + `Space` again

## Quick test

Open any text app (terminal, browser, whatever) and type. The pinyin engine is live right now.

---

No install step needed — everything was already there on your Ubuntu 24.04. The libpinyin IBus engine was added as an input source but the engine wasn't activated. I set it to `libpinyin` so it should switch in from the GNOME input menu now.
