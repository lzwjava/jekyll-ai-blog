---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 第一棵树：AI团队上下文工作空间
translated: true
type: note
---

以下是 **first-tree** 的简介：

## 高层概述

这是一个面向 **人机协作团队的** **开源工作空间与上下文层**。核心理念是：与其让每个 AI 代理从孤立的提示（prompt）中冷启动任务，不如让代理从一个共享的、基于 Git 的知识库（称为 **上下文树**）中读取信息，并将结果写回到该知识库。

可以将其理解为 **代理与人类共同维护的团队记忆**。

## 架构

这是一个包含 5 个包的 pnpm monorepo（单一代码仓库）：

| 包名 | 作用 |
| --- | --- |
| `apps/cli` | `first-tree` / `ftd` 命令行工具 — 登录、守护进程、代理管理、树操作 |
| `packages/server` | Fastify API 服务器 (PostgreSQL/Drizzle/Zod) — SaaS 后端 |
| `packages/client` | SDK + AgentRuntime — 封装 WebSocket 通信、处理器注册、codex/copilot 运行时胶水代码 |
| `packages/shared` | Zod 模式定义 + 类型 — 在服务器/客户端/CLI 之间共享，是数据传输对象（DTO）的唯一真实来源 |
| `packages/web` | React 19 + Vite Web 工作空间 — 用于聊天、代理和上下文树的图形界面 |

## 它解决了什么问题

当代理或人类需要理解某个东西 *为何* 以某种方式构建时，通常无处可查。PR 被合并，问题被关闭，文档逐渐过时。上下文树是一个 **递归的 `NODE.md` 结构**（包含 markdown 文件的 Git 仓库），用于保存持久的决策、所有权、约束条件和领域知识。

## 工作原理

1. **上下文树** — 代理在执行任务前读取的 markdown 文件 Git 仓库
2. **Web 工作空间** — 用于代理、团队成员和 GitHub 集成的聊天界面
3. **命令行工具 + 守护进程** — 将计算机注册到系统，保持本地代理连接
4. **代理运行时** — 在您的机器上运行代理（Claude Code, Codex, 您自己的代理），并通过 First Tree 进行路由
5. **GitHub 集成** — 将 PR、代码审查关联回工作空间

其循环流程为：

```
用户意图 -> 读取团队上下文 -> 代理在上下文感知下工作
-> 人工审核/控制 -> 持久化的结果 -> 更新团队上下文
```

## 谁创建的

从组织名称 `agent-team-foundation/first-tree` 来看——由一支每天深入使用 AI 代理的团队构建。

## 开发进度

主分支约 500 次提交，包含 CI、用于本地开发的 Docker Compose 配置、广泛的 API 接口、数据库迁移、可观测性（OpenTelemetry）以及 GitHub 应用集成。该项目正在积极开发中——最近的几次提交涉及重构代理简报生成、分离服务生命周期后端以及暴露终端提供者故障。已具备实际生产环境雏形。

需要我深入介绍某个具体的包或子系统吗？
