---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 跨工作流修补 Python 版本
translated: true
type: note
---

已完成。已将相同的修复应用于其他7个固定了 `"3.13.2"` 的工作流程：

| 工作流程 | 更改 |
|---|---|
| `gh-pages.yml` | `3.13.2` → `3.13` + curl-based failure notify |
| `test.yml` | `3.13.2` → `3.13` |
| `punch.yml` | `3.13.2` → `3.13` |
| `reminders.yml` | `3.13.2` → `3.13` |
| `notes.yml` | `3.13.2` → `3.13` |
| `news.yml` | `3.13.2` → `3.13` |
| `notes-translation.yml` | `3.13.2` → `3.13` |
| `nytimes.yml` | `3.13.2` → `3.13` |

所有13个工作流程YAML文件均解析无误。尚未提交任何内容——需要我提交并推送吗（例如：`fix(ci): use patch-less python version for ubuntu-latest`）？