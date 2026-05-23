---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw架构与ACP故障排除
translated: true
type: note
---

好的，我现在对 OpenClaw 架构有了全面了解。以下是完整分析：

---

OPENCLAW 架构分析：NewsBot 微信问题
====================================================

OPENCLAW 的工作原理（根据代码）
-----------------------------------

OpenClaw 的架构与 Hermes Agent 有根本不同：

  ┌──────────────────────────────────────────────────────────┐
  │                    GATEWAY (server.ts)                    │
  │                  中央枢纽，会话管理                       │
  ├──────────────┬──────────────┬────────────────────────────┤
  │  通道        │   代理       │   ACP 控制平面             │
  │  (微信,      │   运行器     │   (外部代理                │
  │   Telegram,  │   (内嵌      │    进程)                   │
  │   Discord,   │    PI)       │                            │
  │   ...)       │              │                            │
  └──────┬───────┴──────┬───────┴──────────┬─────────────────┘
         │              │                  │
         │         ┌────┴────┐        ┌────┴────┐
         │         │内嵌      │        │ACP 代理 │
         │         │PI 运行器│        │进程     │
         │         │(进程内) │        │(spawn)  │
         │         └─────────┘        └─────────┘
         │                                   │
    微信 iLink API                   JSON-RPC/stdio
    (长轮询)                          (ACP 协议)


你朋友设置中的消息流程
-----------------------------------------

1. 微信消息通过 `openclaw-weixin` 通道插件到达
2. 通道适配器调用 `runChannelTurn()` (src/channels/turn/kernel.ts)
3. Turn 内核调用 `runDispatch()`，进入 Gateway
4. Gateway 解析该会话的代理 → 找到 "newsbot" 代理
5. NewsBot 代理配置了 ACP 运行时
6. Gateway 启动/连接到外部 ACP 代理进程
7. 消息通过 ACP 协议发送到 ACP 代理
8. ACP 代理处理消息（LLM 调用）
9. 响应通过 ACP 协议返回
10. Gateway 将响应传递给微信通道
11. 通道通过 iLink sendmessage API 发送回复

与 HERMES 的关键区别
------------------------------------

在 Hermes 中：Agent + Gateway + 通道 = 一个进程
在 OpenClaw 中：Agent 可以是单独进程（ACP 运行时）

ACP 代理进程定义在：
  - src/acp/server.ts —— ACP 服务器，作为客户端连接到 Gateway
  - src/acp/translator.ts —— 将 ACP 协议 ↔ Gateway 调用进行转换
  - src/agents/acp-spawn.ts —— 生成 ACP 代理进程

ACP 服务器通过 WebSocket 连接到 Gateway，并作为客户端接收提示并返回响应。

---

根本原因分析
-------------------

诊断信息显示：
  "微信消息已接收 ✅"
  "消息已路由到 NewsBot 代理 ✅"
  "NewsBot 代理已处理消息 ✅"
  "Hermes 集成未触发 ❌"

最后一行是混淆所在。位于 "/tmp/VibApp/" 的 "Hermes 集成" 并不是 OpenClaw 流程的一部分。它是一个独立的 Node.js 脚本，从未连接过。

真正的问题是：为什么 ACP 代理没有返回响应？

三种可能性：

A) ACP 代理进程未运行
   - NewsBot ACP 代理进程可能未启动
   - Gateway 尝试连接但静默失败
   - 检查：`openclaw status` 或 Gateway 日志中的 ACP 连接错误

B) ACP 代理进程在收到提示时崩溃
   - ACP 代理进程启动，但在接收提示时崩溃
   - 错误在 ACP 协议层中被吞没
   - 检查：ACP 代理进程日志（stderr 输出）

C) 代理配置不匹配
   - NewsBot 代理配置可能指向不存在的 ACP 后端
   - 或者工作空间 (~/.openclaw/workspace-newsbot) 没有正确的配置/技能/模型
   - 检查：`~/.openclaw/config.yaml` 中 `agents.list` 的 "newsbot" 条目 —— 确认 `acpBackend`、`model`、`workspace` 字段

---

需要检查的内容（给你的朋友）
-------------------------------

1. 检查 ACP 代理进程是否在运行：
   用 `ps aux | grep acp` 查找 NewsBot ACP 进程

2. 检查 Gateway 日志中的 ACP 错误：
   在 gateway 日志输出中查找 "acp" 或 "newsbot"

3. 检查代理配置：
   读取 ~/.openclaw/config.yaml —— 找到 id 为 "newsbot" 的 `agents.list` 条目。确认：
   - `acpBackend` 设置正确
   - `model` 有效
   - `workspace` 路径存在

4. 检查 ACP 会话状态：
   查看 `~/.openclaw/sessions/` 中的 NewsBot 会话 —— 检查是否有包含代理响应的记录文件

5. /tmp/VibApp/ 的 Hermes 集成无关紧要
   - 它是一个独立的 Node.js 脚本
   - 它未连接到 OpenClaw 的流程
   - 删除或忽略它 —— 它不是修复方案

---

结论
-----------

问题出在 OpenClaw 的 ACP 代理调度上，而不是 Hermes。
位于 /tmp/VibApp/ 的 "Hermes 集成" 是干扰项 —— 它从未属于 OpenClaw 流程。

朋友需要：
1. 验证 NewsBot ACP 代理进程是否实际在运行
2. 检查 gateway 日志中的 ACP 连接/提示错误
3. 验证 ~/.openclaw/config.yaml 中的代理配置
4. 如果 ACP 过于复杂，将 NewsBot 切换到使用内嵌 PI 运行时（从代理配置中移除 `acpBackend`）

切换到内嵌 PI 运行时将使流程与 Hermes 的工作方式相同 —— 代理在进程内运行，无需管理外部 ACP 进程。