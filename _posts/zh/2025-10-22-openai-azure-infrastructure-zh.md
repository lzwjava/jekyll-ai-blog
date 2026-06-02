---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenAI基础设施与Azure依赖关系
translated: true
type: note
---

### OpenAI 技术栈概览

OpenAI 的基础设施针对大规模人工智能研究、训练和部署进行了深度优化，重点关注可扩展性、安全性和快速实验能力。自 2017 年初从 AWS 迁移后，其技术栈主要围绕微软 Azure 构建，Azure 为其超级计算机和工作负载提供了基础云平台。这一转变实现了与专用硬件的更好集成及成本优化。核心技术要素包括统一的 Python 单体代码库、用于编排的 Kubernetes，以及 Apache Kafka 等流处理工具。下面我将按类别进行解析，并特别说明对 Azure 的依赖及 Kubernetes 的具体实施。

#### 云基础设施：深度依赖 Azure

OpenAI 在研究环境和生产环境中广泛使用 Azure，包括训练 GPT 系列等前沿模型。具体包括：

- **Azure 作为核心平台**：所有主要工作负载均在 Azure 上运行，敏感数据（如模型权重）通过私有链接存储以最小化互联网暴露。身份认证集成 Azure Entra ID，支持基于风险的访问控制和异常检测。
- **为何深度绑定 Azure？**：一份泄露的内部文件（可能指向其 2024 年安全架构文章）强调了 Azure 在训练期间保护知识产权的作用。它支持大规模 GPU 集群，用于机器人、游戏等 AI 实验。OpenAI 与微软的合作关系通过 Azure OpenAI 服务保障模型低延迟访问，但在内部，Azure 是定制化超级计算的核心支柱。他们还通过混合本地数据中心处理 GPU 密集型任务，并在 Azure 中管理控制平面（如 etcd）以确保可靠性和备份。

这种深度集成意味着 OpenAI 的技术栈不易移植——它针对 Azure 生态系统的性能和合规性进行了专门优化。

#### 编排与扩展：基于 Azure 优化的 Kubernetes（AKS）

Kubernetes 是工作负载管理的核心，负责批处理调度、容器编排和跨集群可移植性。OpenAI 在 Azure Kubernetes Service（AKS）上运行实验，近年来节点规模已超过 7,500 个（2017 年时为 2,500 个）。

- **AKS 在 Azure 生态中的可靠性**：如您所述，当完全嵌入 Azure 产品时，Azure 的 Kubernetes 服务表现卓越。OpenAI 转向 Azure CNI（容器网络接口）进行网络配置，该接口专为 Azure 云构建——能够处理高性能、大规模环境，而像 Flannel 这样的通用 CNI 在此规模下难以稳定胜任。这使得动态扩展无瓶颈、自动 Pod 健康检查及故障期间切换成为可能。若缺乏 Azure 原生集成（如 blob 存储和工作负载身份），可靠性会因延迟、认证问题或容量限制而下降。他们的自定义自动扩缩器动态增减节点，在削减闲置资源成本的同时，实现数日内实验规模 10 倍扩展。
- **安全层**：Kubernetes 强制执行基于角色的访问控制（RBAC）以实现最小权限，通过准入控制器实施容器策略，并默认拒绝网络出口（仅允许白名单路径）。高风险任务额外使用 gVisor 加强隔离。多集群故障切换确保区域性问题期间任务持续运行。

#### 开发与代码管理：单体代码库策略

OpenAI 为大多数研究和工程工作维护统一的 Python 单体代码库。这集中了代码、库和依赖项，让团队能够使用熟悉的 Python 工具（如 NumPy、PyTorch）及 AI 专用流水线。它与流处理无缝集成，降低了实验的复杂性。CI/CD 流水线通过多方审批和基础设施即代码（IaC）进行严格管控，确保部署一致性。

#### 数据处理与流处理

- **Apache Kafka**：作为日志、训练数据和结果的事件总线。采用多主架构实现高可用性，配备自定义连接器（如用于读取的联合流、用于写入的 Prism Sink）和看门狗程序以适应故障切换等拓扑变化。
- **Kubernetes 上的 PyFlink**：用于 GenAI 流处理，通过 Flink Kubernetes Operator 实现自动化。支持 Python 的 DataStream/Table API，使用 RocksDB 管理状态，Azure blob 存储进行检查点备份——并通过工作负载身份保障安全（无需长期密钥）。

#### 监控与通信

- **Prometheus**：用于调试和指标收集。
- **gRPC**：用于服务间通信。

#### 2025 年演进趋势

近期更新（如 OpenAI DevDay 2025）更侧重于模型 API 和 AgentKit 等智能体工具，但基础设施栈仍以 Azure-Kubernetes 为核心。他们已开源自动扩缩器等工具以分享经验。

此技术栈优先考虑“数据飞轮”以实现快速迭代，但以牺牲可移植性换取 Azure 在超大规模下的可靠性。如果您正在构建类似系统，从 AKS + Kafka 入手可模拟其架构，但在 Azure 之外需预期调整。

[OpenAI 如何利用 Kubernetes 和 Apache Kafka 支持 GenAI](https://blog.bytebytego.com/p/how-openai-uses-kubernetes-and-apache)
[为先进 AI 保障研究基础设施安全](https://openai.com/index/securing-research-infrastructure-for-advanced-ai/)
[OpenAI Kubernetes 案例研究](https://kubernetes.io/case-studies/openai/)
[OpenAI 如何通过 Azure CNI 扩展 Kubernetes 至 7,500 节点](https://medium.com/@PlanB./how-openai-scaled-kubernetes-with-azure-cni-to-handle-7-500-nodes-591162d0efa5)
