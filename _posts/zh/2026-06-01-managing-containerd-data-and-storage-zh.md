---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 管理containerd数据和存储
translated: true
type: note
---

**问题：** 什么是 containerd 数据？我们真的需要将其从根磁盘迁移到卷吗？

**答案：**

## containerd 数据是什么？

`/var/lib/containerd/` 存储容器运行时管理的所有内容：

- **快照（Snapshots）** — 容器镜像的层叠文件系统快照（占用了 59G 的大部分空间）
- **内容存储（Content store）** — 从仓库下载的原始 OCI 数据块（镜像层、清单、配置）
- **元数据（Metadata）** — 跟踪镜像/容器状态的 BoltDB 数据库
- **运行时状态（Runtime state）** — 运行中容器的状态、shim 进程

在你这样的 AMD Dev Cloud 节点的 GPU 开发机上，这几乎全部是 **Docker/容器镜像层**——比如 PyTorch 镜像、ROCm 镜像、Ollama 容器等。这些镜像可能非常庞大（仅 ROCm PyTorch 单个镜像通常就有 20–30G）。

## 你需要迁移它吗？

**大概率不需要，或者至少不紧急。** 理由如下：

| 因素 | 评估 |
|--------|-----------|
| 可重现？ | 是 — 镜像可以从仓库重新拉取 |
| 迁移风险 | 高 — containerd 使用硬链接和 overlay 挂载；`rsync` 可能会破坏它们 |
| 收益 | 释放根磁盘上的 59G 空间 |
| 替代方案 | 直接运行 `docker system prune` 或 `crictl rmi` 删除未使用的镜像 |

## 更安全的替代方案 — 直接清理

```bash
# 查看实际内容
du -sh /var/lib/containerd/io.containerd.snapshotter.v1.overlayfs/snapshots/*

# 如果你在 containerd 之上使用 Docker：
docker system df
docker system prune -af --volumes  # 清除未使用的镜像、容器、卷

# 如果你直接使用 containerd（nerdctl/crictl）：
nerdctl system prune -af
```

这很可能在不进行符号链接操作或冒着破坏运行时的风险的情况下，恢复大部分 59G 空间。

## 如果你确实要正确迁移

`rsync` 不是正确的工具——containerd 在其快照存储中使用了 **硬链接**，而 rsync 会破坏它们。正确的方法：

```bash
systemctl stop containerd
cp -a --reflink=auto /var/lib/containerd /mnt/volume/containerd-data
# 不要使用 rsync —— cp -a 能更好地保留硬链接，或者使用 tar 管道：
# tar -C /var/lib/containerd -cf - . | tar -C /mnt/volume/containerd-data -xf -

# 然后使用绑定挂载，而不是符号链接：
mount --bind /mnt/volume/containerd-data /var/lib/containerd
echo '/mnt/volume/containerd-data /var/lib/containerd none bind 0 0' >> /etc/fstab
systemctl start containerd
```

## 我的建议

**停止迁移。先清理：**

```bash
# 快速检查
ssh root@<your-node> "du -sh /var/lib/containerd/*/snapshots 2>/dev/null; docker system df 2>/dev/null || nerdctl system df 2>/dev/null"
```

如果你同时使用 Ollama/llama.cpp 拉取 GGUF 模型和 Docker 拉取 GPU 镜像，那么很可能积压了大量不再需要的陈旧层。清理操作更安全、更快速，且零风险，而迁移一个正在运行的运行时数据目录则风险较高。
