---
audio: false
generated: true
image: false
lang: en
layout: post
title: Aborting the VRAM Test
translated: false
type: note
---

I read the manual (显存测试软件使用手册). Here's what it says and the practical answer:

## What the manual says

- **`./mats -e 10`** — the `-e 10` means it tests **10MB of VRAM** (显存). This is a small amount, so the test normally **finishes on its own quickly**, ending with a **PASS or FAIL** screen. You don't usually need to force-quit it.
- The only explicit "exit" instruction in the manual (step 9) is for the **report viewer** (`nano report.txt` / `less report.txt`): press **`Ctrl+X`** or **`Ctrl+Z`** to return to the test command screen.

## If you want to abort `mats` while it's actually running

The manual doesn't cover interrupting a running test, but since this runs in a Linux environment:

| Key | Effect |
| --- | --- |
| **`Ctrl + C`** | **Kills the test immediately** — this is what you want to stop/exit a running `mats` process |
| `Ctrl + Z` | Only *suspends* (pauses) the process in the background — it doesn't exit. To actually kill it afterward, type `kill %1` |
| `Ctrl + D` | In some console tools, signals end-of-input (not reliable for mats) |

**So: press `Ctrl + C` to exit/abort `./mats -e 10` while it's running.**

After aborting, you'll be back at the shell prompt, where you can:

- `cd ..` — go back to `/home`
- `reboot` — restart, or `poweroff` — shut down
- Re-run the test or try a different version directory

⚠️ One caveat: aborting mid-test means `report.txt` may be incomplete or not written, so you won't get a reliable PASS/FAIL result for that run. If the test is progressing normally, it's best to just let the 10MB test finish — it typically takes only a short time.
