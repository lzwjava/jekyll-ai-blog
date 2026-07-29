---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MazeBench空间规划测试
translated: true
type: note
---

**MazeBench** 是一个评估基准，旨在测试多模态大语言模型是否真正理解迷宫图像中的**空间规划**，而不仅仅是进行模式匹配或将图像转换为文本并通过暴力搜索获得解。([arXiv][1])

核心思想：

```
迷宫图像
      |
      v
 视觉模型
      |
      v
 内部表示？
      |
      v
 规划 / 导航
      |
      v
 正确路径
```

人类看到迷宫会构建心智地图：

```
起点
 |
 +---+
     |
     +---- 终点
```

但许多大语言模型似乎采取了不同的方式：

```
迷宫图像
    |
    v
“将像素转换为网格”
    |
    v
“逐步尝试路径”
    |
    v
令牌级广度优先搜索
```

MazeBench 这篇论文认为，高准确率可能具有误导性，因为模型通常通过**文本枚举/搜索**来解决迷宫，而非类人的空间推理。([arXiv][1])

---

## 它测试什么？

典型任务：

1. 给模型一张迷宫图像。
2. 提问：

> 找到从起点到终点的路径。

该基准设有多种变化：

* 迷宫大小
* 难度
* 视觉复杂度
* 推理预算
* 模型是否允许使用中间表示

报告中使用的基准包含 **110 张程序生成的迷宫图像**，并评估了 **16 种多模态模型配置**。([arXiv][1])

---

## 有趣的结果

一个令人惊讶的观察结果：

模型可能得分很高，但底层能力仍然不足。

示例：

```
人类：
  看到迷宫
  构建心智图
  找到最短路径

大语言模型：
  图像 -> 文本网格
  A1 B1 C1...
  枚举可能性
  输出答案
```

该基准发现，某些模型消耗数千个令牌来解决人类几乎瞬间就能完成的迷宫。([arXiv][1])

当已经提供正确的网格表示时，模型性能显著提升，这表明部分问题在于**视觉锚定**，而非纯粹的推理。([arXiv][1])

---

## 这对智能体为何重要

这直接关系到当前的智能体研究。

一个编程智能体、浏览器智能体、机器人智能体等需要：

```
观察
   |
   v
维护世界状态
   |
   v
规划
   |
   v
行动
   |
   v
再次观察
```

MazeBench 暴露出一个弱点：

当前大语言模型擅长：

```
上下文 -> 下一个令牌
```

但在以下方面较弱：

```
环境 -> 持久世界模型 -> 动作
```

这类似于其他迷宫智能体基准中讨论的“世界模型”问题：智能体需要内部状态追踪，而不仅仅依赖当前上下文窗口做出响应。([arXiv][2])

---

## 与你 vLLM / nanoGPT 实验的关联

这实际上是理解 Transformer 局限性的一个极好基准。

nanoGPT：

```
令牌
 |
 Transformer
 |
 下一个令牌概率
```

MazeBench 要求：

```
像素
 |
 表示
 |
 记忆
 |
 规划
 |
 动作序列
```

缺失的部分不仅在于更大的模型：

* 外部记忆
* 状态表示
* 搜索
* 工具使用
* 循环迭代

这就是为什么现代智能体系统看起来像：

```
大语言模型
 +
记忆
 +
工具
 +
规划器
 +
环境反馈
```

而不仅仅是：

```
GPT(提示词) -> 答案
```

对于正在构建智能体（Hermes 风格循环、编程智能体、工具使用系统）的人来说，MazeBench 比传统的 MMLU 式基准更接近实际问题。([arXiv][2])

参考文献：

* ([arXiv][1])
* ([arXiv][2])
* ([Hugging Face][3])

[1]: https://arxiv.org/abs/2603.26839?utm_source=chatgpt.com "From Pixels to BFS: High Maze Accuracy Does Not Imply Visual Planning"
[2]: https://arxiv.org/abs/2607.00627?utm_source=chatgpt.com "AGI Maze as a Benchmark Framework for World-Modeling Agents"
[3]: https://huggingface.co/papers/2603.26839?utm_source=chatgpt.com "Paper page - From Pixels to BFS: High Maze Accuracy Does Not Imply Visual Planning"