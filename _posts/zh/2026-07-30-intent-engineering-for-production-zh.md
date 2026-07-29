---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向生产的意图工程
translated: true
type: note
---

问题：IntentLab 的《将你的意图转化为生产系统》一文背后的核心理念是什么？

回答：

我从概念层面阅读了这篇文章。其核心思想与当前 AI 工程的发展方向高度一致：**瓶颈正从编写代码转向将人类意图转化为可靠的可执行系统**。（[Intent][1]）

传统软件流程：

```
人类需求
        |
        v
产品经理编写规格说明
        |
        v
工程师设计架构
        |
        v
工程师编写代码
        |
        v
测试 + 部署
```

AI 改变了这一点：

```
人类意图
      |
      v
AI 代理理解目标
      |
      v
创建规格/计划/工作流
      |
      v
生成代码 + 配置
      |
      v
运行 + 评估 + 改进
```

缺失的一层是 **意图工程（intent engineering）**。

---

## 1. 意图是新的抽象层

在传统编程中：

```
for i in range(10):
    print(i)
```

你指定的是 **如何做**。

在 AI 原生系统中：

```
"为我构建一个客服代理，将工单解决时间减少 50%"
```

你指定的是 **你想要什么结果**。

代理必须推断：

* 需求
* 架构
* API
* 数据源
* 评估标准
* 运营约束

因此新栈变成了：

```
意图
  |
  v
规格说明
  |
  v
代理工作流
  |
  v
工具 / API / 代码
  |
  v
生产系统
```

这类似于编译器曾经带来的变革：

```
机器码
     ^
     |
汇编
     ^
     |
高级语言
```

现在我们正朝着以下方向前进：

```
实现
      ^
      |
代理计划
      ^
      |
意图语言
```

---

## 2. 为什么当前 AI 编码工具不够用

像 Copilot/Cursor/Claude Code 这样的工具在以下方面表现出色：

```
prompt -> 代码
```

但生产环境需要：

```
意图
 |
 +--> 架构
 |
 +--> 数据库变更
 |
 +--> 安全
 |
 +--> 测试
 |
 +--> 部署
 |
 +--> 监控
 |
 +--> 迭代
```

示例：

人类：

> "创建一个在线市场。"

一个编码代理可以生成：

```
前端/
后端/
数据库 schema
API 端点
```

但生产环境的问题仍然存在：

* 使用哪个支付提供商？
* 欺诈规则是什么？
* 延迟目标是多少？
* 如何处理 100 万用户？
* 如何迁移 schema？
* 哪些指标定义成功？

难点不在于生成代码。

难点在于在数千个决策中保持意图不变。

---

## 3. 意图成为“控制平面（control plane）”

这与另一个新兴概念有关：位于执行系统之上的 AI 控制平面。例如，IntentR 描述了一个类似的概念：保留业务意图、协调 AI 执行、治理自主系统。（[intentrai.com][2]）

架构：

```
                人类
                  |
                  v
         意图规格说明
                  |
                  v
        +----------------+
        | 意图引擎        |
        +----------------+
          |      |      |
          v      v      v

     编码    数据    代理

          |
          v

     生产系统
```

意图层回答的问题是：

"这个系统是否仍在做人类想要它做的事？"

---

## 4. 这基本上就是“代理软件工程（agent software engineering）”

今天：

```
开发者
    |
    v
Git 提交
    |
    v
CI/CD
```

明天：

```
开发者
    |
    v
意图文档

示例：

目标：
"将云成本降低 30%"

约束：
- 无停机
- 延迟 <100ms
- 仅限 AWS

成功标准：
- 月度账单减少
- 错误率不变

    |
    v

代理持续优化
```

意图变成了一个活文档。

---

## 5. 类似的想法已经出现

### AI 产品设计

一些工具正从：

```
想法 -> 原型
```

转向：

```
意图 -> 规格 -> 待办事项 -> 实现上下文
```

例如，Intent 将自己定位为帮助产品团队将产品意图转化为实现就绪的工件。（[Intent][1]）

### AI 代理

生产代理需要：

* 记忆
* 评估
* 可观测性
* 护栏
* 回滚

因为失败模式已经改变。

传统软件：

```
bug -> 崩溃
```

代理软件：

```
错误推理
       |
       v
看似合理的输出
       |
       v
业务损害
```

围绕生产代理的社区讨论常常强调这种“静默失败”问题。（[Reddit][3]）

---

## 我的工程解读

这基本上等同于以下转变：

### 1970 年代

```
硬件 -> 汇编
```

### 1980 年代

```
汇编 -> C 语言
```

### 2000 年代

```
手动服务器 -> 云 API
```

### 2025 年以后

```
手动软件构建 -> 意图驱动系统
```

下一代的“编程语言”可能看起来不像代码。

它可能看起来像：

```yaml
goal:
  build: customer_support_agent

business_metric:
  reduce:
    ticket_resolution_time: 50%

constraints:
  budget: $500/month
  compliance: SOC2

tools:
  - zendesk
  - postgres
  - slack

evaluation:
  accuracy > 95%
  escalation_rate < 5%
```

然后代理将其编译为：

```
架构
+
代码
+
基础设施
+
测试
+
运维
```

对于正在构建 AI 代理、CLI 代理和咨询系统的人来说，这个方向可能是最重要的概念之一：**竞争优势从“谁写代码更快”转移到“谁能更好地编码意图、约束和反馈循环”。**

参考资料：

* Intent 文章：<https://intentlab.ai/blog/turn-your-intent-into-production-systems>
* （[Intent][1]）
* （[intentrai.com][2]）

[1]: https://www.useintent.ai/?utm_source=chatgpt.com "Intent - Know What to Build Before AI Writes the Code"
[2]: https://www.intentr.ai/?utm_source=chatgpt.com "IntentR — The Control Plane for Real-World AI"
[3]: https://www.reddit.com/r/test/comments/1tuhyhr/we_deployed_25_ai_agents_in_production_for/?utm_source=chatgpt.com "We deployed 25+ AI agents in production for clients before building our own observability tool. Here's the ugly truth about what actually breaks."
