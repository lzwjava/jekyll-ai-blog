---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 全球网络解析
translated: true
type: note
---

**问题：** RunPod 上的“启用全局网络”（Enable Global Networking）是什么意思？内部主机名（internal hostname）和私有 IP 地址（private IP address）字段分别用于什么？

**回答：**

RunPod 的 **Global Networking** 功能可将你的 Pod 连接到一个**私有覆盖网络**（类似 VPN 网格），该网络跨越 RunPod 全球所有数据中心。如果不启用，你的 Pod 将处于隔离状态——只能通过其公共 HTTP/TCP 代理端口访问。

## 启用后获得的能力

启用全局网络后，你的 Pod 将获得：

- **内部主机名** — 一个稳定的 DNS 名称（例如 `<pod-id>-<port>.proxy.runpod.net` 或类似 `<hostname>.runpod.internal`），可从**同一 RunPod 网络上其他 Pod**（无论它们位于哪个数据中心）解析到你的 Pod。
- **私有 IP 地址** — 在覆盖网络中分配给 Pod 的静态私有 IP（通常在 `10.x.x.x` 范围内）。

## 为什么对你的使用场景很重要

| 使用场景 | 全局网络的作用 |
|---|---|
| 多节点训练（DDP/NCCL） | 节点通过稳定的主机名相互发现，而非依赖临时 IP |
| 多智能体系统 | 智能体 Pod 之间直接调用，无需经过公共互联网 |
| 推理与训练分离 | 独立的推理 Pod 通过内部低延迟调用训练 Pod |
| Ray / vLLM 集群 | Head 节点与 Worker 节点通过私有网络通信 |

## 底层工作原理

RunPod 使用 **WireGuard** 或类似的覆盖网络技术在 Pod 之间创建扁平的三层网络。你的 Pod 会获得一个带有私有 IP 的虚拟网卡。内部主机名的 DNS 解析在该覆盖网络内部进行路由——永远不会触及公共互联网。

## 实际影响

如果你在 RunPod 上运行多 GPU 或多节点作业（这与你的 MI300X 规模训练工作相关），启用此功能对于 Pod 之间 NCCL 的 `MASTER_ADDR` 可靠运行几乎是必需的。你需要设置：

```bash
export MASTER_ADDR=<内部主机名>
export MASTER_PORT=29500
```

如果不启用全局网络，你将不得不通过公共 TCP 代理端口穿透，这会增加延迟和复杂性。

**TL;DR：** 这是 RunPod 的私有 Pod 间网络。当 Pod 需要直接相互通信时（多节点训练、分布式推理、智能体网络），请启用它。
