---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod存储层级详解
translated: true
type: note
---

**问题：** RunPod 中的 Container disk、Volume disk 和 Network volume 分别指什么？

**回答：**

这些是 RunPod 的三种存储层级，区别在于生命周期（数据何时被清除）和可共享性：

**Container disk**（容器磁盘）—— Pod 的临时根文件系统（`/workspace` 之外的所有内容：`/root`、`/tmp`、已安装的 apt/pip 包等）。每次**停止**Pod 时都会被清除（不仅仅是终止）。可将其视为 Docker 容器的可写层。任何通过 `pip install` 或下载到此处的数据都会在停止后消失。

**Volume disk**（卷磁盘）—— 挂载在 `/workspace` 的持久化存储，与特定 Pod 绑定。可跨**停止/启动**周期存活（因此停止 Pod 以节省 GPU 成本时，`/workspace` 中的检查点和数据集仍会保留），但**终止**时会被删除。仅该 Pod 可使用。注意：Pod 停止时费用更高（$0.20/GB/月），运行时为 $0.10/GB/月——RunPod 对在未付费计算资源的 GPU 主机上保留存储收取额外费用。

**Network volume**（网络卷）—— 挂载在 `/workspace` 的持久化存储，但与任何 Pod 无关。可跨终止存活，并能附加到多个 Pod 或无服务器端点。价格更低（$0.07/GB/月，超过 1TB 为 $0.05/GB/月）。代价是：网络附加存储（I/O 比本地 NVMe 卷磁盘慢，对于数据加载器绑定的训练等大量随机读取操作影响明显），并且会将你限制在网络卷所在的数据中心区域——只能在该区域启动 Pod。

**适用于训练工作流的实用模式：**

```bash
# Network volume 位于 /workspace：数据集、模型检查点、希望保留的虚拟环境
/workspace/
├── data/fineweb/          # 跨终止存活
├── checkpoints/gpt2-760m/ # 跨终止存活
└── venv/                  # 可在不同 Pod 间复用

# Container disk：仅作为临时存储——此处数据在停止时全部丢失
/tmp/  /root/
```

经验法则：如果你在会话之间终止 Pod，请使用 **Network volume**（最便宜、最灵活——类似于在 AMD Dev Cloud 上保留持久化磁盘同时终止实例）；如果对同一 Pod 进行停止/启动操作，请使用 **Volume disk**；将 **Container disk** 视为一次性临时存储。由于 Container disk 会重置，需要在启动脚本中重新运行环境设置（apt/pip 安装）——或者将其打包到自定义 Docker 镜像中。

一个注意事项：仅使用 Volume disk 终止 Pod 会删除数据且无法恢复。如果检查点很重要，请使用 Network volume，或在终止前通过 `rsync` 将数据移出。
