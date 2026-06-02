---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes子代理委托与失败
translated: true
type: note
---

以下是 Hermes 中子代理的工作机制以及网络问题处理的全面说明：

## 子代理委派如何工作

架构（工具位于 `tools/delegate_tool.py`）：

```
父代理（你的主对话）
  └─ delegate_task 工具调用
       ├─ [subagent-0] ── ThreadPoolExecutor 工作线程 ── child.run_conversation()
       ├─ [subagent-1] ── ThreadPoolExecutor 工作线程 ── child.run_conversation()
       └─ [subagent-2] ── ThreadPoolExecutor 工作线程 ── child.run_conversation()
            （最多 max_concurrent_children，默认 3 个）
```

每个子代理获得：

- 全新的 AIAgent 实例（没有父代理的对话历史）
- 自己的 task_id（自己的终端会话、文件操作缓存）
- 受限的工具集（禁止使用 delegate_task、clarify、memory、send_message、execute_code）
- 自己的迭代预算（默认 50 次迭代，可通过 delegation.max_iterations 配置）
- 由目标 + 上下文构建的聚焦系统提示
- 共享的凭证池（子代理可在速率限制时轮换密钥）

子代理在 ThreadPoolExecutor 中运行。父代理会阻塞直到所有子代理完成（最多等待 child_timeout_seconds，默认 600 秒）。父代理只看到最终摘要 —— 绝不会看到中间的工具调用。

## 网络故障处理 —— 两层机制

你的日志显示了来自 xiaomi 的流中断。以下是确切发生的情况：

### 第一层：流级别重试（位于 `_interruptible_streaming_api_call` 中）

在 `agent/chat_completion_helpers.py` 中，流式调用在后台线程中运行，主线程上有一个轮询循环。三个故障检测器：

1. 过时流检测器 —— 如果在 `HERMES_STREAM_STALE_TIMEOUT`（默认 180 秒）内没有新块到达，则终止连接，并让重试循环重新连接。对于大上下文会延长超时（>100k token → 300 秒，>50k → 240 秒）。

2. 工具调用中途流中断 —— 如果流在工具调用 JSON 正在流式传输时中断，并且错误是瞬态的（ReadTimeout、连接重置、SSE "网络连接丢失"），则静默重试，最多 `_max_stream_retries` 次。它会重置所有累加器，重建 OpenAI 客户端连接池，并重新开始。用户会看到 "⚠ xiaomi 流中断（ReadTimeout）在 122.6 秒后 —— 重新连接，重试 2/3"。

3. 交付前流中断 —— 如果在任何 token 交付之前流中断，应用相同的重试逻辑。重试用尽后，错误会传播到外层重试循环。

### 第二层：对话级别重试（位于 `conversation_loop.py`）

当流式层的重试用尽并抛出异常时，外层循环捕获错误：

- 无效/空响应 → 使用抖动退避重试（基础 5 秒，上限 120 秒）
- API 错误（429、500、502、503、504、524）→ 由 `error_classifier.py` 分类，使用退避重试
- 凭证耗尽 → 尝试凭证池轮换，然后回退到备选提供商
- 提供商回退链 → 如果 xiaomi 持续失败且你配置了 `fallback_model`，则会切换

"模型在工具调用后返回空 —— 提示继续" 这条消息是另一条路径：模型完成了工具调用但没有返回文本内容，因此循环注入一条合成的用户消息，提示模型进行总结/继续。

## 当网络变化时会发生什么

对于子代理具体来说：

1. 每个子代理有自己的 API 调用循环。任务中途网络变化意味着所有正在进行的 HTTP 请求都会遇到 ReadTimeout 或连接重置。

2. 每个子代理独立触发流级别重试（这就是为什么你会看到 [subagent-0]、[subagent-1]、[subagent-2] 在大约 122-123 秒同时中断）。

3. 如果网络在重试窗口内（通常是 3 次尝试）恢复，子代理会静默重新连接并继续。它们的对话历史得以保留 —— 重试会使用相同的消息重新发送相同的 API 调用。

4. 如果网络在全部重试中保持断开：
   - 流层抛出错误
   - 对话层使用退避重试
   - 如果仍然失败，尝试回退提供商（如果配置了）
   - 如果全部用尽，子代理返回 `{"failed": True, "error": "..."}`
   - 父代理在委派结果中看到 "failed" 条目并报告它

5. `child_timeout`（默认 600 秒）是硬性上限。一个被网络问题卡住的子代理最终会超时。心跳线程（30 秒间隔）监控子代理进度 —— 如果迭代计数和当前工具在 15 个周期内（450 秒空闲）都没有进展，它会停止触碰父代理的活动，让网关超时触发。

6. 每个子代理在重试时重建自己的 OpenAI 客户端（`agent._replace_primary_openai_client`），从连接池中清除死连接。

## 关键配置旋钮

- `delegation.child_timeout_seconds` —— 每个子代理的硬性超时（默认 600）
- `delegation.max_iterations` —— 每个子代理的迭代上限（默认 50）
- `delegation.max_concurrent_children` —— 并行子代理数（默认 3）
- `HERMES_STREAM_STALE_TIMEOUT` —— 覆盖过时流检测（环境变量）
- 回退模型链 —— 在 `config.yaml` 中，子代理继承父代理的回退链

简短回答：子代理执行期间的网络变化会导致所有子代理并行流中断。每个子代理在流级别（3 次尝试，连接重建）和对话级别（退避 + 凭证轮换 + 回退）独立重试。如果网络在大约 5-10 分钟内恢复，大多数子代理会透明地恢复。如果没有，它们会优雅地失败，父代理会收到错误摘要而非结果。
