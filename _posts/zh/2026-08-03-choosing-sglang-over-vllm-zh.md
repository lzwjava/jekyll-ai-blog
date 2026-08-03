---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 选择SGLang而非vLLM
translated: true
type: note
---

问题：我应该贡献给哪个仓库：SGLang 还是 vLLM？

回答：

基于你的背景（Java 后端 → LLM 训练 → nanoGPT → vLLM 实验 → CUDA/GPU 好奇心），我建议优先考虑：

**1. 从 SGLang 开始**
SGLang

原因：

* 代码库比 vLLM 更小、迭代更快。
* 有更多机会做出有意义的贡献。
* 重点关注 **agent 工作负载、结构化生成、推理模型**，这与 LLM 应用的发展方向一致。
* 更容易理解整个技术栈：

  ```
  API 请求
      ↓
  调度器
      ↓
  分词器
      ↓
  KV 缓存
      ↓
  注意力后端
      ↓
  CUDA 内核
      ↓
  GPU
  ```

良好的初次贡献点：

```bash
git clone https://github.com/sgl-project/sglang
cd sglang
```

学习：

```
python/sglang/srt/
├── managers/        # 服务器生命周期
├── mem_cache/       # KV 缓存
├── models/          # 模型封装
├── layers/          # transformer 层
├── server_args.py
└── engine/
```

潜在的贡献路径：

### 第一层：Python 工程

示例：

* 添加模型支持
* 改进错误信息
* 添加基准测试
* 修复兼容性问题

这很适合你，因为你已经有生产后端的经验。

---

### 第二层：LLM 服务内部机制

学习：

* 连续批处理
* 分页注意力
* 前缀缓存
* 推测解码

然后贡献：

```
scheduler.py
scheduler_output.py
tokenizer_manager.py
```

---

### 第三层：GPU 内核工作

稍后：

```
sgl-kernel/
flashinfer/
triton 内核
```

学习：

```python
# 简单思路
Q @ K.T -> 注意力分数
scores @ V -> 输出
```

GPU 优化：

```
矩阵
  ↓
分块
  ↓
共享内存
  ↓
张量核心
  ↓
CUDA 内核
```

---

**2. 然后贡献给 vLLM**
vLLM

vLLM 是 LLM 服务领域的“Linux 内核”。

它在工业界有广泛采用。

但：

* 代码库更大
* 更成熟
* 第一个 PR 更难

架构：

```
vllm/
├── engine/
├── worker/
├── executor/
├── attention/
├── distributed/
├── model_executor/
└── cuda/
```

核心思路：

```
用户请求
    |
AsyncLLMEngine
    |
调度器
    |
KV 缓存管理器
    |
Worker
    |
CUDA 注意力内核
    |
GPU
```

vLLM 中适合贡献的领域：

* AMD ROCm 支持
* CUDA 内核
* 量化
* 新模型架构
* 性能基准测试

---

我建议的 6 个月路径：

```
第1个月：
  SGLang
  - 本地运行
  - 阅读架构
  - 提交文档/测试/小修复

第2-3个月：
  SGLang 内部机制
  - 调度器
  - KV 缓存
  - 批处理

第4个月：
  CUDA/Triton 内核贡献

第5-6个月：
  vLLM 贡献
  - 更深入的推理引擎工作
```

你目前的优势：

你已经：

* 从零训练过 GPT-2
* 使用过 nanoGPT
* 接触过 vLLM
* 理解 GPU 内存限制
* 拥有自己的 RTX 4070 环境

许多贡献者只了解 Python API。你的路径应该是：

```
模型训练
      ↓
PyTorch
      ↓
CUDA 内核
      ↓
推理引擎
      ↓
分布式服务
```

这种组合很罕见。

如果你的目标是 **AI 基础设施工程师职位（香港/新加坡/美国）**，那么在 SGLang/vLLM 中合并的几个 PR 可能比另一门课程或另一个玩具聊天机器人更有价值。

参考：

* [SGLang GitHub](https://github.com/sgl-project/sglang?utm_source=chatgpt.com)
* [vLLM GitHub](https://github.com/vllm-project/vllm?utm_source=chatgpt.com)
* [SGLang 文档](https://docs.sglang.ai/?utm_source=chatgpt.com)
* [vLLM 文档](https://docs.vllm.ai/?utm_source=chatgpt.com)