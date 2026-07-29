---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Trae AI 编程 IDE 简介
translated: true
type: note
---

**TRAE** 是字节跳动推出的 AI 原生编程 IDE，定位是：

> "真正的 AI 工程师"——与开发者协作的 AI 编程工程师，而不仅仅是自动补全。([Trae][1])

可以将其视为字节跳动对以下产品的回应：

* Cursor
* GitHub Copilot
* Windsurf

它本质上是 **VS Code + LLM 代理 + 项目理解 + 自主编码工作流**。([Trae][2])

---

## 核心理念

传统 IDE：

```
人类
 |
 | 编写代码
 v
IDE
 |
 v
编译器 / 运行时
```

AI IDE：

```
人类意图
      |
      v
  AI 代理
      |
 +----+----+
 |         |
代码库    工具
 |         |
 v         v
修改      测试
代码      调试
 |
 v
可运行的软件
```

开发者从：

> "编写每一行代码"

转变为：

> "定义意图、审查变更、引导代理"

这与 Claude Code、OpenAI Codex 代理、Kimi Code、Manus 风格代理的方向一致。

---

## 主要功能

### 1. AI 结对编程

你可以提问：

```
解释这个仓库
查找身份验证漏洞
重构这个模块
添加 API 端点
编写测试
```

代理会读取项目上下文并编辑文件。

类似的工作流：

```bash
git clone my-project

trae

> 理解这个仓库
> 将 Spring Boot 2 迁移到 3
> 运行测试并修复错误
```

---

### 2. Builder 模式

一个有趣的功能是 "Builder"：

你描述一个产品：

```
构建一个 SaaS 仪表盘。

需求：
- React 前端
- Spring Boot 后端
- PostgreSQL 数据库
- 用户登录
- 支付页面
```

代理会尝试：

1. 创建架构
2. 生成文件
3. 安装依赖
4. 连接组件
5. 运行/调试

([Trae][3])

这更接近于一个 **AI 软件工厂**。

---

### 3. SOLO 代理

TRAE 有一个更自主的模式叫做 SOLO。

概念上：

```
任务
 |
 v
规划代理
 |
 +-- 编码代理
 |
 +-- 测试代理
 |
 +-- 调试代理
 |
 v
最终 PR
```

TRAE 将 SOLO 描述为一个能够通过规划和执行来处理更大开发任务的代理。([Trae][2])

---

### 4. MCP / 工具集成

现代 AI 编码代理需要工具：

```
LLM
 |
 +-- 文件系统
 +-- 终端
 +-- 浏览器
 +-- git
 +-- 数据库
 +-- 文档
```

TRAE 支持 MCP 风格的外部工具访问，允许代理使用额外的资源。([Trae][2])

---

## 为什么字节跳动要构建它？

因为软件工程正在变成一场代理竞赛。

旧栈：

```
工程师
   |
 IDE
   |
 代码
```

新栈：

```
工程师
   |
 意图
   |
 AI 代理团队
   |
 代码库
   |
 生产环境
```

字节跳动已经拥有：

* 庞大的工程组织
* 内部代码库
* AI 模型基础设施
* 产品迭代文化

因此，AI IDE 具有战略意义。

---

## 与 Cursor 的对比

粗略比较：

|            | TRAE                     | Cursor                 |
| ---------- | ------------------------ | ---------------------- |
| 公司       | 字节跳动                 | Anysphere              |
| 基础       | VS Code 风格             | VS Code 分支           |
| 重点       | AI 工程师工作流          | AI 结对编程            |
| 代理       | 强强调                   | 强                     |
| 企业       | 发展中                   | 发展中                 |
| 生态系统   | 字节跳动生态系统         | 独立                   |

---

## 对于构建代理 / AI 产品的人

TRAE 之所以有趣，是因为它代表了下一个抽象：

以前：

```
开发者编写代码
```

现在：

```
开发者设计循环：

目标
 ↓
代理
 ↓
工具
 ↓
反馈
 ↓
迭代
```

这与你 "循环工程" 的想法一致。

未来的工程师可能会花更多时间编写：

```yaml
agent:
  goal: 迁移支付服务
  tools:
    - github
    - terminal
    - database
  evaluator:
    - unit_test
    - benchmark
```

而不是手动编辑数千行代码。

---

## 需要关注的事项

### 隐私

与任何云 AI IDE 一样：

```
你的代码
   |
   v
远程模型推理
   |
   v
AI 提供商服务器
```

对于私有公司代码，请仔细检查策略。社区已有讨论和报告提出关于遥测和数据收集的问题，因此企业在采用前应审查安全设置。([TechRadar][4])

---

## 我的看法

TRAE 不仅仅是 "另一个 Copilot"。

有趣的部分是转变：

```
Copilot 时代 (2022-2024)

AI = 自动补全


代理时代 (2025+)

AI = 初级工程师
```

TRAE、Cursor、Claude Code、Codex、Kimi Agent 都在争夺同一个未来：

**人类 + AI 软件开发的操作系统。**

对于你的工作流（nanoGPT、vLLM、代理、CLI 工具），一个有趣的实验是：

```
TRAE + 你的仓库
        |
        v
提问：
"理解这个 AI 代理框架。
找出 5 个架构改进点。
实现其中一个并运行测试。"
```

这可以测试它是否真的是一个工程代理，而不仅仅是一个聊天包装器。([Trae][2])

参考资料：

* [TRAE 官方网站](https://www.trae.cn/)
* [TRAE AI IDE 产品页面](https://www.trae.ai/?utm_source=chatgpt.com)
* [TRAE 企业介绍](https://www.trae.cn/enterprise?utm_source=chatgpt.com)

[1]: https://www.trae.cn/ "TRAE - The Real AI Engineer | TRAE - The Real AI Engineer"
[2]: https://www.trae.ai/?utm_source=chatgpt.com "TRAE - Collaborate with Intelligence"
[3]: https://trae.ai-kit.cn/home.html?utm_source=chatgpt.com "Trae ｜ 官网下载 ｜ 文档·教程 | 字节跳动免费AI编程IDE"
[4]: https://www.techradar.com/pro/security/bytedance-ai-tool-caught-spying-on-users?utm_source=chatgpt.com "ByteDance AI tool Trae caught spying on users"