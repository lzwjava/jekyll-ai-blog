---
audio: false
generated: true
image: false
lang: en
layout: post
title: "tt: Timesheet and Punch Card Verifier"
translated: false
type: note
---

## Summary

**Project:** `tt` — Timesheet and punch card verification tool for contractor attendance compliance.

**How it works:**
1. User registers (`tt register <id> <name>`) and logs in (`tt login <id>`)
2. Via REPL (`uv run tt` with no args), user runs `/add_records` which:
   - Takes a screenshot of a timesheet/punch card
   - Sends it to OpenRouter vision LLM (gemini-2.5-flash) for structured extraction
   - Saves extracted data to `data/<staff_id>/<record_type>.json`
   - Copies the image to `images/` with timestamped naming
3. `tt verify` cross-checks client timesheets against vendor punch cards
4. Reports weekly/monthly pass/fail against a 60% project-time threshold

**Current data:**
- 1 registered user: `45294575` (james.z.w.li)
- 5 weeks of client timesheet records extracted (May 2026)
- Project ratios: 80%, 80%, 80%, 100%, 100% — all passing

**Bugs fixed this session:**
1. `uv run tt` failed — missing `[build-system]` in pyproject.toml (hatchling added)
2. `tt status` crashed — `.session.json` picked up as contractor cache (hidden file filter added)
3. `uv.lock` removed from git tracking
4. GitHub remote URL updated to `lzwjava/tt`

**Architecture notes:**
- Two cache systems coexist: flat `data/<name>.json` (contractor verification cache from `tt verify`) and per-user `data/<staff_id>/<type>.json` (REPL records from `/add_records`)
- REPL has full tab completion, interactive prompts, and image extraction pipeline
- All data is Pydantic v2 models with JSON serialization
