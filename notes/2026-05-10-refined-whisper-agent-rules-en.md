---
audio: false
generated: true
image: false
lang: en
layout: post
title: Refined Rules for Whisper Agent Enhancements
translated: false
type: note
---

Rule rewritten. Key adjustments vs. the original:

- **Comprehensive detail** is now the core directive — explicit "do NOT summarize," length-similar-to-input, examples of forbidden hand-waves like "various topics" / "and so on," and a list of specifics to preserve (function names, file paths, version numbers, model names).
- **Numeric normalization** ported from `transcript_agent.py` and expanded: "fifty K CNY" → "50K CNY", "GPT four" → "GPT-4", "two point five times" → "2.5x".
- **Whisper-specific speaker rule** (vs. transcript_agent's A:/B: labels): no labels at all, third-person narration, with explicit Q&A phrasing guidance.
- **Tone preservation** now calls out humor / frustration / hesitation explicitly.
- **Reorganization**: explicit permission to break original chronological order and group scattered topics together.
- **Language**: always English; translate-while-refining for Chinese with canonical-form rule for brand/technical names (e.g., "CUDA" not "kuda").
- **Output format**: hard rule — start directly with H1, no preamble.

Re-run the same command to see the difference:

```bash
ww whisper refine /Users/lzwjava/projects/private-projects/whisper-playground/yangyang/yangyang.txt
```
