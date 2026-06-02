---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Coverage Guide Essentials
translated: false
type: note
---

Here’s a practical, dev-focused intro to the **coverage** (coverage.py) package—what it measures, how to use it well, and the knobs you’ll actually care about.

# What coverage.py is

* A Python tool that **measures which lines and branches of your code run** during tests or any execution.
* Outputs **text, HTML, XML, and JSON** reports so you can see gaps and wire it into CI quality gates.
* Works with unittest, pytest, nose, or plain scripts.

# Core concepts (in plain terms)

* **Line coverage**: Did a line run at least once?
* **Branch coverage**: Did each possible branch of a decision run? (if/else, boolean short-circuit, exceptions, comprehensions, etc.)
* **Source selection**: Only measure your own code to avoid noise from venv/site-packages.
* **Data storage**: Runs create a `.coverage` (SQLite) data file; you can merge many runs.
* **Contexts**: Tag execution with labels (e.g., per test), so you can slice reports by test names, commands, etc.

# Quick start

```bash
# 1) Install
pip install coverage

# 2) Run your tests under coverage (pytest is just an example)
coverage run -m pytest

# 3) See a terminal report (with missing-line numbers)
coverage report -m

# 4) Generate HTML (open htmlcov/index.html in a browser)
coverage html

# Optional: machine-readable reports
coverage xml        # for CI tools like Sonar, Jenkins, Azure DevOps
coverage json       # scripted analysis
```

# Recommended .coveragerc

Create a config at your repo root to make results consistent locally and in CI.

```ini
[run]
# Only measure your packages to keep noise down
source = src, your_package
branch = True
parallel = True                 # allow multiple processes/runs to write their own data
relative_files = True           # cleaner paths in reports (CI-friendly)
concurrency = thread, multiprocessing

# You can also exclude files or patterns entirely
omit =
    */tests/*
    */.venv/*
    */site-packages/*
    */migrations/*

[report]
show_missing = True
skip_covered = False            # set True if you want a shorter report
fail_under = 90                 # make CI fail if coverage is below 90%
exclude_lines =
    pragma: no cover            # standard pragma to ignore lines
    if TYPE_CHECKING:
    raise NotImplementedError

[html]
directory = htmlcov
title = Coverage Report

[xml]
output = coverage.xml

[json]
output = coverage.json

[paths]
# Useful when combining data from different machines/containers
source =
    src
    */workspace/src
    */checkouts/your_repo/src
```

# Measuring subprocesses & parallel runs

If your code spawns subprocesses (multiprocessing, CLI tools), set up **subprocess coverage**:

1. In `[run]`, keep `parallel = True`.
2. Export an env var so subprocesses auto-start coverage with the same config:

```bash
export COVERAGE_PROCESS_START=$(pwd)/.coveragerc
```

3. Run your program/tests normally (or still via `coverage run -m ...`).
4. After all runs finish, merge data and report:

```bash
coverage combine
coverage report -m
```

> Tip: `concurrency = multiprocessing, thread, gevent, eventlet, greenlet` lets coverage hook into different async models.

# Branch coverage & pragmas

* Enable `branch = True` in `[run]`. This catches missed `else` arms, short-circuits, exception paths, etc.
* Ignore untestable lines with a trailing comment:

  * `# pragma: no cover` — exclude that line from coverage.
  * For tricky branches, refactor rather than overusing pragmas.

# Contexts (slice coverage by test or task)

Contexts attach labels to executed lines so you can answer: “Which tests cover this code?”

* Easiest with pytest:

  * In `.coveragerc` add `dynamic_context = test_function`.
  * Then `coverage html --show-contexts` or inspect per-context data to see which test touched a line.
* You can also set `dynamic_context = test` (test nodeid) or `dynacontext` via env in custom runners.

# Pytest integration

Two common patterns:

**A. Native coverage CLI (simple & fast)**

```bash
coverage run -m pytest -q
coverage report -m
```

**B. pytest-cov plugin (adds CLI sugar)**

```bash
pip install pytest-cov
pytest --cov=your_package --cov-branch --cov-report=term-missing --cov-report=html
```

Both end up using coverage.py under the hood; use whichever matches your team conventions.

# Typical CI wiring (GitHub Actions sketch)

```yaml
- name: Install
  run: pip install -U pip coverage pytest

- name: Test with coverage
  run: |
    coverage run -m pytest -q
    coverage report -m
    coverage xml
- name: Enforce threshold
  run: coverage report --fail-under=90
- name: Upload HTML
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: htmlcov
    path: htmlcov/
```

# Common pitfalls & fixes

* **Huge/slow reports**: Restrict `source=` and use `omit=` to skip venv, tests, generated code.
* **Different paths on CI vs local**: Add a `[paths]` section so `coverage combine` merges datasets.
* **Subprocesses not measured**: Set `COVERAGE_PROCESS_START` and keep `parallel = True`, then `coverage combine`.
* **Async frameworks**: Add the relevant entry to `concurrency = ...`.
* **C extensions**: coverage.py measures Python, not native code—write harness tests around the Python boundary.
* **False negatives on unreachable code**: Mark with `# pragma: no cover`, but consider refactoring to make behavior testable.

# Handy commands you’ll actually use

```bash
coverage erase                       # clean previous data
coverage run -m pytest               # collect
coverage report -m                   # text summary with missing lines
coverage html                        # open htmlcov/index.html
coverage xml                         # CI parsers
coverage json                        # scripts/automation
coverage combine                     # merge parallel/subprocess data
coverage annotate                    # per-line .py, showing which lines ran
```

# When to stop tuning

Aim for a **meaningful threshold** (e.g., 80–95%), enforce it with `fail_under`, and focus reviews on **diff coverage** (are the new/changed lines tested?). Don’t chase 100% on code that’s hard to exercise (feature flags, defensive guards)—use pragmas sparingly and prefer simpler, testable design.

If you want, I can generate a minimal example repo layout with a ready-to-run `.coveragerc`, pytest config, and a failing threshold gate to drop into your projects.
