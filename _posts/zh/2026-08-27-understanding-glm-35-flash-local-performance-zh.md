---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解GLM-3.5 Flash本地性能
translated: true
type: note
---

问题：如何理解“GLM-3.5 Flash 本地运行，单流 30–40 tokens/s，感谢 MIT 和 Berkeley 学者的 FreeToken 工作”？

回答：

这句话的基本意思是：

> “我们成功在本地硬件上部署了 GLM-3.5 Flash。对于单个请求流，推理速度约为每秒 30–40 个 token。我和我们的学生/社区团队想感谢 MIT 和 Berkeley 的研究人员发表了 FreeToken 工作。”

详细分解如下：

### 1. “GLM3.5 Flash 我们在本地已经跑通了”

意思是他们进行了**本地推理**，而不是调用 API。

示例：

```
用户
 |
 v
本地机器
 |
 v
GLM-3.5 Flash 权重
 |
 v
生成 token
```

他们可能下载了模型权重，并运行了类似以下命令：

```bash
python generate.py \
  --model glm-3.5-flash \
  --prompt "hello"
```

而不是：

```
你的应用
   |
   v
OpenAI API / 智谱 API
   |
   v
云端 GPU
```

本地意味着他们控制：

* GPU
* 内存
* 量化
* 推理引擎
* 延迟

---

### 2. “单流三四十”

这是一个推理基准测试。

语言模型逐个 token 生成文本：

```
输入：
"Explain transformer"

模型前向传播：

token 1
token 2
token 3
...
token N
```

速度：

```
tokens / second
```

因此：

```
30-40 tok/s
```

意思是：

```
一个用户
一个对话
一个生成流

≈ 每秒 30-40 个 token
```

对于人类对话来说，这感觉非常快。

示例：

一个普通回答：

```
500 tokens
```

在 40 tok/s 下：

```
500 / 40 = 12.5 秒
```

---

### 3. 为什么提到“单流”？

因为吞吐量和延迟是不同的。

单流：

```
GPU
 |
 用户 A
 |
 40 tok/s
```

多用户：

```
GPU
 |
 + 用户 A
 + 用户 B
 + 用户 C
```

同一块 GPU 可能达到：

```
单流：
40 tok/s

批处理：
总计 200 tok/s
```

但每个人可能得到：

```
10-20 tok/s
```

生产系统关心的是：

* 延迟
* 吞吐量
* 并发用户数

---

### 4. “FreeToken” 可能指推理优化

有趣的部分是感谢 MIT/Berkeley 的研究人员。

原因可能是某种降低推理成本的优化技术。

现代 LLM 推理的瓶颈：

```
Transformer 前向传播：

Attention:
Q K V

+
MLP

+
内存搬运
```

特别是在解码阶段：

```
token 1 -> token 2 -> token 3
```

模型反复读取权重和 KV cache。

问题通常是：

```
GPU 计算 < GPU 内存带宽限制
```

优化论文试图减少：

* KV cache 大小
* 内存搬运
* 冗余计算
* token 生成开销

因此，一个研究思路可以将：

```
A100:
20 tok/s
```

变成：

```
40 tok/s
```

而不改变模型。

---

### 5. 从工程角度看为什么这很有趣

这与 Linux/开源的模式相同：

研究人员发表：

```
论文
+
代码
+
权重
```

然后学生和工程师可以构建：

```
论文
      |
      v
实现
      |
      v
本地部署
      |
      v
初创公司/产品
```

AI 生态系统正在向 Linux 生态系统靠拢。

现在，一个小团队可以做到以前需要 Google/OpenAI 规模才能做的事情。

示例：

2018 年：

```
训练 transformer：
只有 Google 能做到
```

2026 年：

```
微调 7B/30B 模型：
一个人 + 多张 GPU
```

---

考虑到你自己的实验（从零开始训练 GPT-2 124M、nanochat、本地 Qwen/vLLM），关键要注意的是：

**模型架构只是成功的一半。推理栈正在成为一个重要的竞争层面。**

这个栈是：

```
模型架构
        |
        v
训练数据
        |
        v
权重
        |
        v
推理引擎
        |
        v
内核优化
        |
        v
硬件利用率
```

FreeToken 这类工作集中在：

```
推理引擎 + 内存效率
```

这正是为什么一个小团队可以在本地运行强大模型的原因。

参考文献：

* GLM 模型： [https://github.com/THUDM/GLM-4](https://github.com/THUDM/GLM-4)
* vLLM 推理引擎： [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
* FlashAttention： [https://github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)
