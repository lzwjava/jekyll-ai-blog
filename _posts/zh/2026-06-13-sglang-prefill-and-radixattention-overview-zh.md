---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang预填充与RadixAttention概述
translated: true
type: note
---

**问题：** 什么是 SGLang，其中的 prefill 是如何工作的？

---

## SGLang：是什么

SGLang（Structured Generation Language）不仅仅是另一个推理服务器——它是一个用于高效 LLM 执行的完整系统，结合了 Python 嵌入式前端语言和高度优化的后端运行时。前端提供了用于定义复杂生成程序的原语——例如并行提示执行、受限生成和多步推理链。后端通过 RadixAttention 等创新技术处理实际推理，实现跨请求的自动 KV 缓存共享。

SGLang 由加州大学伯克利分校的 SGLang 团队和开源社区开发，驱动着超过 400,000 个 GPU，每天处理数万亿个 token，已被 xAI、AMD、NVIDIA、LinkedIn、Cursor、Oracle、Google Cloud、Microsoft Azure 和 AWS 采用。

它还集成了 DeepSeek 特定的优化——MLA 吞吐量优化、MLA 优化内核、数据并行注意力、多 token 预测和 DeepGemm——使其成为服务 DeepSeek 模型的首选方案。

---

## 架构：两层

### 1. 前端 DSL（Python 原生）

你使用 `sgl.*` 原语将 LLM 程序编写为 Python 代码：

```python
import sglang as sgl

@sgl.function
def multi_turn_qa(s, question):
    s += sgl.system("你是一个精确的助手。")
    s += sgl.user(question)
    s += sgl.assistant(sgl.gen("answer", max_tokens=256))
    s += sgl.user("用一句话总结你的回答。")
    s += sgl.assistant(sgl.gen("summary", max_tokens=64))
```

这使得运行时能够提前看到*整个计算图*——从而实现跨分支的批处理、跨步骤的 KV 重用以及并行性。

### 2. 后端运行时

关键组件：
- **RadixAttention**——前缀 KV 缓存重用（详情见下文）
- **分块 prefill（Chunked prefill）**——将 prefill 块与 decode 交错，防止 TTFT 尖峰
- **零开销 CPU 调度器**——无停顿的连续批处理
- **XGrammar**——通过压缩的 FSM 实现受限解码（结构化 JSON 输出）
- **FlashInfer / FlashAttention 后端**——实际的 CUDA 内核调度

---

## SGLang 中的 Prefill 如何工作

标准 prefill 回顾：给定一个包含 N 个 token 的提示，你通过所有 Transformer 层执行一次完整的前向传播来填充 KV 缓存。这是计算密集型的，且注意力计算复杂度为 O(N²)。只有在这之后，你才开始自回归解码。

SGLang 在此基础上的创新：

### RadixAttention：跳过冗余 Prefill

在现有的推理引擎中，请求处理完成后其 KV 缓存被丢弃，阻止了 KV 缓存在多次调用之间重用。相反，SGLang 在基数树中维护所有请求的 KV 缓存的 LRU 缓存。这种方法将 KV 缓存视为传统缓存，并利用基数树进行高效匹配、插入和淘汰。

数据结构是一个**基数树**（基于 token 序列的 trie）：

```
root
├── [system_prompt_tokens...] ← 共享前缀的缓存 KV
│   ├── [user_question_A...]  ← 仅计算这部分增量
│   └── [user_question_B...]  ← 仅计算这部分增量
```

SGLang 的 RadixAttention 使用基数树为任何传入请求找到最长的缓存前缀，并仅将未缓存的后缀路由到 prefill 计算路径。

通过共享前缀，内存使用量与唯一内容成正比，而非总 token 数：无前缀缓存时——3 个请求 × 1000 个 token = 内存中 3000 个 token；有前缀缓存时——800 个共享 + 3 × 200 个唯一 = 1400 个 token（节省 53%）。缓存的 KV 状态无需重新计算：prefill 时间仅计算新（未缓存）token 的注意力，从而显著降低具有缓存前缀的请求的 TTFT。

然后，注意力后端（FlashInfer 等）接收 RadixCache 中的索引，并仅对未缓存的 token 计算注意力，将新的 KV 条目追加到缓存中。

### 分块 Prefill（Chunked Prefill）

长提示可能会使 decode 请求陷入饥饿（队头阻塞）。SGLang 将 prefill 工作分块：

- 将一个 4096 token 的 prefill 拆分为，例如，4 × 1024 块
- 将每个块与一个 decode 步骤交错
- GPU 保持忙碌，decode 延迟不会尖峰

这由服务器中的 `--chunked-prefill-size` 控制。

### PD 分离（Prefill-Decode 拆分）

SGLang 通过 prefill-decode 分离，在 96 个 GPU 上实现了 52.3K 输入 token/s 和 22.3K 输出 token/s——比普通的张量并行快 5 倍。

其思想：prefill 是计算密集型的（矩阵运算为主），decode 是内存带宽密集型的（小批量，大量 KV 读取）。在同一 GPU 上运行它们会相互竞争。PD 分离：

- **Prefill 节点**：计算优化，处理完整提示的 KV 填充
- **Decode 节点**：内存带宽优化，处理 token 生成
- KV 缓存通过 NVLink/RDMA 在节点之间传输

SGLang 通过 Mooncake TransferEngine 支持 PD 分离部署模式。SGLang 还引入了 HiCache，它扩展了 RadixAttention（以前仅限于 GPU 内存），增加了分层缓存支持——GPU 内存作为 L1，主机内存作为 L2，分布式存储作为 L3——与 Mooncake 等分布式存储后端集成。

启动方式如下：
```bash
# Prefill worker
python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3 \
  --disaggregation-mode prefill --port 8001

# Decode worker
python -m sglang.launch_server --model-path deepseek-ai/DeepSeek-V3 \
  --disaggregation-mode decode --port 8002

# Router
python -m sglang.launch_router --prefill http://localhost:8001 \
  --decode http://localhost:8002
```

---

## 快速开始（你的 MI300X 设置）

```bash
pip install sglang[all]

# 启动服务器
python -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V3 \
  --tp 8 \
  --chunked-prefill-size 2048 \
  --port 30000

# 查询
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-ai/DeepSeek-V3", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

## SGLang 与 vLLM 在 Prefill 上的对比

| 特性 | SGLang | vLLM |
|---|---|---|
| 前缀缓存 | RadixTree（自动，LRU） | 基于哈希（手动） |
| 分块 prefill | 是 | 是 |
| PD 分离 | 原生（Mooncake） | 单独（Dynamo） |
| DeepSeek MLA | 优化内核 | 标准 |
| 吞吐量（70B） | 约 3.1× vLLM | 基线 |

鉴于你正在 MI300X 上运行 DeepSeek 模型，SGLang 是正确选择——它是唯一通过 ROCm 在 AMD 上提供一流 MLA 内核支持的引擎。

---

## 参考资料

- [SGLang 论文：结构化语言模型程序的高效执行](https://arxiv.org/abs/2312.07104)
- [SGLang 加入 PyTorch 生态系统](https://pytorch.org/blog/sglang-joins-pytorch/)
- [RadixAttention 文档](https://sgl-project-sglang-93.mintlify.app/concepts/radix-attention)
- [HiCache + Mooncake 设计](https://kvcache-ai.github.io/Mooncake/design/hicache-design.html)
- [PD 分离深入探讨](https://www.spheron.network/blog/prefill-decode-disaggregation-gpu-cloud/)