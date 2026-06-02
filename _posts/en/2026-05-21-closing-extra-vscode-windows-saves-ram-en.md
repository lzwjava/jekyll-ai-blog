---
audio: false
generated: true
image: false
lang: en
layout: post
title: Closing Extra VSCode Windows Saves RAM
translated: false
type: note
---

You have **12 VSCode windows** open, each with 5-8 helper processes. That's the main reason VSCode uses ~23 GB.

| # open | Helper processes | RAM |
|---|---|---|
| 12 windows | 25 total | ~23 GB |

Keeping only the 1-2 projects you're actively working on would cut this to **~3-4 GB**.

---

**Extensions to consider removing** from this laptop (since your remote machine handles the heavy work):

| Extension | Disk | Remove? |
|---|---|---|
| `tomoki1207.pdf` — PDF viewer in VSCode | small | ✓ Yes — just open PDFs in browser |
| `yzane.markdown-pdf` — PDF export | small | ✓ Yes |
| `xdebug.php-pack` — PHP debugging | small | ✓ Yes — unless you do PHP work |
| `torn4dom4n.latex-support` — LaTeX | small | ✓ Yes |
| `moozzyk.arduino` — Arduino IDE | small | ✓ Yes |
| `mcu-debug.*` (3 extensions) — MCU debugger | 5 MB | ✓ Yes |
| `redhat.fabric8-analytics` — dead project | small | ✓ Yes |
| `azemoh.one-monokai` — duplicate theme | small | ✓ Remove 1 of 2 |

**Total freed**: ~50 MB disk + 0-3 plugin helper processes.

Want me to clean those up too? The biggest win is still closing the 10 extra VSCode windows.
