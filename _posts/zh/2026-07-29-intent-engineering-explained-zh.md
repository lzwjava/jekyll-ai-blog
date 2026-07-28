---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 意图工程详解
translated: true
type: note
---

问题：解释 IntentLab 文章《将你的意图转化为生产系统》及其重要性。

回答：

我阅读了这篇文章。核心思想是：

> **AI 工程的下一个演进方向不是提示工程，而是意图工程：将人类目标转化为可执行的规范，使代理能够在生产环境中可靠地实现这些目标。** ([RJL.pub][1])

这与您一直在探索的方向高度一致：**循环工程、多代理、数字员工、Hermes 通知、代理编排。**

文章大致是在说：

```
提示：
"给我构建一个用户管理页面"

          ↓

任务：
"创建 CRUD API"

          ↓

意图：
"让管理员能够安全地管理用户，
在这些约束条件下，
带有可衡量的成功标准，
并在条件不满足时停止"

          ↓

生产系统
```

---

## 1. 提示 → 上下文 → 意图

作者认为 AI 开发经历了几个阶段：

### 阶段 1：提示工程

人类：

```
编写一个 Python 脚本来解析 CSV
```

AI：

```
生成代码
```

问题：

* 没有业务上下文
* 没有约束条件
* 没有成功定义

---

### 阶段 2：上下文工程

给 AI 提供：

```
CLAUDE.md
AGENTS.md
仓库结构
架构文档
数据库模式
API 文档
编码规则
```

现在代理理解了环境。

这与更广泛的行业趋势一致：可靠的代理需要高质量的上下文、检索、工具和记忆，而不仅仅是更好的提示。([elastic.co][2])

示例：

```
你正在使用 Spring Boot 3。

数据库：
PostgreSQL 16

规则：
- 控制器中不允许直接写 SQL
- 使用 MyBatis 映射器
- 所有 API 都需要 JWT
```

好多了。

---

### 阶段 3：意图工程

但上下文仍然回答的是：

> "我应该怎么做？"

它没有回答：

> "我为什么要做这个？"

意图增加了：

```
目标
成功标准
约束条件
权限
停止条件
人工升级规则
```

示例：

`migration.intent.yaml`

```yaml
目标:
  将遗留用户 API 迁移到 v2

成功标准:
  - 所有测试通过
  - p95 延迟 < 100ms
  - 零破坏性 API 变更

约束条件:
  - 不修改数据库模式
  - 不涉及支付模块

权限:
  - 编辑 backend/src/user

停止条件:
  - 业务规则不明确
  - 重试 3 次后测试仍然失败

升级:
  负责人: backend-team
```

现在代理有了一个契约。

---

# 为什么这很重要

传统软件：

```
人类
 |
 v
需求
 |
 v
工程师
 |
 v
代码
 |
 v
生产
```

AI 原生软件：

```
人类意图
      |
      v
意图规范
      |
      v
代理工作者
      |
      +---- 编码代理
      |
      +---- 测试代理
      |
      +---- 安全代理
      |
      +---- 审查代理
      |
      v
生产
```

人类向上移动。

你不再是：

```
逐行编写代码的人
```

你变成了：

```
定义目标、
约束条件、
架构、
评估的人。
```

---

# 与你“循环工程”的联系

你之前的想法：

> 代理醒来 → 检查状态 → 修复 → 重试 → 报告完成

实际上非常接近。

一个生产代理循环看起来像这样：

```python
while True:

    state = observe()

    if goal_completed(state):
        notify_user()
        break

    action = agent.decide(
        intent=intent_spec,
        context=context,
        tools=tools
    )

    execute(action)

    evaluate()
```

许多代理系统中缺失的部分是：

```
evaluate()
```

如果没有评估：

```
代理认为：
"我完成了"

人类看到：
"它搞坏了生产环境"
```

意图提供了评估器。

---

# 多代理示例

想象一家人工智能软件公司。

人类：

```
构建一个 SaaS 计费系统
```

意图：

```yaml
目标:
  上线 Stripe 订阅计费

成功标准:
  - 客户可以订阅
  - 生成发票
  - 退款功能正常
  - 安全审查通过

约束条件:
  - PCI 合规
  - 不存储卡号
```

代理：

```
CEO 代理
 |
 +-- 产品代理
 |
 +-- 架构师代理
 |
 +-- 后端代理
 |
 +-- 前端代理
 |
 +-- QA 代理
 |
 +-- 安全代理
```

每个代理接收：

```
相同的意图
不同的职责
```

---

# 有趣的商业含义

这改变了 AI 咨询。

旧式咨询：

```
"我们将构建一个 AI 聊天机器人"
```

新式咨询：

```
"我们将把你的业务流程转化为
意图规范 + 自动化工作流。"
```

有价值的产品不再是代码。

而是：

```
业务流程
        ↓
意图模型
        ↓
代理工作流
        ↓
评估系统
```

---

# 我对你 AI 公司方向的看法

这篇文章基本上描述了您正在接近的产品类别。

您的技术栈可以变成：

```
意图层
    |
    +-- intent.yaml
    |
代理运行时
    |
    +-- Claude/OpenAI/Qwen
    |
工具
    |
    +-- MCP
    +-- shell
    +-- 浏览器
    +-- 数据库
    |
评估
    |
    +-- 测试
    +-- 指标
    +-- 人工审批
```

一个最小实现：

```
project/
├── intent.yaml
├── context.md
├── agents/
│   ├── coder.py
│   ├── tester.py
│   └── reviewer.py
├── tools/
└── evals/
```

基本上：

**GitHub Actions + Claude Code + MCP + 评估框架 + 意图文件。**

这很可能就是 AI 工程的发展方向：从“调用 LLM API”转向“运营自主生产系统”。([RJL.pub][1])

参考文献：

* ([RJL.pub][1])
* ([elastic.co][2])

[1]: https://rjl.pub/?utm_source=chatgpt.com "RJL.pub - AI-Native Development Journey | RJ Lindelof"
[2]: https://www.elastic.co/elasticsearch/context-engineering?utm_source=chatgpt.com "Context engineering for AI agents | Elastic"
