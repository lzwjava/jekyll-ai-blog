---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes AGENTS.md Loading Rules
translated: false
type: note
---

Here's how Hermes loads per-project AGENTS.md:

**Entry point:** `build_context_files_prompt()` in `agent/prompt_builder.py` (line 1412)

**Priority chain (first match wins — only ONE project context type loaded):**

1. `.hermes.md` / `HERMES.md` — walks from cwd up to git root
2. `AGENTS.md` / `agents.md` — cwd only (no walk)
3. `CLAUDE.md` / `claude.md` — cwd only
4. `.cursorrules` + `.cursor/rules/*.mdc` — cwd only

**How AGENTS.md specifically works (`_load_agents_md`, line 1350):**

```python
def _load_agents_md(cwd_path: Path) -> str:
    for name in ["AGENTS.md", "agents.md"]:
        candidate = cwd_path / name
        if candidate.exists():
            content = candidate.read_text(encoding="utf-8").strip()
            content = _scan_context_content(content, name)  # security scan
            result = f"## {name}\n\n{content}"
            return _truncate_content(result, "AGENTS.md")  # cap at 20k chars
    return ""
```

It checks cwd only — no directory walking. If you're in `/Users/lzwjava/projects/hermes-agent`, it looks for `AGENTS.md` right there.

**The key difference with `.hermes.md`:** `_find_hermes_md` (line 79) walks from cwd up through parent directories until it hits the git root. So `.hermes.md` at the repo root gets found even when you're in a subdirectory.

**Integration into system prompt (`agent/system_prompt.py`, line 269):**

```python
context_files_prompt = _r.build_context_files_prompt(...)
```

This gets prepended to the system prompt as `# Project Context` with the note "The following project context files have been loaded and should be followed."

**Security:** `_scan_context_content` (line 44) runs a threat-pattern scan on the content before injection. If it detects prompt injection patterns, the file is BLOCKED and a warning is logged instead of injecting the content.

**Truncation:** `_truncate_content` caps each context source at 20,000 chars.

**Cron jobs:** When a cron job has a `workdir` set, `build_context_files_prompt()` is called with that directory as cwd, so AGENTS.md from the project directory gets injected into the cron session's system prompt (see `cron/scheduler.py` line 1648).
