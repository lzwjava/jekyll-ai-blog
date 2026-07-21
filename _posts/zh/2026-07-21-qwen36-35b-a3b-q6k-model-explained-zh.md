---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen3.6-35B-A3B Q6_K模型解析
translated: true
type: note
---

**问题：** `mradermacher/Qwen3.6-35B-A3B Q6_K` 模型是什么？

**答案：**

`mradermacher/Qwen3.6-35B-A3B-Q6_K` 是阿里巴巴 **Qwen3.6-35B-A3B** 模型的 **GGUF 量化版本**，用于通过 `llama.cpp`、LM Studio、Ollama 等工具进行本地推理。（[Hugging Face][1]）

结构解析：

```
Qwen3.6-35B-A3B
│       │    │
│       │    └── A3B = 30亿激活参数
│       └────── 350亿总参数
└────────────── 模型系列
```

### 1. 35B-A3B = 混合专家模型

它**不是一个普通的密集 35B 模型**。

它是一个混合专家模型：

```
总参数：
    350 亿

每 token 激活：
    ~30 亿

推理计算量：
    接近 3B 模型

内存需求：
    接近 35B 模型
```

路由器选择专家：

```
token
 |
路由器
 |
+---------+
| 专家1    |
| 专家2    |  <-- 活跃的专家
| 专家3    |
+---------+
 |
FFN 输出
 |
下一层
```

因此，与密集的 7B/14B 模型相比，每个 FLOP 能获得高得多的智能。Qwen 将其描述为一个 350 亿总参数 / 30 亿激活参数的 MoE 模型，专为编码、推理、多模态任务和长上下文设计。（[Qwen Studio][2]）

---

### 2. Q6_K 表示 6 位量化

原始 FP16：

```
350 亿参数 × 2 字节

≈ 70 GB 显存
```

Q6_K：

```
350 亿参数 × ~0.75 字节

≈ 28.6 GB 模型文件
```

mradermacher GGUF 版本显示：

```
Q6_K:
  大小：~28.6 GB
  质量：非常好
```

（[Hugging Face][1]）

比较：

| 量化   | 大小   | 质量   |
| ------ | ------ | ------ |
| Q4_K_M | ~21 GB | 良好   |
| Q5_K_M | ~25 GB | 非常好  |
| Q6_K   | ~29 GB | 极好   |
| Q8_0   | ~37 GB | 接近 FP16 |

（[Hugging Face][1]）

---

### 3. 硬件要求

纯 GPU 运行：

```
Q6_K 模型：
~29 GB 显存

+ KV 缓存
+ 运行时开销
```

实际需求：

* RTX 3090 24GB ❌（需要内存卸载）
* RTX 4090 24GB ❌（同样）
* RTX 6000 Ada 48GB ✅
* A6000 48GB ✅
* MI300X 192GB ✅
* 配备 64GB 统一内存的 Mac ✅

对于 24GB 显卡：

```bash
llama-server \
  -m Qwen3.6-35B-A3B-Q6_K.gguf \
  --n-gpu-layers 60
```

会将部分层卸载到 CPU 内存。

---

### 4. 为什么这个模型很有趣

最佳平衡点：

```
Qwen3.6-35B-A3B-Q6_K

智能水平：
    ~大型模型级别

活跃计算量：
    ~3B

内存需求：
    ~29GB

速度：
    远快于密集的 35B 模型
```

用于智能体：

```
Claude Code 风格工作流
        |
        v
Qwen3.6-35B-A3B-Q6_K
        |
        +-- 编码
        +-- 工具调用
        +-- 长上下文
        +-- 规划
```

这正是 MoE 擅长的模型类型：**具备接近前沿的能力，但无需前沿推理成本**。社区测试也报告 Q6_K 是当你有足够 RAM/VRAM 时本地智能体编码的实用选择。（[Reddit][3]）

---

针对你的硬件：

* RTX 4070 12GB → 除非重度 CPU 卸载（慢），否则无法本地运行
* RTX 3090 24GB → Q4/Q5 量化更好
* MI300X 192GB → 此模型轻而易举，可以运行多个并发副本

一个好的 AMD ROCm 测试将是：

```
MI300X
  |
  llama.cpp ROCm
  |
  Qwen3.6-35B-A3B-Q6_K
  |
  兼容 OpenAI 的 API
  |
  智能体 / 编码基准测试
```

此模型基本上是目前较好的“本地 AI 智能体大脑”候选之一。（[Qwen Studio][2]）

参考资料：

* ([Hugging Face][1])
* ([Qwen Studio][2])
* ([Reddit][3])

[1]: https://huggingface.co/mradermacher/Qwen3.6-35B-A3B-GGUF?utm_source=chatgpt.com "mradermacher/Qwen3.6-35B-A3B-GGUF · Hugging Face"
[2]: https://qwen.ai/blog?id=qwen3.6-35b-a3b&lid=1qgBzVUzv0DLHy9oa&utm_source=chatgpt.com "Qwen"
[3]: https://www.reddit.com/r/LocalLLaMA/comments/1tb3zxp/local_llm_autocomplete_agentic_coding_on_a_single/?utm_source=chatgpt.com "Local LLM autocomplete + agentic coding on a single 16GB GPU + 64GB RAM"
