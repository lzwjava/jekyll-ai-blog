---
audio: false
generated: true
image: false
lang: en
layout: post
title: Translation Instruction Layers and Improvements
translated: false
type: note
---

Here's what the code reveals:

---

## Current State: Two Competing Mechanisms

### 1. `prompt` front matter field (the "proper" way)
Used in ~18 files. Example from `2024-11-24-review-2024-en.md`:

```yaml
prompt: Do not translate specific items such as Yin, Yin Wang, Zhiwei, etc.
```

This gets picked up in `scripts/translation/markdown_translate_client.py:27`:
```python
front_matter_prompt = front_matter_dict_copy.get("prompt", None)
```

Then injected into the LLM **system prompt** via `translate_client.py:127-128`:
```python
if front_matter:
    head += f"{front_matter}\n"
```

This is reliable — the LLM sees it as an instruction, not content.

### 2. `**AI Translation tips:**` inline in body (the niyao way)
Only in `2026-05-28-niyao-en.md`. This is just markdown body content — the LLM sees it as article text, not a structured instruction. It works because LLMs are smart enough to infer intent, but it's fragile and non-standard.

### 3. Hardcoded global term maps (code-level)
In `translate_client.py:56-68` and `translate_lang.py:22-34`:
```python
zh_term_map = {
    "Zhiwei": "智维",
    "Zhiwei Li": "李智维",
    "Yin Wang": "王垠",
    "Fun Live": "趣直播",
    # ... 11 terms total
}
```

Plus validation in `translate_validate_utils.py` — `check_prohibited_zh_terms()` catches "志炜", `check_yin_wang_mistranslation()` catches "阴王"/"王寅".

---

## The Problem

You have **3 layers** doing the same thing differently:
- Global hardcoded maps in Python code (requires code change to update)
- Per-file `prompt:` field in front matter (freeform string, no structure)
- Inline `**AI Translation tips:**` in body (fragile, non-standard)

The niyao post's approach is clever — it keeps name mappings co-located with the content. But it should be in `prompt:` front matter, not inline in the body.

---

## What Could Be Better

**Option A: Migrate inline tips to `prompt:` field** (minimal change)

Move the niyao tips to front matter:
```yaml
prompt: "AI Translation tips: Niyao (倪瑶), Zhiwei Li (李智维), Xiaohe Meditation (小荷冥想), Zhuoyebang (作业帮), Tang Qiao (唐巧), Wang Wei (王巍)"
```

This is already supported — `markdown_translate_client.py` already injects `prompt` into the system prompt. Just delete the inline line from the body.

**Option B: Structured `translation_hints:` front matter** (cleaner)

Replace the freeform `prompt:` with a structured field:
```yaml
translation_hints:
  zh:
    Niyao: 倪瑶
    Xiaohe Meditation: 小荷冥想
    Zhuoyebang: 作业帮
```

Then update `translate_client.py` to read this field and build term-specific rules automatically, similar to how the hardcoded `zh_term_map` works but per-file. This would:
- Be machine-parseable (no regex parsing of prose)
- Allow language-specific hints (different mappings for zh vs ja)
- Merge cleanly with the global map (per-file overrides global)

**Option C: Move global maps to a YAML config file** (best long-term)

Extract the hardcoded `zh_term_map` from code into `scripts/translation/term_map.yaml`:
```yaml
zh:
  Zhiwei: 智维
  "Zhiwei Li": 李智维
  "Yin Wang": 王垠
  # ...
```

Per-file `translation_hints:` in front matter overrides entries from this global map. No code change needed to add new terms.

---

## My Recommendation

Do A now (30 seconds), then C when you have 15 minutes:

1. **Now**: Move the niyao inline tips to `prompt:` front matter, delete the inline line. Already works with existing code.

2. **Soon**: Extract `zh_term_map` to a YAML config, update `get_language_specific_preamble()` to load from it. Then per-file `translation_hints:` can extend/override without code changes.

Want me to do step 1 now?