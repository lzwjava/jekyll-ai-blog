---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: GKE 扩缩容中的 HPA 与 VPA
translated: true
type: note
---

在 Google Cloud（特别是 Google Kubernetes Engine/GKE）中，Vertical Pod Autoscaler (VPA) 和 Horizontal Pod Autoscaler (HPA) 都是自动扩缩 Kubernetes workload 的机制，但它们的工作方式根本不同。

**Horizontal Pod Autoscaler (HPA)** 通过调整 Pod replica 的**数量**来进行扩缩。当您的应用需要更多资源时，HPA 会创建额外的 Pod 副本以分担负载。例如，如果 CPU 使用率飙升，HPA 可能会从 3 个 Pod 扩容到 10 个 Pod。它非常适合可以并行处理请求的 stateless 应用。HPA 通常监控 CPU utilization、memory usage 或 custom metrics 等指标，并根据您定义的阈值进行 scale out（增加 Pod）或 scale in（减少 Pod）。

**Vertical Pod Autoscaler (VPA)** 通过调整单个 Pod 的 **resource requests 和 limits** 来进行扩缩。VPA 不是增加更多 Pod，而是修改每个 Pod 可以使用的 CPU 和 memory 数量。如果一个 Pod 持续消耗比 request 更多的资源，VPA 可以增加其资源分配，并使用新设置重启该 Pod。这在您最初不确定如何设置 resource requests，或者应用随时间变化的资源需求无法从 horizontal scaling 中获益时非常有用。

核心区别：HPA 增加应用的实例数量，而 VPA 让每个实例变得更大或更小。您实际上可以同时使用两者，但需要仔细配置以避免冲突（通常 HPA 针对 CPU，VPA 针对 memory）。在 GKE 中，这些作为内置功能提供，并与 Kubernetes autoscaling 生态系统集成。
