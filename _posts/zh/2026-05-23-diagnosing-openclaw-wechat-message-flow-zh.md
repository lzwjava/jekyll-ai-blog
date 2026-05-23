---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诊断OpenClaw微信消息流
translated: true
type: note
---

好的，这是我的分析。我已经追踪了Hermes代码库中的完整消息流。

---

分析：Hermes Agent中的微信消息流
==============================================

代码实际执行的操作（Hermes Agent）
------------------------------------------

Hermes中的微信消息管道是：

1. 入站：WeixinAdapter._poll_loop() 长轮询 iLink API (getupdates)
2. 处理：_process_message() → 构建 MessageEvent → 调用 self.handle_message(event)
3. 分发：BasePlatformAdapter.handle_message() → 生成 _process_message_background()
4. 代理：_message_handler(event) → GatewayRunner._handle_message()
5. LLM：_run_agent() → 创建 AIAgent → 调用 agent.run_conversation()
6. 出站：响应通过 BasePlatformAdapter._send_with_retry() 发送
7. 发送：WeixinAdapter.send() → iLink sendmessage API

关键点：在Hermes中，微信适配器和代理位于同一进程中。
网关是一个单体——平台I/O + 代理循环 + 工具分发都运行在
一个Python进程中。在正常的网关流程中根本没有“ACP运行时”。

ACP适配器（acp_adapter/server.py）是一个独立的东西——它将Hermes
暴露为ACP服务器，供IDE客户端（VS Code、Zed、JetBrains）使用。它并
未连接到网关的平台适配器。

---

朋友的诊断描述的内容
--------------------------------------

报告提到了：
- “NewsBot Agent”，工作空间为 ~/.openclaw/workspace-newsbot
- “ACP (OpenClaw ACP)” 运行时
- “openclaw-weixin” 通道
- “Hermes integration at /tmp/VibApp/”

这不是标准的Hermes Agent设置。这是OpenClaw（或一个分支），其
架构不同：

  OpenClaw架构（从诊断中推断）：
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ 微信         │────>│ NewsBot      │────>│ ACP 运行时   │
  │ 通道         │     │ 代理         │     │ (OpenClaw)   │
  │ (openclaw-   │     │ (路由)       │     │              │
  │  weixin)     │     │              │     │              │
  └──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  │ 未连接
                                                  ▼
                                          ┌──────────────┐
                                          │ /tmp/VibApp/ │
                                          │ (Hermes 节点 │
                                          │  集成)       │
                                          └──────────────┘

---

根本原因分析
-------------------

诊断说：

  “微信消息已接收 ✅”
  “消息已路由至NewsBot代理 ✅”
  “NewsBot代理处理消息 ✅”
  “Hermes集成未触发 ❌”

这说得通。流程是：

1. 微信消息通过 openclaw-weixin 通道到达
2. OpenClaw 将其路由到 NewsBot 代理
3. NewsBot 分派给 ACP 运行时
4. ACP 运行时处理消息（LLM 调用）
5. ACP 运行时将响应返回给 NewsBot
6. ??? 响应从未到达微信

断连发生在步骤5和6之间。有两个可能的失败点：

可能性A：ACP 运行时返回了响应，但 OpenClaw 没有将其转发回微信
  - ACP 运行时处理了消息并生成了响应
  - 但响应停留在 ACP 协议层内部
  - OpenClaw 的 NewsBot 代理没有将其转发给微信通道
  - 这是 OpenClaw 的 ACP→通道桥接的 bug

可能性B：ACP 运行时静默失败
  - ACP 运行时接收到消息但出错
  - 错误被吞掉（用户看不到日志）
  - 微信通道从未收到响应

可能性C：/tmp/VibApp/ 的“Hermes 集成”完全是一个独立的东西
  - 它是一个独立的 Node.js 脚本，本应是响应路径的一部分
  - 但它根本没有接入 ACP 运行时
  - 它是作为概念验证创建的，但从未集成

---

需要检查的内容（给你的朋友）
-------------------------------

1. 检查 ACP 运行时日志——查看 ACP 处理步骤中的错误
   - 在 OpenClaw 中：查找与 newsbot 代理的 ACP 运行时相关的日志
   - 检查 LLM 调用是否成功并返回响应

2. 检查 NewsBot 的响应处理器是否连接到微信通道
   - 在 OpenClaw 配置中：验证 NewsBot 代理的输出通道
     是否设置为 openclaw-weixin（不仅仅是其输入）

3. /tmp/VibApp/ 的 Hermes 集成是一个干扰项
   - 它是一个独立的 Node.js 脚本，不是 OpenClaw 管道的一部分
   - 真正的问题在于 OpenClaw 的代理→通道桥接，而非 Hermes

4. 先用一个更简单的代理测试——尝试在 OpenClaw 中将微信路由到一个非 ACP 的代理
   以查看通道本身是否工作

---

结论
-----------

这是 OpenClaw 的问题，不是 Hermes Agent 的问题。我检查过的 Hermes 代码库
展示了一个干净、工作的微信管道（iLink 长轮询 → 网关运行器 → AIAgent → iLink sendmessage）。朋友的“NewsBot”加上 ACP 运行时是 OpenClaw 的架构，它具有不同的代理分发路径。/tmp/VibApp/ 的 Hermes 集成无关紧要——它从未连接到 OpenClaw 管道。

修复需要在 OpenClaw 中进行，具体来说是如何将 ACP 运行时的响应路由回微信通道适配器。