---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 幂等Git拉取更新
translated: true
type: note
---

是的，完全正确。每个仓库都是独立的 `git pull` 操作——没有共享状态或事务。如果你在第 30 个仓库处取消（共 60 个）：

- 仓库 1-30：已拉取完成
- 仓库 31-60：未被触及，仍处于旧状态

重新运行 `ww projects update` 只是再次拉取全部 60 个仓库——已更新的仓库会在约 1 秒内显示“已是最新”，其余 30 个仓库则会进行实际更新。`git pull` 是幂等的，因此重新运行始终安全。

无需检查点或恢复逻辑——这正是其精妙之处。