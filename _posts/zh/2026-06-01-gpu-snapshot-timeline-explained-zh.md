---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU快照时间线详解
translated: true
type: note
---

以下是根据法证证据整理的时间线：

**2026年3月16日** — AMD 构建了快照镜像：

- 使用 buildkit 构建的 `rocm:latest` Docker 镜像（26GB 的 `setup.sh` 为 ROCm 安装层）
- 已清除 `droplet-agent`（标准镜像构建清理步骤）

**2026年5月20日 04:39** — 你的 Droplet 基于该快照创建：

- Cloud-init 运行，重新安装了 `droplet-agent`
- 宿主机已在 `/opt/rocm-7.2.0/` 位置拥有 ROCm 7.2.0（22GB，已预置在镜像中）

**2026年5月20日 04:40** — 容器 `rocm` 启动：

- 运行了带 ROCm GPU 访问权限的 Jupyter Lab
- 大约在5月21日退出（11天前）

**回答你的问题：** 当你创建 GPU Droplet 时，你选择了类似 `Ubuntu 7.2-gpu-mi300x1-192gb-devcloud-atl1` 的镜像。该镜像**同时包含**：

- 宿主机上安装的 ROCm 7.2.0（`/opt/rocm-7.2.0/`）—— 22GB
- 预加载的 `rocm:latest` Docker 镜像（内部另有 36GB 的 ROCm）—— 并已预配置 Jupyter Lab

你并未手动安装任何东西。AMD Dev Cloud 已将所有内容集成到快照中。Docker 镜像只是宿主机上已有内容的容器化副本——旨在方便运行 Jupyter Lab。

**关键结论：** containerd 中的 59GB 完全来自 AMD Dev Cloud 预加载的快照。`rocm` 容器已于 11 天前退出，你并未使用它。宿主机上的 ROCm（位于 `/opt/rocm-7.2.0/`，22GB）才是实际驱动 GPU 工作负载的组件——Docker 镜像是冗余的。删除 Docker 工件是安全的。需要我清理它们吗？
