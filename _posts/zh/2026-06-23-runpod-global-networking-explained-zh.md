---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod全球网络详解
translated: true
type: note
---

**问题：** RunPod 的“GPU 位置 / 启用全球网络”部分是什么意思——具体来说，内部主机名、私有 IP 地址和开关分别代表什么？

**回答：**

这是 RunPod 的 Pod 网络配置。以下是每个字段的含义：

**GPU 位置** —— Pod 运行的物理数据中心区域（例如 US-TX、EU-RO）。与延迟和数据驻留相关。

---

**启用全球网络** —— 一个开关，启用后将为您的 Pod 提供：

### 内部主机名
RunPod 私有网络内的稳定 DNS 名称，例如：
```
<pod-id>-<port>.proxy.runpod.net
```
这允许其他 Pod（或 RunPod 的基础设施）通过名称而非动态分配的 IP 地址访问您的 Pod。适用于多 Pod 配置——例如，推理 Pod 调用预处理 Pod。

### 私有 IP 地址
RunPod 内部 VXLAN/覆盖网络内分配的稳定 RFC-1918 IP（如 `10.x.x.x`）。仅在 RunPod 网络内可访问——无法通过公共互联网访问。

---

**为什么这对您的使用场景很重要：**

| 场景 | 是否使用全球网络？ |
|---|---|
| 单个 Pod，通过 SSH 登录，运行训练 | 否——不需要 |
| 多 Pod 分布式训练（NCCL） | 是——Pod 之间需要互相发现 |
| 推理 Pod + 独立 API 网关 Pod | 是 |
| vLLM 服务器被代理 Pod 调用 | 是 |

如果您正在运行单个 MI300X Pod 进行训练（例如您的 nanoGPT 运行），则不需要此功能。如果您正在构建多节点设置或代理基础设施，其中 Pod 之间需要通信，请启用它，并使用内部主机名进行服务发现，而不是硬编码 IP 地址。

未启用全球网络时，私有 IP 是临时的——Pod 重启后可能会更改。启用后，主机名在重启后保持稳定。