---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transition to pyproject.toml Only
translated: false
type: note
---

Yes, exactly right. Since you have `pyproject.toml`, `requirements.txt` is redundant. Here's the plan:

1. **Add `piexif` to `pyproject.toml`** under `[project].dependencies`
2. **Delete `requirements.txt`**
3. **Install with `pip install .`** (or `pip install -e .` for editable/dev mode)

`pip install -e .` is better for active development — changes to your source are reflected immediately without reinstalling.

If you have dev-only deps (like `pyright`), add them under:

```toml
[project.optional-dependencies]
dev = ["pyright"]
```

Then install with `pip install -e ".[dev]"`.

So yes — remove `requirements.txt`, add `piexif` to `pyproject.toml`, and use `pip install -e .` going forward.