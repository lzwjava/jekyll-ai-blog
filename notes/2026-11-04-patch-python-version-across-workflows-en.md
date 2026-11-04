---
audio: false
generated: true
image: false
lang: en
layout: post
title: Patch Python version across workflows
translated: false
type: note
---

Done. Applied the same fix to the 7 other workflows that pinned `"3.13.2"`:

| Workflow | Change |
| --- | --- |
| `gh-pages.yml` | `3.13.2` → `3.13` + curl-based failure notify |
| `test.yml` | `3.13.2` → `3.13` |
| `punch.yml` | `3.13.2` → `3.13` |
| `reminders.yml` | `3.13.2` → `3.13` |
| `notes.yml` | `3.13.2` → `3.13` |
| `news.yml` | `3.13.2` → `3.13` |
| `notes-translation.yml` | `3.13.2` → `3.13` |
| `nytimes.yml` | `3.13.2` → `3.13` |

All 13 workflow YAML files parse cleanly. Nothing is committed yet — want me to commit and push (e.g., `fix(ci): use patch-less python version for ubuntu-latest`)?
