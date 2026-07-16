---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2026 AI：智能体与基础设施变革
translated: true
type: note
---

问题：最近几个月有哪些重要的AI新闻（涉及智能体/AI基础设施/GPU/前沿实验室）？

答案：

根据你的关注点（大语言模型训练、智能体、GPU集群、基础设施），整体趋势如下：

**2026年的AI正从“更好的聊天机器人”转向“自主软件工人+AI工厂”。**

重要故事如下：

---

## 1. 编程智能体成为杀手级应用

最大的转变：

> 大语言模型 → 智能体 → 长期运行的工程工作者

不再是Copilot的自动补全。

新架构：

```
用户
 |
智能体（Claude Code / Codex / Cursor 等）
 |
规划器
 |
工具执行
 |
Shell
 |
Git
 |
测试
 |
云部署
```

近期趋势：

* 终端原生智能体
* 多智能体编程
* 持久记忆
* 工具编排
* 上下文工程

Anthropic发布了一篇关于Claude Code的深度解读，展示了CLI智能体如何演变为严肃的编程工作流。([Anthropic][1])

研究也表明，CLI智能体正在成为真正的工程工作流，而不仅仅是演示。微软对早期Claude Code / Copilot CLI采用情况的研究发现，采用者的合并请求数量有可测量的增长。([arXiv][2])

对于正在构建`ww`、`iclaw`、`zz`的人来说，这可能是价值最高的领域。

我目前的心智模型：

```
2024年：
AI助手编写代码片段

2025年：
AI智能体编写功能

2026年：
AI工程师处理工单
```

---

# 2. MCP → 智能体基础设施战争

下一层基础设施是：

```
模型
 |
智能体运行时
 |
MCP / 工具
 |
企业系统
```

每个人都在构建：

* 工具调用
* 智能体记忆
* 工作流引擎
* 权限
* 评估
* 可观测性

AWS推出了“Agent Toolkit”，专注于让编程智能体安全地与云服务协作。([Amazon Web Services, Inc.][3])

未来的基础设施类似于Kubernetes：

之前：

```
应用
 |
Kubernetes
 |
云
```

未来：

```
智能体
 |
智能体运行时
 |
工具 / MCP
 |
云API
```

---

# 3. 前沿实验室在智能体上竞争，而不仅仅是模型

## OpenAI

主要方向：

```
GPT模型
+
Codex
+
智能体平台
```

Codex正从“编程助手”转向自主编程工作流。([OpenAI][4])

## Anthropic

Anthropic最大的战略资产可能是：

```
Claude
+
Claude Code
+
企业开发者
```

Claude Code正在成为他们切入开发者的楔子。([Anthropic][1])

## Google DeepMind

Google正在推动：

```
Gemini
+
计算机使用
+
科学智能体
+
多模态智能体
```

近期Gemini发布的重点在于智能体行为和计算机使用能力。([Google DeepMind][5])

## 新实验室

Mira Murati的Thinking Machines值得关注，因为他们押注于：

```
开放/可定制的基础模型
+
企业微调
```

而不仅仅是封闭的聊天机器人。([Axios][6])

---

# 4. GPU战争：NVIDIA仍占主导，但推理改变经济格局

行业分化：

## 训练

仍然是：

```
H100
H200
B200
GB200
GB300
```

的主导地位。

护城河：

* CUDA
* NCCL
* 网络
* 集群管理
* 编译器栈

## 推理

更有趣。

问题：

“能否廉价地运行智能？”

重要技术：

* vLLM
* TensorRT-LLM
* SGLang
* 推测解码
* 量化
* MoE服务

未来GPU利用率：

```
训练集群
        |
        v
推理工厂
        |
        v
数百万智能体
```

---

# 5. 开源模型持续进步

重要趋势：

```
巨大的封闭模型
        ↓
较小的开源模型
        ↓
专用的智能体模型
```

胜出的模型可能不是：

“一个10T参数的上帝模型”

而是：

