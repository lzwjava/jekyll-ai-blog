---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Containerd空间回收状态
translated: true
type: note
---

Containerd rsync 被终止，部分数据已清理。模型迁移已完成并正常运行。状态如下：

```
根磁盘：697G  已用 88G（剩余 610G）— 原为 124G，释放了 36G
卷：      100G  已用 37G（剩余 58G）
```

已生效的操作：
- ✓ llama.cpp/models (37G) → 迁移至卷，并创建回链

未生效的操作：
- ✗ containerd (59G) — overlayfs 快照（ROCm 容器层）中存在 39000 多个小文件。rsync 耗时过长。

**containerd 处理选项：**
1. `systemctl stop containerd && mv /var/lib/containerd /mnt/volume_.../containerd && ln -s /mnt/volume_.../containerd /var/lib/containerd && systemctl start containerd` — 在相同文件系统上 mv 是瞬间完成的……但由于这里是不同文件系统，实际仍会复制。
2. **改用清理未使用的容器镜像** — 执行 `crictl rmi --prune` 可释放大量空间，无需移动任何文件。
3. 修改 `/etc/containerd/config.toml` 中 containerd 的 `root` 路径，使其指向卷（需重启，可能导致运行中的容器中断）。

是否先尝试清理容器镜像？这是释放根磁盘空间最安全的方式，不会影响 containerd 配置。