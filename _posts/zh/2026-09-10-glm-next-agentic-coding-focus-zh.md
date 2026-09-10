---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'GLM Next: 智能体编码聚焦'
translated: true
type: note
---

**问题：GLM Next 模型有什么特别之处？**

**回答：** 如果你所说的“GLM Next”指的是 Z.ai 当前**下一代 GLM 系列**，那么有趣之处在于 Z.ai 越来越多地围绕**长周期智能体编程（long-horizon agentic coding）**优化 GLM，而不仅仅是打造一个更好的聊天机器人。

截至 2026 年 9 月，相关的发展脉络是 **GLM-5 → GLM-5.1 → GLM-5.2 → GLM-5.3**。Z.ai 自己的研究页面将 GLM-5.3 列为最新版本。（[Z.ai][1]）

### 1. 关键：后训练 > 仅仅扩展基础模型

GLM-5.3 特别有趣，因为**据报道它使用的底层基础模型与 GLM-5.2 基本相同**。改进来自于在长周期环境上进行了更多后训练/强化学习（RL）。（[Kie][2]）

这一点很重要。

旧范式：

```text
更多数据
   ↓
更多参数
   ↓
更好的模型
```

新的范式越来越倾向于：

```text
强基础模型
      ↓
更好的环境
      ↓
更好的轨迹
      ↓
强化学习 / 智能体训练
      ↓
更优的现实世界任务完成度
```

对于编程智能体而言，这可以说比静态基准测试再提升 20% 更为重要。

### 2. 极度面向智能体

GLM-5 的技术方向明确是**“从氛围编程（vibe coding）到智能体工程（agentic engineering）”**。Z.ai 将其描述为针对复杂系统工程和长周期智能体任务。（[Z.ai][1]）

因此，不再是：

```text
用户 → 提示 → 代码
```

而是更接近以下循环：

```text
目标
 ↓
推理
 ↓
检查仓库
 ↓
编辑文件
 ↓
运行编译器/测试
 ↓
观察失败
 ↓
调试
 ↓
修改
 ↓
再次测试
 ↓
重复 × N
```

这与你使用 `ww`、`iclaw`、Codex/Claude Code 风格智能体时做的事情非常接近。

### 3. 巨大的 MoE，但活跃计算量相对较小

GLM-5 的总参数量约为 **744B，活跃参数约 40B**。（[THE D*AI*LY BRIEF][3]）

概念上：

```text
744B 参数
       │
       ├── 专家 1
       ├── 专家 2
       ├── ...
       └── 专家 N
             ↑
       路由器选择专家
             ↓
       约 40B 活跃
```

因此，它拥有前沿级别的*容量*，而无需对每个 token 进行密集的 744B 计算。

这也是 GLM 在**推理工程**角度同样值得关注的原因之一。

### 4. 长上下文不仅仅是营销数字

GLM-5.2/5.3 已迈向 **100 万 token 上下文**，尤其适用于长时间运行的编程/智能体工作负载。（[Eigent][4]）

这改变了智能体架构。

不再需要不断进行摘要：

```text
仓库
 ↓
摘要
 ↓
摘要的摘要
 ↓
智能体丢失细节
```

你可以将以下内容保留在一个巨大的工作上下文中：

```text
大型仓库
+ 终端历史
+ 测试失败信息
+ 之前尝试
+ 文档
+ 任务状态
```

对于自主编程智能体来说，**上下文持久性本身就是一种能力**。

### 5. GLM-5 的架构包含一些真正有趣的推理技巧

GLM-5 的技术报告描述了：

* 约 744B MoE
* 约 40B 活跃
* DeepSeek 稀疏注意力
* 多潜在注意力（Multi-Latent Attention）
* 多 Token 预测（Multi-Token Prediction）
* 渐进式长上下文训练
* 从 issue/PR 对中获取的大规模软件工程数据

稀疏注意力工作尤其相关，因为百万 token 上下文下的朴素全注意力变得荒谬。（[THE D*AI*LY BRIEF][3]）

因此，这里有一些超越单纯“中国版 Claude”的有趣想法。

---

### 我认为对**你**来说最有趣的部分

实际上并不是 744B 参数这个数字。

而是这一点：

> **GLM 正在成为一个围绕智能体与计算机交互的反馈循环而训练的模型。**

这是一个不同的优化目标。

传统大语言模型：

```text
P(下一个 token | 文本)
```

智能体编程模型：

```text
P(动作 / 代码 / 工具调用
  | 目标, 仓库, 环境, 之前动作, 观察结果)
```

而真正的目标变得更接近：

```text
P(任务最终成功)
```

而不是：

```text
P(下一个 token 是正确的)
```

这就是为什么如果你在构建 CLI 智能体，最近 GLM 的进步值得关注。

而 GLM-5.3 尤其有趣，因为它提供了证据表明：**在真实的长周期环境上进行强化学习/后训练，即使不改变底层预训练模型，也能产生巨大收益**。（[Kie][2]）

如果你愿意，我可以接下来详细拆解 **GLM-5 的实际架构 + 训练流程，从 token → MoE 路由器 → 注意力 → MTP → 强化学习**，达到与 nanoGPT/nanochat 相同的实现级别。

[1]: https://www.zhipuai.cn/en/research?utm_source=chatgpt.com "Z.ai - Inspiring AGI to Benefit Humanity"
[2]: https://kie.ai/blog/glm-5-3-zhipu-next-model?utm_source=chatgpt.com "GLM-5.3: What the Zhipu Signals Actually Say"
[3]: https://www.beri.net/learning/glm-5-technical-report?utm_source=chatgpt.com "GLM-5 — Advanced Paper (Free) | THE D*AI*LY BRIEF"
[4]: https://www.eigent.ai/blog/glm-5-2?utm_source=chatgpt.com "GLM-5.2: Zhipu AI's 1M-Token Open-Weight Coding Model"
