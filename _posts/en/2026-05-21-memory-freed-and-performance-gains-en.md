---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Freed and Performance Gains
translated: false
type: note
---

My bad — they're fully closed. The 76 MB is an Apple system process (`CodeSigningHelper`) that has "Code" in its name, not VSCode.

**Memory freed since we started**:

| What | Before | After | Saved |
| --- | --- | --- | --- |
| VSCode | 23 GB | 0 | **23 GB** |
| WeType | 1.6 GB | 0 | **1.6 GB** |
| Spotlight (mdworker storm) | 14 GB | 0.5 GB (idle) | **13.5 GB** |
| Old VSCode extension versions | 1 GB disk | 0 | **1 GB disk** |
| **Total virtual demand** | **~95 GB** | **~57 GB** | **~38 GB freed** |

Real physical RAM is still at ~15 GB used because macOS keeps compressed pages until something needs the space. But the machine should feel **significantly snappier** — no swap thrashing, no CPU pinned at 250% by Spotlight.