```
小型专家模型
+
工具
+
记忆
+
验证
```

例如：

```
70B模型
+
Python执行器
+
浏览器
+
RAG
+
规划器
```

可以超越更大的纯聊天模型。

---

# 6. AI基础设施瓶颈从GPU转向电力和数据中心

下一个约束：

不仅仅是GPU。

现在：

```
GPU
 |
HBM
 |
网络
 |
电力
 |
数据中心
```

大型AI集群正在变成电力基础设施项目。研究正在探索灵活的数据中心，根据电网约束动态调度工作负载。([arXiv][7])

---

# 7. 个人AI实验室 / OPL趋势

这符合你的“一人实验室”想法。

架构：

```
人
 |
AI CEO智能体
 |
-----------------
|       |       |
编程  研究    数据
智能体 智能体  智能体
 |
GPU工作站/云
```

一个工程师拥有：

* RTX 5090/3090级别机器
* 云GPU爆发
* 智能体
* 自动化

现在可以像一个小型创业团队一样运作。

---

# 8. 未来6-12个月我会关注什么

我对你的排名：

## 第一梯队

### 智能体运行时

学习/构建：

* MCP
* 工具调用
* 记忆
* 评估
* 沙箱执行

### 编程智能体

研究：

* Claude Code架构
* OpenAI Codex架构
* SWE-agent风格系统

## 第二梯队

### 推理基础设施

学习：

```
vLLM
SGLang
TensorRT-LLM
CUDA内核
KV缓存
连续批处理
```

### 分布式训练

你当前的路径：

```
单张RTX4070
        ↓
2张GPU
        ↓
多节点
        ↓
100B tokens
```

正好对齐。

## 第三梯队

GPU硬件：

有趣的二手市场：

* RTX 3090 24GB
* A6000 48GB
* Tesla P40/P100/V100
* AMD MI50/MI100 (ROCm实验)

但严肃工作仍是NVIDIA生态胜出。

---

我的总结：

```
2023年：
Transformer

2024年：
RAG

2025年：
智能体

2026年：
智能体操作系统

2027年：
AI原生公司
```

最大的机会可能不是训练下一个GPT。

而是构建**智能体基础设施层**，让一个人能够控制数千个AI工作者。

参考文献：

* Google DeepMind AI新闻：([Google DeepMind][5])
* Anthropic Claude Code更新：([Anthropic][1])
* Gartner编程智能体市场分析：([Gartner][8])
* AWS Agent Toolkit：([Amazon Web Services, Inc.][3])
* AI编程智能体采用研究：([arXiv][2])

[1]: https://www.anthropic.com/news?type=research&utm_source=chatgpt.com "Newsroom \ Anthropic"
[2]: https://arxiv.org/abs/2607.01418?utm_source=chatgpt.com "Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI"
[3]: https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/?utm_source=chatgpt.com "Announcing Agent Toolkit for AWS — help AI coding agents build effectively on AWS - AWS"
[4]: https://openai.com/index/gartner-2026-agentic-coding-leader/?utm_source=chatgpt.com "OpenAI named a Leader in enterprise coding agents by Gartner | OpenAI"
[5]: https://deepmind.google/blog/?utm_source=chatgpt.com "News — Google DeepMind"
[6]: https://www.axios.com/2026/07/15/mira-murati-thinking-machines-open-weight-model-inkling?utm_source=chatgpt.com "Mira Murati's Thinking Machines debuts first AI model"
[7]: https://arxiv.org/abs/2606.25098?utm_source=chatgpt.com "Power-Flexible AI Data Centers: A New Paradigm for Grid-Responsive Compute"
[8]: https://www.gartner.com/en/newsroom/press-releases/2026-05-20-gartner-says-the-market-for-enterprise-ai-coding-agents-is-entering-a-new-phase-of-expansion-and-competitive-realignment?utm_source=chatgpt.com "Gartner Says the Market for Enterprise AI Coding Agents Is Entering a New Phase of Expansion and Competitive Realignment"