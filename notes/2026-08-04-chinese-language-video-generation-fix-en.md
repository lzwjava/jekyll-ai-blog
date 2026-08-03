---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Language Video Generation Fix
translated: false
type: note
---

Done. ✅ Here's the summary of the analysis and what was built:

## Analysis findings (why you saw English video text)

| # | Issue | Detail |
| --- | --- | --- |
| 1 | **Prompt bias** | Scene generation used English examples + *word-count* limits ("2-6 words") — meaningless for Chinese, so the LLM defaulted to English titles/subtitles even for Chinese articles |
| 2 | **No CJK font** | DejaVu/Liberation/Arial (the only candidates) don't cover CJK — verified via `fc-match`: 是/军 exist **only** in NotoSansCJK. Chinese would've rendered as □□□ tofu |
| 3 | **Space-based wrapping** | `text.split()` can't break Chinese (no spaces) → one unbreakable line → font shrinks to unreadable size |

## What I built — Language selector (Auto / English / 中文)

**Frontend** (`server.py`): New **Language** dropdown in Step 1 next to the topic input; sent with both `/api/generate-content` and `/api/generate-video`.

**Backend** (`server.py` + `video.py`):

- `language` field on both request models → threaded through `_run_generation` → `generate_video_from_content` → `_generate_scenes`
- **Content prompt**: writes the article in the chosen language (Auto = same as topic)
- **Scene prompt**: language-aware — for 中文 uses character counts ("title: 2-8 个汉字, subtitle: 10-25 个汉字") instead of word counts; `image_prompt` stays English for best Flux quality

**Rendering** (`video.py` `_create_slide_frame`):

- **CJK font detection**: if title/subtitle contain CJK, loads **Noto Sans CJK SC** (Black for title, Regular for subtitle) with WenQuanYi fallback — these also cover Latin, so mixed text like "GPU是什么？" renders perfectly
- **Character-based wrapping** for CJK (plus hard-break for over-long tokens in any language)
- The existing auto-shrink loops now re-load fonts via the same candidate list (preserving the correct `.ttc` face index)

**Verified**: rendered Chinese slides ("GPU是什么？", "并行计算之王", long 13-char titles, long subtitles) — all fit inside their bars with proper glyphs.

**Committed & pushed**: `f1eda19` → `origin/main`. Server running at `http://localhost:8000` — try the 中文 topic with **中文** selected and the video titles/subtitles will now be Chinese.
