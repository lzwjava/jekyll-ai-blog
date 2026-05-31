---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯迭代预算解释
translated: true
type: note
---

以下是Hermes中迭代预算的工作方式：

## 迭代预算 — 工作原理

**核心类**是 `agent/iteration_budget.py` — 一个线程安全的消费/退还计数器（约62行）。每个 `AIAgent` 实例（父代理或子代理）持有一个。

**默认值：**
- 父代理：`max_iterations=90`（可配置）
- 子代理（通过 `delegate_task`）：`delegation.max_iterations`（默认50），独立预算

**循环**位于 `agent/conversation_loop.py` 第796行：

```python
while (api_call_count < agent.max_iterations
       and agent.iteration_budget.remaining > 0) \
      or agent._budget_grace_call:
```

每次迭代 = 一次API调用（该轮中可能包含多次工具调用）。

**每次迭代的预算流程：**

1. **检查中断** — 如果用户发送了 `/stop` 或新消息，立即跳出循环
2. **检查宽限调用** — 如果设置了 `_budget_grace_call`，则消耗该标志并允许最后一次迭代运行（随后无论结果如何都将退出）
3. **`consume()`** — 尝试从剩余次数中减去1。如果已为0，则打印你看到的⚠️警告并跳出循环
4. **执行API调用** — 模型响应，工具执行
5. **在特定条件下退还：**
   - `execute_code` 迭代会被退还（第3403、3883行） — 程序化工具调用不消耗预算
   - 上下文压缩重试会被退还（第3403行） — 使用压缩上下文重试不计入次数
   - Ollama上下文过小错误会被退还（第1100行）

**当预算完全耗尽时**（第4332-4349行）：
- 如果尚无最终响应，Hermes会移除所有工具并进行一次额外的调用，要求模型总结到目前为止所做的工作
- 这就是“宽限调用” — 模型有机会干净地收尾，而不是在工具使用中途直接终止

**你看到的消息：**
```
⚠ 迭代预算已用尽（60/60）— 响应可能不完整
```
这意味着代理达到了 `max_iterations=60`（要么在 config.yaml 中配置，要么由调用者设置）。该响应是预算耗尽后模型的总结尝试。

**关键设计决策：**
- 预算按代理独立计算，而非全局 — 子代理消耗50次迭代不会消耗父代理的预算
- 通过 `threading.Lock` 实现线程安全 — 适用于并发网关会话
- 退还机制防止 `execute_code` 循环耗尽主对话的预算
- 宽限调用确保你总能得到一些响应，即使是被截断的