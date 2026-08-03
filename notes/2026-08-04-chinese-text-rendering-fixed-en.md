---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chinese Text Rendering Fixed
translated: false
type: note
---

## ✅ Chinese text rendering fixed

### Root cause
The remote box had **zero CJK fonts** (only DejaVu). `video.py`'s font loader for Chinese text looks for `NotoSansCJK-Black.ttc` / `NotoSerifCJK-Bold.ttc` / `wqy-zenhei.ttc` — none existed, so it silently fell back to **PIL's default bitmap font**, which has no CJK glyphs → Chinese title/subtitle rendered as **tofu boxes (□□□)**.

### Fixes applied
1. **Installed `fonts-noto-cjk`** on the remote → provides `NotoSansCJK-Regular.ttc`, `NotoSansCJK-Bold.ttc`, `NotoSerifCJK-*.ttc`
2. **Patched `video.py`** (commit `f7f5d68`):
   - Added `NotoSansCJK-Bold.ttc` (SC face) to the title candidates — Ubuntu 24.04's package ships **Bold but not Black**, which was the first title candidate
   - `_load_font(..., cjk=True)` now has a **fontconfig `fc-match ':lang=zh-cn'` last-resort fallback**, so Chinese text can never silently drop to tofu again even if font paths change
3. **Redeployed + restarted the server** (health 200, tunnel still live)

### Verified on the remote

| Check | Result |
|---|---|
| Font loading | `Noto Sans CJK SC` Bold (title) + Regular (subtitle) ✓ |
| Full slide render | `_create_slide_frame("AI 短视频创作工坊", "用人工智能…")` → 1080×1920 PNG ✓ |
| fc-match fallback | present in the running code ✓ |
| Public URL | `https://rc-63980f23582dde21.radeon.firstdg.ai/health` → 200 ✓ |

### One thing to know about in-image Chinese
FLUX (like most diffusion models) renders Chinese text **inside the generated scene images** poorly — you'll get garbled pseudo-characters if the image prompt asks for Chinese signage. That's a model limitation, not a code bug. Best practice for the pipeline: keep scene **image prompts in English** and let the LLM storyboard translate; use Chinese only in **title/subtitle overlays** — which now render correctly with Noto Sans CJK SC.

Want me to also add an auto-translate step in `gen-video` (LLM translates Chinese scene prompts → English before image generation)? That would make Chinese prompts produce clean videos end-to-end.
