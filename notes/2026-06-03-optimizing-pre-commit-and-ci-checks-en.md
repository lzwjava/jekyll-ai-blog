---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Pre-commit and CI Checks
translated: false
type: note
---

**Question:** How should you architect pre-commit hooks vs GitHub Actions to balance developer velocity with code quality, given your codebase and workflow?

**Answer:**

You've identified the core tradeoff correctly: **pre-commit is synchronous friction, CI is async safety**. Here's the decision framework:

### Categorize by Latency

| Check | Latency | Blocks Dev? | Verdict |
|-------|---------|------------|---------|
| **Fast (<100ms)** | trailing-ws, end-of-file, yaml, toml, json, merge-conflict, ast, case-conflict | ✅ Yes | Pre-commit |
| **Medium (500ms-2s)** | ruff (check+format), shellcheck, mixed-line-ending | ⚠️ Maybe | Pre-commit, but config for speed |
| **Slow (5s+)** | pyright (type-checking w/ dependencies), bandit (recursive scan) | ❌ No | GitHub Actions only |
| **Context-dependent** | Large file checks, tests | ❌ No | GitHub Actions |

### Your Current Config: Problems

1. **`pyright` with 20+ dependencies** — This is your killer. Type-checking Python with torch, tensorflow, cloud SDKs can take 5-15s even on fast machines. Blocks every commit. Move to GH Actions.

2. **`bandit -r scripts/`** — Recursive security scanning on a growing codebase will slow down linearly. Either:
   - Move to GH Actions (runs once, not per-commit)
   - Or keep it but only scan changed files (requires pre-commit plugin config)

3. **`ruff-format` on large codebases** — If you have hundreds of Python files, formatting can take 2-5s. Test locally: `time ruff format .`

### Recommended Split

**Pre-commit (keep local, fast feedback):**

```yaml
- Basic hygiene: trailing-ws, end-of-file, mixed-line-ending, case-conflict
- Structured data: check-yaml, check-toml, check-json (fast, deterministic)
- Code syntax: check-ast, debug-statements, check-executables-have-shebangs
- Conflict markers: check-merge-conflict
- Size limits: check-added-large-files (catches accidental binary commits)
- Ruff formatting & lint (ONLY on changed files, stage them)
```

**GitHub Actions (async, comprehensive):**

```yaml
- pyright (type-checking)
- bandit (security scan)
- Additional linters (eslint, markdown lint)
- Tests (pytest, integration tests)
- Build checks (if applicable)
```

### Config Optimization

**Make ruff faster on pre-commit:**

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.9.10
  hooks:
    - id: ruff
      args: [--fix, --select, "E,W,F,I,UP"]  # Focus on essential rules, not all
    - id: ruff-format
      stages: [commit]  # Only on commit, not on push
```

**Move pyright to GH Actions:**

```yaml
# .github/workflows/type-check.yml
name: Type Check
on: [pull_request, push]
jobs:
  pyright:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install pyright torch ... (dependencies)
      - run: pyright scripts/
```

**Bandit in GH Actions only:**
Remove from pre-commit entirely. Add to GH Actions, runs once per PR.

### Measuring Impact

Before changing anything, measure your current setup:

```bash
# Time each hook
time pre-commit run --all-files
time pre-commit run pyright --all-files
time pre-commit run bandit --all-files
```

If any hook takes >2s, move it to CI. Rule of thumb: **if devs see >3s total pre-commit latency, they start using `--no-verify`**.

### Your Specific Case

Given you:

- Ship fast
- Use CLI-first workflows
- Have a heterogeneous codebase (Python, shell, YAML, markdown)
- Care about CI rigor (security, types)

**I'd recommend:**

```yaml
# Keep in pre-commit (< 1s total)
- trailing-whitespace, end-of-file, mixed-line-ending
- check-yaml, check-toml, check-json
- check-ast, debug-statements, check-merge-conflict
- ruff (format + essential lint rules only)
- shellcheck

# Remove from pre-commit, move to GH Actions
- pyright (expensive type-check)
- bandit (security, run async)
```

Then add to `.github/workflows/quality.yml`:

- Full pyright scan
- bandit security scan
- Any integration tests

This way: **commit is instant, feedback is comprehensive async, and you never feel friction when iterating locally**.

### The Question You Asked: "How Frequently Do They Fail?"

This depends on your team discipline. In a well-maintained codebase:

- Basic hygiene checks fail <1% (mostly accidental)
- Ruff lint fails ~5-10% (catches real issues)
- Pyright fails ~10-20% (types are stricter)
- Bandit fails <1% (mostly false positives you skip anyway)

If you see >30% failure rate on any hook, either:

1. The hook is too strict (disable/configure)
2. Your codebase quality is degrading (address root cause)

**TL;DR:** Pre-commit = fast local feedback loop. CI = comprehensive async checks. Move anything >2s to CI. You'll ship faster and catch issues before PR merge.
