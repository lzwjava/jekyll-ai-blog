---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IDC中国智能体2026报告
translated: true
type: note
---

## 问题：什么是 IDC Agent 报告（例如“Data Agent 重塑数据厂商” / IDC China Agent 2026）？

## 回答：

IDC Agent 报告是国际数据公司（IDC）发布的**企业市场研究报告**，分析 **AI Agent 如何改变企业软件、数据平台、基础设施和厂商**。

你提到的文章是 IDC 围绕 **Data Agent** 所做的 2026 趋势分析的一部分——并非单一的“Agent 模型排名”。它关注的是**企业 AI Agent 生态系统**。（[IDC][1]）

核心观点：

> 传统企业软件 = 人操作应用程序。
> Agent 时代 = 人表达目标，Agent 执行工作流。

例如：

传统 BI：

```
CEO：
“上个月销售额怎么样？”

分析师：
1. 打开 BI 工具
2. 编写 SQL
3. 关联表
4. 构建仪表盘
5. 解释结果
```

Data Agent：

```
CEO：
“上个月广东收入为什么下降？”

Data Agent：

1. 理解意图
2. 查询 ERP + CRM + 仓库
3. 生成 SQL
4. 分析异常
5. 查找原因
6. 建议行动
7. 创建报告
```

---

## IDC 对中国 Agent 2026 的市场看法

IDC 将 Agent 生态系统划分为几个层级：（[IDC][2]）

```
                    企业应用
        ------------------------------------------
        销售 Agent | HR Agent | 财务 Agent
        编码 Agent | 客服 Agent


                    Agent 平台层
        ------------------------------------------
        Agent 构建器
        工作流引擎
        工具调用
        记忆
        评估
        安全


                    模型层
        ------------------------------------------
        GPT / Claude / Qwen / DeepSeek
        多模态模型


                    数据层
        ------------------------------------------
        Data Agent
        知识图谱
        向量数据库
        Lakehouse
        数据治理


                    基础设施
        ------------------------------------------
        GPU
        云
        存储
        网络
```

---

# 什么是 Data Agent？

IDC 将 Data Agent 定义为：

> 利用 Agent 技术，通过对话式或低代码界面管理、治理、查询、分析和使用企业数据。（[IDC][3]）

它涵盖：

```
数据集成 Agent
        |
        |
数据治理 Agent
        |
        |
数据发现 Agent
        |
        |
Text-to-SQL Agent
        |
        |
BI 分析师 Agent
        |
        |
决策 Agent
```

---

## 为什么 IDC 认为 Data Agent 很重要

因为企业 AI 的瓶颈不仅仅是模型。

真正的瓶颈：

```
       LLM
        |
        |
   智能
        |
        |
-------------------
        ？
-------------------
        |
企业数据
```

公司拥有：

* ERP
* CRM
* HR 系统
* 数据库
* 文档
* 日志
* 知识库

但数据是：

```
孤立
+
脏乱
+
权限受限
+
缓慢
```

Agent 需要：

```
实时数据
+
上下文
+
权限
+
记忆
+
行动能力
```

IDC 预测，到 2028 年，中国 60% 的 top 500 企业将部署企业 Data Agent。（[IDC][1]）

---

# 这个领域有哪些厂商？

## 1. 传统数据厂商

它们添加 Agent 能力：

示例：

* 数据仓库厂商
* 数据库厂商
* BI 厂商
* 数据治理厂商

优势：

```
已拥有企业数据
+
客户关系
+
安全合规
```

---

## 2. 云厂商

示例：

* 阿里云
* 腾讯云
* 华为云
* AWS
* Microsoft Azure

它们提供：

```
模型
+
计算
+
数据平台
+
Agent 平台
```

---

## 3. AI Agent 创业公司

它们构建：

```
Agent 运行时
+
工作流
+
工具
+
记忆
+
MCP 集成
```

示例：

* Manus 风格自主 Agent
* 编码 Agent
* 研究 Agent

---

# 为什么 IDC 发布这些报告？

因为企业采购者需要答案：

### CIO 问：

“我们应该构建 Agent 平台吗？”

### CTO 问：

“哪种架构？”

### 厂商问：

“市场在哪里？”

### 投资者问：

“谁会赢？”

IDC 销售：

* 市场规模
* 厂商评估
* 技术评估
* 咨询

---

# 对于 AI 工程师，重要的收获

2026 年企业 AI 堆栈正在从以下方向转变：

```
2023：
聊天机器人 + RAG

2024：
Copilot

2025：
工作流 Agent

2026：
Agent 平台

2027+：
自主企业软件
```

有价值的工程技能正在转移：

旧：

```
微调模型
构建聊天机器人
构建 API
```

新：

```
Agent 编排
工具调用
MCP
记忆系统
评估
企业数据集成
安全 / 权限
可观测性
```

获胜架构更接近：

```
用户
 |
Agent 路由器
 |
规划器
 |
+-------------+
| 工具        |
| SQL         |
| API         |
| 浏览器      |
| 代码        |
+-------------+
 |
记忆
 |
企业数据
 |
执行
```

IDC 对 2026 年的主要信息基本上是：

**AI Agent 不会取代企业软件；它们将成为企业软件之上的新执行层。**（[IDC][4]）

参考文献：

* （[IDC][1]）
* （[IDC][3]）
* （[IDC][4]）
* （[IDC][2]）

[1]: https://www.idc.com/resource-center/blog/%E5%BD%93%E6%95%B0%E6%8D%AE%E5%BC%80%E5%A7%8B%E4%B8%BAagent%E8%80%8C%E7%94%9F%EF%BC%9Aidc-futurescape-2026-%E7%BB%99%E4%B8%AD%E5%9B%BD%E4%BC%81%E4%B8%9A%E7%9A%84%E5%8D%81%E4%B8%AA%E5%85%B3%E9%94%AE%E4%BF%A1%E5%8F%B7/?utm_source=chatgpt.com "IDC - 当数据开始为Agent而生：IDC FutureScape 2026 给中国企业的十个关键信号"
[2]: https://www.idc.com/wp-content/uploads/2025/11/IDC-Asia-Pacific-FutureScape-2026_China-AI-Excerpt.pdf?utm_source=chatgpt.com "IDC Market Glance: 中国 AI Agent 市场概览 2025Q4"
[3]: https://www.idc.com/resource-center/blog/resource-region/3_337/page/5/?utm_source=chatgpt.com "China Archives - Page 5 of 15 - IDC"
[4]: https://www.idc.com/resource-center/blog/agentic-ai-ecosystems-navigating-the-megatrend-thats-reshaping-enterprise-technology-markets/?utm_source=chatgpt.com "IDC - Agentic AI Ecosystem: Market Landscape & Layers | IDC"