---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix reasoning model token limit
translated: false
type: note
---

Fixed both files. Here's the summary:

    Problem: DeepSeek v4 Flash is a reasoning model — it generates an internal chain-of-thought before the visible answer. With max_tokens=60, the reasoning alone consumed the entire budget, leaving content: null and finish_reason: "length".

    Fix: Bumped max_tokens from 60 → 300 in both files:
    - /home/xiaoxin/projects/ww/ww/note/create_note_utils.py:75
    - /home/xiaoxin/projects/ww/ww/note/screenshot_log.py:102

    300 tokens is enough headroom for reasoning + a ~6-word title. The model will still produce the short output you want — the extra budget just gives the reasoning phase room to breathe.

    Why 60 worked before: You were likely using a non-reasoning model (older DeepSeek, GPT, Claude) that doesn't have a separate reasoning/thinking phase. Those models turn tokens directly into visible output, so 60 tokens was plenty for "max 6 words." Switched to deepseek/deepseek-v4-flash which does add reasoning tokens.

    Try ww note again — it should work now.
