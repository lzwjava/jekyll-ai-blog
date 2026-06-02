---
audio: false
generated: true
image: false
lang: en
layout: post
title: Timesheet Verification and Cross-Checking Tool
translated: false
type: note
---

Done. Here's what was built:

```
tt/
├── __init__.py
├── cli.py          # CLI: tt verify [-i DIR] [-m MODEL] [-t THRESHOLD]
├── models.py       # Pydantic: ClientWeek, VendorPunchDay, VerificationResult, etc.
├── extractor.py    # Vision LLM extraction via OpenRouter (client timesheets, punch cards, vendor timesheets)
├── verify.py       # Cross-check logic + weekly/monthly threshold verification
└── openrouter.py   # OpenRouter API client (your code, added call_openrouter_vision)
```

Usage:

```bash
uv run tt verify                           # run with defaults
uv run tt verify -i input -m google/gemini-2.5-flash -t 0.60
```

What `tt verify` does:
1. Reads all images from `input/client/`, `input/vendor/punch/`, `input/vendor/timesheet/`
2. Sends each to a vision LLM via OpenRouter to extract structured JSON
3. Cross-references: flags days where client logged hours but vendor shows missed punch (and vice versa)
4. Calculates weekly project ratios (must be ≥ 60%) and monthly aggregate (must be ≥ 60%)
5. Prints a table and exits 0 (SATISFIED) or 1 (NOT SATISFIED)

Set `OPENROUTER_API_KEY` in `.env` or environment to run. The default model is `google/gemini-2.5-flash`.
