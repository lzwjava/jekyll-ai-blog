---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 长序列上下文并行
translated: true
type: note
---

**问题：** 这段关于 SGLang Context Parallel 设计的中文技术文本是什么意思？

**回答：**

这是一份幻灯片/演讲记录，解释了 **为什么 SGLang 需要上下文并行（CP）来处理长序列推理**。以下是完整解析：

---

## 第一节：动机——为什么长序列会打破传统方法

**上下文长度每代约增长 10 倍**（从 GPT-1 2018 年至今）。随着序列变长，两个问题会叠加：

**KV 缓存内存**：KV 缓存大小为 `O(seq_len * num_layers * num_heads * head_dim)`。对于大型模型上的 128K token 序列，这可能达到几十 GB —— 很容易超过单 GPU 显存。

**注意力计算**：如果没有稀疏注意力或滑动窗口，注意力在计算和内存上都是 `O(seq_len²)`。在 128K+ token 时，这非常吃力。

**为什么张量并行（TP）在这里失效**：TP 在 GPU 间拆分权重矩阵，但不拆分*序列维度*。每个 GPU 仍然需要为其层看到完整的 KV 缓存。你无法通过 TP 来摆脱 192K token 序列。

**GQA/MLA 的难题**：GQA（分组查询注意力，用于 LLaMA 3）和 MLA（多头潜在注意力，用于 DeepSeek）压缩了 KV 头。这使得基于 TP 的朴素 KV 分片更加困难 —— 当 KV 头数量少于 TP 度数时，你无法将 KV 头均匀地分到各 TP 秩上。

**结论**：CP 不再是可选项 —— 它是长序列在线服务的基础原语。

---

## 第二节：SGLang 运行时架构（简化基线）

当前（CP 前）的运行时流程：

```
客户端 HTTP 请求
    → VPC 服务器
    → TokenizerManager（分词 → token ID）
    → 运行时（收集批处理请求）
    → 广播到 N 个工作进程（例如 TP=4，即 4 个工作进程）
        每个工作进程：
            - 检查本地 RadixCache / KV 缓存（前缀复用）
            - 运行 BatchScheduler
            - 执行前向传播（注意力 + FFN）
    → Detokenizer
    → 响应客户端
```

从混乱的 OCR/转录中解码的关键术语：

- **"Td4"** → TP 度数为 4（4 个张量并行工作进程）
- **"PVit Cache / TdCache"** → RadixCache（SGLang 的带树结构的前缀感知 KV 缓存）
- **"Batch Scanner"** → BatchScheduler / 连续批处理循环
- **"DumpDump"** → 可能是 "decode" 步骤（prefill → decode）
- **"Zero FQ"** → ZeroMQ（SGLang 在分词器和运行时之间使用的 IPC 传输）

---

## 第三节：CP 增加了什么

文本最后说 SGLang 需要**将 CP 集成到现有框架中**，以最小化长序列的推理延迟。

在实践中，SGLang 中的 CP 意味着：

```
序列 [T0...T_N] 在 CP 秩之间拆分：
  CP 秩 0：[T0 ... T_{N/2}]    → GPU 0
  CP 秩 1：[T_{N/2}...T_N]     → GPU 1

每个秩计算本地 QKV，然后：
  - 环注意力（在环上传送 K, V）用于因果掩码
  - 或者：在注意力之前全收集 KV（更简单，但内存更多）
```

这是**环注意力** —— 标准的 CP 原语。SGLang 的实现处理了与 RadixCache 的交互（跨 CP 秩的前缀复用并非易事）。

---

## 总结

该文本是一个技术演讲的介绍，解释了：

1. 序列长度扩展 → KV 缓存和注意力计算爆炸
2. 仅靠 TP 无法解决，尤其在有 GQA/MLA 的情况下
3. SGLang 当前架构（ZMQ → 运行时 → TP 工作进程 → RadixCache）
4. 需要将 CP 分层引入，以在生产吞吐量下处理 128K+ token 服务

如果你在深入阅读 SGLang 内部实现，关键文件是 `python/sglang/srt/managers/schedule_batch.py`（BatchScheduler）、`radix_cache.py` 以及 `srt/layers/attention/` 中的注意力后端。
