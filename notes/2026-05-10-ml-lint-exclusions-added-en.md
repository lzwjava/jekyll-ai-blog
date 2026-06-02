---
audio: false
generated: true
image: false
lang: en
layout: post
title: ML Lint Exclusions Added Summary
translated: false
type: note
---

The ml exclusions work — pre-commit passes on all ml files. There are 7 pre-existing pyright failures in unrelated modules (speech_to_text, audio, java_agent, try_tiktoken) for missing optional deps (google-cloud-speech, pydub, jpype, tiktoken) — these predate this change and aren't in scope.

Diff summary:

```toml
[tool.pyright]
exclude = [
    ".venv/",
    "ww/ml/",     # added
]

[tool.ruff]                      # new section
extend-exclude = ["ww/ml"]
```

`ww/ml/` is third-party learning/reference code (Coursera, PyTorch examples, Karpathy projects) — its deps (torch, sklearn, scipy, pydub, plotly, dash) aren't project dependencies, so excluding it from both linters is the right call.
