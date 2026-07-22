---
audio: false
generated: true
image: false
lang: en
layout: post
title: Removing dead binaries with bad shebangs
translated: false
type: note
---

Removed. `pi` is gone — both the binary and the package files.

**Root cause recap:**
- `pi` was a Python 2 package (2013, abandoned) installed via pip under a Python 3.13 environment that no longer exists on this machine
- The shebang `#!/usr/bin/python3.13` → "required file not found"
- The package itself is fundamentally incompatible with Python 3 (uses `print` statement syntax, deprecated `imp` module)

If you ever need to audit other dead binaries in `~/.local/bin/`:

```
file ~/.local/bin/* | grep -E "Python script" | while read f _; do
  head -1 "$f" | grep -q "$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d. -f1-2)" || echo "BAD SHEBANG: $f"
done
```