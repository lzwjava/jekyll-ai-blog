---
audio: false
generated: true
image: false
lang: zh
layout: post
title: vLLM 与 llama.cpp 应用场景对比
translated: true
type: note
---

问题：为什么人们使用 vLLM？对比 vLLM 与 llama.cpp。

答案：

人们使用 **vLLM** 主要是为了 **高吞吐量服务**，而 **llama.cpp** 用于 **本地轻量级推理**。它们针对 **不同的工作负载**。

---

# 核心区别（一句话概括）

* **vLLM** → 面向 **大量并发用户** 的服务器，高吞吐量 🚀
* **llama.cpp** → 在 **小型硬件上本地运行**，设置简单 🧠

---

# 架构差异

### vLLM

* GPU 优先推理引擎
* 采用 **PagedAttention**（KV 缓存分页）
* 跨用户批量处理
* 为 API 服务优化
* 需要大容量 GPU 显存

### llama.cpp

* CPU 优先（可选 GPU 支持）
* 无动态批处理
* 单用户/少量用户
* GGUF 量化格式
* 可在笔记本/小型 GPU 运行

---

# 性能对比

| 特性               | vLLM        | llama.cpp   |
| ------------------ | ----------- | ----------- |
| 多用户支持         | ✅ 优秀      | ❌ 较差      |
| 吞吐量             | ✅ 极高      | ❌ 低        |
| 单用户延迟         | ⚠️ 中等      | ✅ 极好      |
| CPU 支持           | ❌ 否        | ✅ 优秀      |
| GGUF 支持          | ❌ 否        | ✅ 原生支持  |
| 内存效率           | ⚠️ 中等      | ✅ 最优      |
| 大模型服务         | ✅ 最优      | ⚠️ 有限      |
| RTX 4070 兼容性    | ⚠️ 有限      | ✅ 最优      |
| 生产环境 API       | ✅ 理想      | ⚠️ 基础      |
| 工具调用支持       | ✅ 良好      | ✅ 良好      |

---

# 企业选择 vLLM 的原因

因为 vLLM 能够：

### 1. 同时服务大量用户

示例：

* 50 名用户同时聊天
* vLLM 批量处理请求
* GPU 利用率约 90%
* 吞吐量提升 10 倍

llama.cpp：

* 顺序处理请求
* GPU 经常空闲
* 整体速度慢得多

---

### 2. 提供 OpenAI 兼容的 API 服务器

vLLM 提供：

```bash
vllm serve model
```

然后可调用：

```bash
POST /v1/chat/completions
```

使用者包括：

* OpenWebUI
* OpenClaw
* LangChain
* AutoGen
* 各类智能体

---

### 3. 更高效的批处理

示例：

单个请求：

* llama.cpp 更快

10 个请求：

* vLLM **快得多**

100 个请求：

* vLLM **快几个数量级**

---

# 个人选择 llama.cpp 的原因

因为它能：

### 1. 在小型 GPU 上运行

你可以运行：

* 26B IQ3
* 34B IQ2
* 甚至 70B CPU 版本

在 RTX 4070 上：

* llama.cpp → 可以
* vLLM → 无法运行

---

### 2. 支持 GGUF 格式

以下格式均可运行：

```
Q4_K_M
IQ3_S
IQ2_XS
```

vLLM 无法加载这些格式。

---

### 3. 显存需求更低

26B 模型示例：

| 引擎             | 显存需求 |
| ---------------- | -------- |
| vLLM             | ~30GB    |
| llama.cpp IQ3    | ~13GB    |

差异巨大。

---

# 何时使用 vLLM

使用 vLLM 如果：

* 构建 API 服务器
* 多用户聊天场景
* 智能体集群
* 高吞吐量需求
* GPU ≥ 24GB
* 数据中心环境

---

# 何时使用 llama.cpp

使用 llama.cpp 如果：

* 本地开发
* RTX 4070 / 4060 显卡
* GGUF 格式模型
* 单用户使用
* 离线环境
* 内存受限

---

# 你的情况（RTX 4070）

你应该优先选择：

👉 llama.cpp
而非 vLLM

因为：

* 12GB 显存
* 需要运行 26B 模型
* 需要 GGUF 格式
* 单用户使用

vLLM 对你 **没有优势**。

---

# 简单类比

vLLM = 餐厅厨房 🍽️

* 同时烹饪多份订单
* 规模化效率高

llama.cpp = 家庭烹饪 🍳

* 适合单人使用
* 简单灵活

---

# 最终建议

根据你的硬件配置：

RTX 4070 + 本地模型 → **llama.cpp 胜出**

仅当你升级到以下配置时才考虑 vLLM：

* RTX 4090
* A100
* 3090
* 多 GPU 服务器
