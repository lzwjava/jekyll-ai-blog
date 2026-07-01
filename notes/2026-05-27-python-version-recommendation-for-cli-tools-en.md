---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Version Recommendation for CLI Tools
translated: false
type: note
---

**Question:** When did Python 3.11, 3.12, and 3.13 release? Given it's now 2026 and for a CLI toolkit like `ww`, what minimum Python version should I specify?

**Answer:**

## Release Timeline

| Version | Initial Release | EOL |
| --------- | ---------------- | ----- |
| 3.11.0 | Oct 24, 2022 | ~Oct 2027 |
| 3.12.0 | Oct 2, 2023 | ~Oct 2028 |
| 3.13.0 | Oct 7, 2024 | ~Oct 2029 |
| 3.14.0 | 2025 (alpha → stable Oct 2025) | ~Oct 2030 |

Notable: 3.12 is now in "security fixes only" stage — it no longer accepts regular bugfixes and binary installers are no longer provided. 3.13 is now the current stable feature release series, and 3.14 is the latest feature release series.

---

## What to Set for `ww`

Your `pyproject.toml` currently says `python >= 3.8`. That's too conservative for 2026. Here's the reasoning:

**Bump to `>=3.11` minimum.** Here's why:

**What you gain from 3.11+:**

- ~25% faster CPython (specializing adaptive interpreter) — matters for CLI startup time
- `tomllib` in stdlib (useful for config parsing)
- `ExceptionGroup` / `except*` — cleaner error handling in async code
- Much better tracebacks with precise error locations

**What you gain from 3.12+:**

- f-string improvements (nested expressions, multiline)
- `@override` decorator in `typing`
- Per-interpreter GIL (groundwork for real threading)
- But: it's now security-only, so you'd be pinning to a version no longer getting bugfixes

**What you gain from 3.13+:**

- New interactive REPL (colorized, multi-line)
- Experimental free-threaded mode (no GIL)
- Experimental JIT
- Active bugfix releases through ~2027

**Recommendation: `python >= 3.11`**

Rationale for `ww` specifically:

- It's a personal CLI toolkit, not a library others depend on — you control the runtime
- You're on macOS M2 (ships Python 3.12+ via Homebrew by default) and Ubuntu (easy to install 3.11+)
- 3.11 EOL is Oct 2027 — still 18 months out, plenty of runway
- Setting `>=3.12` is also fine and slightly better future-facing, but 3.11 maximizes compatibility if you ever share it without asking people to upgrade
- `>=3.13` is aggressive for a CLI tool — libraries like `Pillow`, `faiss-cpu`, some whisper bindings still have occasional lag on new versions

**If you want to be forward-leaning:** `>=3.12` is the sweet spot right now — still getting bugfixes until Oct 2028, widely available, and drops the dead weight of 3.8–3.10 syntax limitations.

In `pyproject.toml`:

```toml
[project]
requires-python = ">=3.12"
```

And in your GitHub Actions CI, test against `["3.12", "3.13"]` — skip 3.14 until it stabilizes in Oct 2025 final release.

---

**Bottom line:** Drop `>=3.8` — it's a 2019 version, EOL Oct 2024. Set `>=3.11` minimum, `>=3.12` preferred. You're not shipping a library with broad compatibility constraints, you're shipping your own tool on machines you control.
