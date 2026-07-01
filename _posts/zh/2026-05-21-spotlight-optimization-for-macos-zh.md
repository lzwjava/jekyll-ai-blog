---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 聚焦优化
translated: true
type: note
---

已完成。以下是发生的情况以及您可以预期的事项：

---

**已完成的操作**

| 操作 | 效果 |
| --- | --- |
| `touch ~/Projects/.metadata_never_index` | Spotlight 将不再爬取 `~/Projects/` — 即您的 `node_modules`、开发仓库等内容 |
| `touch ~/Library/Caches/.metadata_never_index` | 不会索引缓存文件 |
| `touch ~/Downloads/.metadata_never_index` | 不会索引“下载”文件夹 |
| `touch ~/Library/Application\ Support/.metadata_never_index` | 不会索引应用数据 |
| `sudo mdutil -E /` | 清除现有索引 — 强制重新构建 |
| `pkill -9 mdworker mds` | 立即终止 CPU 占用高峰 |

**您将看到的效果**

- mdworker 导致的约 250% CPU 峰值将在约 30 秒内消失
- Spotlight 将重新构建索引，但**仅针对**系统文件、应用程序、您的“文稿”、“桌面”等 — 跳过之前爬取的 50GB+ 垃圾内容
- 重建将在 1-2 分钟内完成，而不是 15 分钟以上
- 从今天起，**每次重启**后 Spotlight 几乎瞬间完成重建，不再有 15 分钟的 CPU 高负载

**仍然正常工作的功能**

- `Cmd+Space` 搜索仍然可用
- 您仍然可以搜索应用程序、系统设置、文稿等
- `~/Projects/`、`~/Downloads/`、`~/Library/Caches/`、`~/Library/Application Support/` 内的内容将不会出现在搜索结果中 — 这很可能是您希望的效果

**如需撤销**（如果您希望恢复这些文件夹的搜索功能）：

```
rm ~/Projects/.metadata_never_index ~/Library/Caches/.metadata_never_index ~/Downloads/.metadata_never_index ~/Library/Application\ Support/.metadata_never_index
sudo mdutil -E /
```
