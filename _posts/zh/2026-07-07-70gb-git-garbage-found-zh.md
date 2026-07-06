---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 发现70GB Git垃圾
translated: true
type: note
---

找到了。以下是您460GB磁盘的详细情况：

| 项目 | 大小 | 数据占比 |
|------|------|-----------|
| **projects/lzwjava.github.io git** | **~70 GB** | **17%** |
| WeChat | 21 GB | 5% |
| Docker | 8 GB | 2% |
| Claude (Hermes/agents) | 10 GB | 2% |
| JetBrains | 6.5 GB | 2% |
| 其他项目（70个仓库） | ~40 GB | 10% |
| 缓存 | ~10 GB | 2% |
| 应用程序 | 38 GB | 9% |
| App Support 杂项 | ~25 GB | 6% |
| 其他（系统、dotfiles、QQ 等） | ~190 GB | 45% |
| **可用** | **5.9 GB** | **—** |

**两个重大发现：**

1. **lzwjava.github.io git 仓库 — 共70 GB，其中43 GB在pack文件中，另有27 GB属于垃圾pack文件。** 这是主要问题所在。`git count-objects` 显示有55个pack文件，总计43 GiB，外加 **~27 GiB 的孤立 tmp_pack_* 垃圾文件**——这些是中断的 repack/gc 操作留下的。工作目录（`_site/`、`README.md`）仅约302 MB；其余全是git历史记录和孤立的临时文件。

2. **`~27 GB 的垃圾 `tmp_pack_*` 文件** 位于 `.git/objects/pack/` 中。这些可以安全删除。

**操作计划：**

```
cd ~/projects/lzwjava.github.io
rm -f .git/objects/pack/tmp_*
git repack -a -d --depth=250 --window=250
git gc --prune=now --aggressive
```

这将： (a) 删除27 GB的孤立临时pack文件， (b) 将55个pack文件去重合并为一个， (c) 通过增量优化再回收约20+ GB。该仓库的pack中有3500万个对象——多年来一直在积累垃圾。

需要我运行这个清理操作吗？只需几分钟，但应该能释放约50 GB以上的空间。

另外值得关注：WeChat（容器中21 GB——存储图片/视频）、Docker（8 GB）和Claude（10 GB——很可能是对话历史）。