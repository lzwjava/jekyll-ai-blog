---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why Pip Install Works Without PyPI
translated: false
type: note
---

There are a few reasons why `pip install mini-copilot` might work locally even without publishing to PyPI:

1. **Already published to PyPI** — Someone (possibly you) may have already published it. You can check at `https://pypi.org/project/mini-copilot/`.

2. **Installed in editable mode** — If you ran `pip install -e .` inside the project directory, pip installs it directly from your local source. Running `pip install mini-copilot` afterward would just find it already installed and report success.

3. **Local package index or cache** — pip has a local cache (`~/.cache/pip`). If you previously installed it from a local wheel or source, the cached version might be reused.

4. **Different package with same name** — There might be an unrelated `mini-copilot` package on PyPI that happens to share the name.

To diagnose, run:

```bash
pip show mini-copilot
```

This will show the **Location** and **Home-page** fields, telling you exactly where pip got it from. If the location points to your local project directory, it was installed with `-e .`.
