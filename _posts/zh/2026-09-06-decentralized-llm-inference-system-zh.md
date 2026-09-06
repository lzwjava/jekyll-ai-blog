---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 去中心化大语言模型推理系统
translated: true
type: note
---

**BloomBee** 是一个去中心化系统，用于在点对点网络上提供大型语言模型（LLM）推理服务。

**核心理念：** 无需一台强大的 GPU 机器来承载庞大的模型（例如 LLaMA 3.1 405B），BloomBee 将模型的 Transformer 模块拆分到多个节点上——每个节点仅托管几层——并协同通过互联网处理推理请求。这利用了闲置的 GPU 资源，实现经济高效的 LLM 访问。

**它解决的关键挑战**（节点间带宽 + 每节点内存）：
- **张量卸载**——每个节点承载更多层，减少网络跳数
- **推测性解码**——每次往返发送多个草稿 token，降低通信频率
- **无损激活压缩**——在无精度损失下减少激活数据的字节数
- **微批次流水线**——将通信与计算重叠，隐藏延迟

**结构：** 这是一个 Python 项目（包含 `src/`、`tests/`、`benchmarks/`、`examples/` 以及 Docker 支持），已发布至 PyPI，基于 *hivemind* P2P 框架构建，并附有 arXiv 上的相关研究论文。它看起来像是源自 Petals 风格分布式推理思想的衍生或演进版本。

需要深入了解某个具体部分吗？比如 `src/` 中的架构，或推测性解码的工作原理？