---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全部已提交并推送
translated: true
type: note
---

全部 committed 并 pushed。总结：

**Committed**（已有4个 commits，包括新提交）：
- `feat(home): show notes as front page instead of posts` (`f5e6401b3`)
- 加上之前领先远程的3个 commits

**Pushed**：`origin`（GitHub） — `main` 完全是最新的（`origin/main` = `HEAD` = `f5e6401b3`），working tree clean。最初的 60 秒超时推送实际上已经成功；后续的重试遇到了暂时的 SSH/密钥问题，最后的 `git push` 确认所有内容都已推送至远程。

注意：还配置了 `gitea`（192.168.1.36）和 `gitlab` 远程仓库 — 我只推送到了 `origin`（GitHub）。要我也推送那些吗？