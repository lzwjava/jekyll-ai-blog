---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘空间严重不足 - 剩余15GB
translated: true
type: note
---

是的——磁盘仍然严重不足。以下是完整情况：

## 当前状态

| | |
|---|---|
| 文件系统 `/dev/nvme0n1p2` | **总计 916G，已用 854G，可用 15G (99%)** |
| Inodes | 已用 10% — 正常（不是问题） |

您遇到的 ENOSPC 错误是真实的：916G 中仅剩 15G 可用。

## 主要空间占用者

**`/home/lzw/projects` — 488G**
- `jekyll-ai-blog/fineweb_test_dump` — **88G**（数据集转储）
- `llama.cpp/models` — **72G**（LLM 权重）
- `imagenet` — **64G**（数据集）
- `backup.lzwjava.github.io/.git` — **57G**（Git 对象）
- `coco` — **38G**，`llama` — **31G**，`llama2.c` — **26G**，`open_llama_3b` — **13G**

**`/home/lzw/.cache` — 57G**
- `nanochat/base_checkpoints` — 27G + `chatsft_checkpoints` — 3.8G
- `uv` — 7.8G，`JetBrains` — 6.2G，`whisper` — 4.3G

**其他**
- `/home/lzw/.local/lib` — 38G，`Downloads` — 19G，`qDownloads` — 14G
- `/var` — 21G（`cuda-repo` 3.1G，`log` 2.7G，`crash` 609M）
- `/tmp/pip-unpack-fogsmaol` — 628M（孤立的 pip 临时目录）

## 现在可以安全清理的内容（约 9G，无风险）

- `uv` 缓存：`uv cache clean` → 约 7.8G
- `/var/crash` → 609M
- `/tmp/pip-unpack-*` 残留文件 → 约 630M
- `pip` 缓存 + apt 缓存

## 更大的清理收益（需要您确认）

- `fineweb_test_dump`（88G）、`backup.../.git`（57G）、`llama.cpp/models`（72G）——这些才是真正的解决之道；如果其中任何一个可以重新生成或重新下载，删除后可释放 50–90G 空间。

是否需要我现在运行安全清理？如果是，哪些大目录（数据集、模型、git 备份）可以安全删除？