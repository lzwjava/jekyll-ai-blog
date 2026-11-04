---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 两个远程推送被GitLab拒绝
translated: true
type: note
---

两个远端仓库已成功推送：

| 远端 | 推送状态 |
| -------- | ------------- |
| **origin (GitHub)** | ✅ `f5e6401b..852a5564` 已推送 |
| **gitea** | ✅ `65f99c8d..852a5564` 已推送 |
| **gitlab** | ❌ 拒绝 (non-fast-forward) |

**GitLab 失败的原因：** GitLab 的 `main` 分支处于提交 `735c8c4 "Initial commit"`，该提交与你的本地历史*无关*——这是一个完全独立的仓库树（本地与远端相差约 48k 个文件 / 4.3M 行删除）。这不是正常的快进式合并；同步需要一个**强制推送**，覆盖 GitLab 现有的 `main` 及其 "Initial commit" 历史。

我没有**强制推送**，因为那会破坏 GitLab 当前的历史。你希望如何处理 GitLab？

- **强制推送** — `git push --force gitlab main`（覆盖 GitLab 无关的 `main` 分支），或
- **跳过 GitLab** — 保持原样（GitHub 和 gitea 已同步）。

你只需执行即可。
