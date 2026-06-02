---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Spotlight索引已禁用，性能提升
translated: true
type: note
---

Spotlight 已**永久禁用**。以下是具体情况：

| 之前 | 之后 |
|---|---|
| mds_stores：**14 GB RAM** | mds 守护进程：**471 MB**（空闲，CPU 0%） |
| mdworker：**18 个进程**占用 CPU | **0** |
| 持续索引所有文件夹 | **所有卷均已禁用** |
| 重启后：15 分钟的 CPU 地狱 | 重启后：无任何操作 |

**更改内容**：
- `sudo mdutil -a -i off` — 在 `/`、`/System/Volumes/Data`、`/System/Volumes/Preboot` 上关闭索引
- mds 守护进程仍然存在（Apple 限制无法完全关闭），但**处于空闲状态，占用 471 MB 内存且 CPU 0%**，而非之前的 14 GB + 90% CPU
- `Cmd+Space` 仍可从现有索引启动应用，但不会搜索文件内容或为新文件建立索引

**如需重新启用**（如果您将来想恢复）：

```
sudo mdutil -a -i on
```
