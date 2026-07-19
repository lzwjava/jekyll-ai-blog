---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI研究代理比较
translated: true
type: note
---

问题：在Claude、ChatGPT、Gemini等模型中，谁拥有“研究代理”？

答案：

大多数前沿AI实验室现在都有某种形式的**研究代理 / 深度研究模式**。其思路类似：模型不仅依靠自身权重进行回答，而是执行多步骤工作流：

```
用户问题
      |
      v
规划代理
      |
      +--> 搜索网页/论文/文档
      |
      +--> 阅读来源
      |
      +--> 提取事实
      |
      +--> 验证矛盾
      |
      +--> 撰写带引用的报告
```

主要参与者：

| 公司       | 产品                                    | 研究代理能力                              |
| ---------- | --------------------------------------- | ----------------------------------------- |
| OpenAI     | ChatGPT Deep Research                   | 最先进的全能型研究代理之一                |
| Anthropic  | Claude Research（通过Claude.ai功能）     | 擅长长文档处理与分析                      |
| Google     | Gemini Deep Research                    | 因整合Google Search而强大                 |
| Perplexity | Deep Research                           | 围绕搜索与答案合成构建                    |
| xAI        | Grok DeepSearch                         | 专注于网络研究                            |
| Microsoft  | Copilot Researcher                      | 企业级研究工作流                          |
| Alibaba    | Qwen deep research features             | 开源生态实验                              |
| DeepSeek   | Deep research style agents via ecosystem | 更多社区驱动                              |

### 1. OpenAI ChatGPT Deep Research

架构大致如下：

```
GPT模型
+
浏览器/搜索工具
+
代码执行
+
引用系统
+
长上下文推理
```

典型用途：

* “比较20款用于LLM训练的GPU服务器”
* “分析所有关于RLVR的论文”
* “寻找最佳开源代理框架”

它可以花费数分钟进行研究，而非立即生成回答。

---

### 2. Claude Research

Claude的优势：

* 非常强的长上下文阅读能力
* 出色的文档综合能力
* 良好的推理风格

常见工作流：

```
100篇PDF论文
        |
        v
Claude
        |
        v
研究地图
        |
        v
文献综述
```

例如：

“阅读这50篇机器学习论文，找出研究空白。”

Claude在这方面通常表现很好。

---

### 3. Gemini Deep Research

Google拥有天然优势：

```
Gemini
   |
Google Search
   |
Google Scholar
   |
YouTube
   |
Gmail/Drive（企业）
```

特别擅长：

* 当前信息
* 旅行研究
* 市场调研
* Google生态数据

---

### 4. Perplexity Deep Research

Perplexity几乎是一个原生研究型产品。

其核心循环：

```
问题
 |
搜索数十个页面
 |
对来源进行排序
 |
总结
 |
引用
```

非常适合：

* “这周发生了什么？”
* 竞争情报
* 产品对比

---

### 有趣的未来：多代理研究

未来可能不是：

```
一个巨型模型回答
```

而是：

```
研究经理代理

        |
        |
 -----------------------
 |          |           |
搜索代理   编码代理    评论代理

        |
        v

最终研究报告
```

例如：

```
GPT-5代理：
  “研究RTX 3090集群是否适用于LLM训练”

代理A：
  收集硬件基准测试

代理B：
  收集论文

代理C：
  计算经济性

代理D：
  质疑假设

最终：
  50页工程报告
```

这非常接近人类研究团队的工作方式。

鉴于你使用多个模型（Claude + GPT + Gemini 交叉验证）的实验，有趣的方向实际上是：

```
10个前沿模型
100个专业代理
1个研究组织
```

其中模型成为“研究员工”：

* Claude → 文献分析师
* GPT → 规划者/编码者
* Gemini → 网络/数据研究员
* DeepSeek → 高性价比工作者
* 本地Qwen → 私有数据工作者

瓶颈变成了**编排**，而非原始智能。