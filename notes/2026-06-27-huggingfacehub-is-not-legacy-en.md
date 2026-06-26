---
audio: false
generated: true
image: false
lang: en
layout: post
title: huggingface_hub is not legacy
translated: false
type: note
---

Question: Is `huggingface_hub` legacy now? Is `hf` the latest CLI? (I have `hf --version` → 1.12.0)

Answer:

Not legacy — you're conflating two things. `huggingface_hub` is the **Python package**, and it's very much current. `hf` is just the **new name for its CLI entry point**, which ships *inside* that same package.

What actually changed:

- The old command was `huggingface-cli`. It was renamed to `hf` (cleaner verb-noun syntax) and the old name was deprecated.
- `hf --version 1.12.0` is the version of the `huggingface_hub` package itself — they share versioning because the CLI is part of the library.

So:

```bash
pip show huggingface_hub   # this is what hf --version reports
hf --help                  # new CLI (huggingface-cli still works but warns)
```

The new syntax is `hf <resource> <action>`:

```bash
hf auth login              # was: huggingface-cli login
hf download <repo>         # was: huggingface-cli download <repo>
hf upload <repo> <path>    # was: huggingface-cli upload
hf auth whoami
hf repo create <name>
```

In Python nothing changed — you still import the same thing:

```python
from huggingface_hub import HfApi, snapshot_download, hf_hub_download
```

Worth verifying the exact rename timeline and which version flipped the default, since CLIs like this move fast and I shouldn't guess from memory:Confirmed by the sources — and your `1.12.0` tells the whole story:

- The `hf` CLI was renamed from `huggingface-cli` as a quality-of-life improvement, introduced in v0.34, following the `hf <resource> <action>` grammar.
- In huggingface_hub v1.0, the deprecated `huggingface-cli` was fully removed and the redesigned `hf` CLI (now Typer-based) replaced it. Other v1.0 breaking changes worth knowing if you're scripting against it: migration to httpx as the HTTP backend, and hf_xet became the default file-transfer package, replacing hf_transfer which was removed.
- One compatibility gotcha for your training stack: transformers v4 explicitly requires huggingface_hub v0.x, while transformers v5 requires v1.x. Since you're on `1.12.0`, you need transformers v5 — if something pins old transformers, you'll get a resolver conflict.

So: `huggingface_hub` = the library (current, you're on 1.12.0). `hf` = its CLI (current). `huggingface-cli` = the dead name. You're fully up to date.

Quick reference for the commands you'll actually hit on the sec-edgar GPT work:

```bash
hf auth login
hf download <org>/<model>           # pulls weights/tokenizer
hf upload <org>/<repo> ./out        # single-commit
hf upload-large-folder <repo> ./ckpt  # resumable, for big checkpoints
hf cache ls --filter "size>1GB"     # new v1.0 docker-style cache mgmt
hf jobs run --flavor a10g-small ...  # run scripts on HF hardware
```

One env var worth setting on your MI300X box to kill the startup auto-update check in non-interactive runs: `export HF_HUB_DISABLE_UPDATE_CHECK=1`.

References:

- [Say hello to `hf`: a faster, friendlier Hugging Face CLI](https://huggingface.co/blog/hf-cli)
- [huggingface_hub v1.0 release blog](https://huggingface.co/blog/huggingface-hub-v1)
- [Migrating to huggingface_hub v1.0](https://huggingface.co/docs/huggingface_hub/en/concepts/migration)
