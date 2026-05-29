---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving Homebrew and pip Binary Conflicts
translated: false
type: note
---

There it is. You have `huggingface-hub` 0.29.3 installed via pip, which already owns `/opt/homebrew/bin/hf` and `/opt/homebrew/bin/tiny-agents`. The Homebrew `hf` formula provides the same binaries.

Two options:

**Option 1 — Clean fix:** Remove the pip package, then link:
```sh
pip uninstall huggingface-hub
brew link hf
```

**Option 2 — Force overwrite:** Just overwrite the pip scripts with Homebrew's:
```sh
brew link --overwrite hf
```

Option 2 works but leaves the pip package installed — you'd have two copies of `huggingface-hub` (one via pip, one via brew) which is a maintenance headache. Option 1 is cleaner.

Want me to also check if the `hf` formula should declare a conflict with the pip package in its formula file?