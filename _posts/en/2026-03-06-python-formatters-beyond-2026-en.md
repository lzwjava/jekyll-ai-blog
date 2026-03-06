---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Formatters Beyond Black 2026
translated: false
type: note
---

**Question:** Besides Black, what other Python formatters are there?

**Answer:**

Here are the most popular and actively maintained Python code formatters besides **Black** (as of 2025–2026):

- **ruff format**  
  Extremely fast (written in Rust), very popular in 2024–2026, 90–95% Black-compatible by default, becoming the new de facto standard in many projects.

- **isort**  
  Only sorts imports (not a full formatter), but still widely used together with Black or others.

- **autopep8**  
  Automatically formats code to conform (mostly) to PEP 8. Conservative, configurable, but slower and less opinionated than Black/ruff.

- **yapf**  
  Google’s formatter. Highly configurable — you can make it behave very close to Black, PEP 8, or completely custom style.

- **blue**  
  Almost identical to Black, but with 79-character line length (instead of 88) to match older projects / flake8 defaults.

- **blacken-docs**  
  Formats code blocks inside documentation (Markdown, RST, etc.) using Black.

- **docformatter**  
  Formats docstrings (mostly PEP 257 / Google / NumPy style).

- **pyink**  
  Meta’s fork of Black with a few extra defaults/tweaks (used internally at Meta).

- **darker**  
  Only formats the changed lines (useful in pre-commit + CI to avoid big reformatting commits).

**Quick comparison (2025–2026 popularity & philosophy):**

| Formatter      | Speed       | Opinionated? | Black-compatible? | Main use-case today                     | Actively maintained |
|----------------|-------------|--------------|---------------------|------------------------------------------|----------------------|
| ruff format    | ★★★★★       | Yes          | ~95%                | Replacing Black in new projects          | Very active         |
| Black          | ★★★★        | Very         | —                   | Still very common baseline               | Active              |
| yapf           | ★★          | No           | Configurable        | Teams that want full control             | Active              |
| autopep8       | ★★          | No           | No                  | Legacy / conservative projects           | Active              |
| blue           | ★★★★        | Very         | Almost              | Projects stuck on 79-char lines          | Low activity        |

**Most common choices in 2026:**

1. **ruff format** (often just called **ruff**) — fastest growing
2. **Black** — still very widely used
3. **Black + isort** (or **ruff format + ruff check --select I**)
4. **yapf** — mostly in companies with custom style guides

**Bottom line in 2026:**  
If you're starting a new project → **ruff format** is currently the strongest default choice for most teams.

**References:**

- [https://github.com/astral-sh/ruff](https://github.com/astral-sh/ruff)
- [https://black.readthedocs.io/](https://black.readthedocs.io/)
- [https://github.com/google/yapf](https://github.com/google/yapf)
- [https://pypi.org/project/autopep8/](https://pypi.org/project/autopep8/)