---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 存储清理：释放95GB
translated: true
type: note
---

完成。总结如下：

```
根磁盘：    697G  已用 29G（可用 668G）—— 原为 124G，释放了 95G
卷：        100G  已用 37G（可用 58G）
Containerd：1.8M（原为 59G）
```

**在根磁盘上释放了 95 GB**：
- 37G → 将 llama.cpp 模型移至卷并创建了符号链接
- 36G → 删除了 rocm Docker 镜像
- 22G → 删除了 containerd overlayfs 快照（容器镜像层）