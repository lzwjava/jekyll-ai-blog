---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Overload Diagnosis and Fixes
translated: false
type: note
---

Here's the fresh picture. Some things have changed.

---

## Top Memory Offenders (right now)

| Rank | What | RAM | # Processes | Verdict |
| --- | --- | --- | --- | --- |
| **1** | **CGPDFService** (×8) | **~16 GB** | 8 | PDF files open somewhere → close them |
| **2** | **VSCode** | **~23 GB** | 25 | Close projects not in use |
| **3** | **WeChat** | **~20 GB** | 12 | Still running! |
| **4** | **mds_stores** (Spotlight) | **~14 GB** | 1 | Rebuilding index — temporary |
| **5** | **Browsers** (Safari + WebKit) | **~13.5 GB** | 27 | Too many tabs |
| 6 | Python | 2.8 GB | 2 | Depends on what's running |
| 7 | Microsoft (Teams/Office) | 1.7 GB | 4 | Quit if not using |
| 8 | GitHub Desktop | 1.5 GB | 1 | Quit if not using |
| 9 | Ghostty | 1.3 GB | 1 | Normal |

**Total demand**: ~95 GB on 16 GB physical. Your machine is a hero for surviving this.

---

## What to clean next (in order of impact)

**1. Kill WeChat** — still here despite the earlier suggestion

```
pkill -9 WeChat WeChatAppEx WeApp
```

This alone drops 20 GB of virtual demand. The mini-program engine is the heaviest thing on your system.

**2. Close the PDF files that spawned CGPDFService**

You have **8 CGPDFService processes** using ~16 GB. These are spawned when Safari, Preview, or Mail opens a PDF. Find which app has a PDF open and close the tab/window.

```
# Quick check what's using PDF
lsof -c CGPDFService 2>/dev/null | head -5
```

**3. Close VSCode projects**

25 processes × ~1 GB each. Only keep the one project you're actively editing. `Cmd+Q` the rest.

**4. Wait 2 more minutes for Spotlight**

mds_stores at 14 GB is still rebuilding the index after the erase. This will crash down to near 0 once it finishes.

---

Want me to kill WeChat and find which PDF is open? Those two steps free ~36 GB of memory pressure immediately.
