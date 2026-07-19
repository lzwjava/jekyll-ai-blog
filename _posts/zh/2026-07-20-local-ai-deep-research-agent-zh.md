---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地AI深度研究代理
translated: true
type: note
---

问题：`LearningCircuit/local-deep-research` 介绍

回答：

[Local Deep Research GitHub Repository](https://github.com/LearningCircuit/local-deep-research?utm_source=chatgpt.com) 是一个开源的**本地 AI 深度研究智能体**。可以将其视为 ChatGPT Deep Research / Gemini Deep Research 这类系统的自托管版本，但由你控制模型、数据和基础设施。

核心思路：

```
用户问题
      |
      v
研究智能体
      |
      +--> 网络搜索
      |
      +--> 学术搜索
      |
      +--> 本地文档
      |
      +--> 多次 LLM 调用
      |
      v
综合报告 + 引用
```

它不仅仅是 RAG，更接近于一个**智能体研究工作流**。

## 架构

主要组件：

```
                 +----------------+
                 |      用户       |
                 +--------+-------+
                          |
                          v
              +-----------+------------+
              | Local Deep Research    |
              |        智能体          |
              +-----------+------------+
                          |
        +-----------------+----------------+
        |                 |                |
        v                 v                v

    LLM 后端          搜索工具         知识库

    Ollama            SearXNG           PDF
    vLLM              网页              论文
    OpenAI API        arXiv             笔记
    Claude API        PubMed            文档
```

该项目支持：

* 通过 Ollama 使用本地 LLM
* 兼容 OpenAI 的端点
* 网络搜索
* 学术来源
* 你自己的文档库

README 将其描述为“用于深度、智能体式研究的 AI 驱动研究助手”，使用多个 LLM 和搜索引擎，并带有引用。

## 有趣的部分：智能体策略

关键部分是 **LangGraph 智能体策略**。

传统方式：

```
问题
   |
搜索 5 个 URL
   |
总结
   |
回答
```

智能体方式：

```
问题

LLM 思考：

"需要更多关于 X 的信息"

        |
        v

搜索 X

        |
        v

阅读结果

        |
        v

"需要学术来源"

        |
        v

搜索 arXiv/PubMed

        |
        v

比较来源

        |
        v

生成报告
```

智能体决定：

* 搜索什么
* 使用哪个搜索引擎
* 何时证据足够
* 何时综合

该仓库声称 LangGraph 智能体模式是其基准测试结果背后的关键。

## 本地硬件

对你的配置而言有趣的点：

该项目专门针对本地 GPU 使用。

README 提到：

> 在单张 RTX 3090（Qwen3.6-27B）上完全本地运行

并报告了以下基准测试数字：

* SimpleQA ~95%
* xbench-DeepSearch ~77%

在本地硬件上。

你的 RTX 4070 12GB 更受限，但可能的配置：

### 小型本地配置

```
RTX 4070
 |
 +-- Qwen3 8B / 14B
 |
 +-- Ollama
 |
 +-- Local Deep Research
```

### 严肃配置

```
2 x RTX 3090 24GB

48GB VRAM

      |
      +-- Qwen3 32B
      +-- Deep Research 智能体
      +-- 嵌入模型
```

这正是多 GPU 有用的工作负载类型。

## 安装

最简单的方式：

```bash
pip install local-deep-research

python -m local_deep_research.web.app
```

然后连接：

```
LLM：
  Ollama
  vLLM
  兼容 OpenAI API

搜索：
  SearXNG
```

该项目也提供了 Docker 部署。

## 与 ChatGPT Deep Research 对比

|                     | ChatGPT Deep Research | Local Deep Research |
| ------------------- | --------------------- | ------------------- |
| 模型               | OpenAI 模型           | 任意模型            |
| 数据隐私           | 云端                  | 本地                |
| 自定义知识         | 有限                  | 强大                |
| 成本               | 订阅/API 费用         | 硬件成本            |
| 智能体定制         | 有限                  | 完整代码访问        |
| 研究工作流         | 封闭                  | 开放                |

有趣的未来方向：

```
10 个模型
   |
100 个研究智能体
   |
交叉验证
   |
最终科学报告
```

该项目本质上是朝着这一目标的基础构建块。

## 对于你的“AI 代币工厂”想法

这个仓库非常接近 AI 公司的“研究部门”。

想象一下：

```
                    管理智能体

                         |
       +-----------------+----------------+
       |                 |                |

 文献智能体         代码智能体        市场智能体

 Claude             Qwen            Gemini

       |                 |                |

       +-------- 辩论 / 验证 ------------+

                         |

                  最终报告
```

Local Deep Research 提供了一个工人。下一步进化是**智能体组织**。

对于正在构建 CLI 智能体、模型训练实验和多模型工作流的人来说，这个仓库值得研究，主要在于：

1. LangGraph 编排
2. 搜索规划
3. 引用管道
4. 本地模型集成
5. 持久化知识库

它不仅仅是“ChatGPT 克隆”；它更接近于一个开源的研究操作系统。

参考文献：

* [Local Deep Research GitHub Repository](https://github.com/LearningCircuit/local-deep-research?utm_source=chatgpt.com)