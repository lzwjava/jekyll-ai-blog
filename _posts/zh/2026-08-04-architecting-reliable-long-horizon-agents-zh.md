---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建可靠的长周期智能体
translated: true
type: note
---

问题：如何设计一个代理（agent），使其能够可靠地处理长时间运行/长时间跨度任务（多次回合、工具调用、数小时的工作），而不会因为上下文限制而崩溃？

答案：

真正起作用的有四种机制。其他都是胶水代码。

**1. 外部化状态——不要把上下文窗口当作数据库**

上下文是缓存，不是存储。将计划+进度写入磁盘，恢复时重新读取。这使任务在崩溃、压缩甚至进程重启后可以*恢复*。

```python
# state.py — 唯一的真相来源
import json, os

STATE_FILE = "task_state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {"todos": [], "done": [], "notes": [], "cursor": 0}

def save_state(s):
    json.dump(s, open(STATE_FILE, "w"), indent=2)
```

代理的系统提示应始终指示："在执行任何操作之前，读取 `task_state.json`。完成每个子任务后，更新它。" 这实际上就是 Claude Code 的 TODO 列表的工作方式——它不是 UI 糖，而是状态机。

**2. 压缩（Compaction）——尽早触发，而不是等到极限**

Anthropic 自身的指导：简单循环在约 5–20k token 时触发摘要，复杂循环在 50–100k token 时触发——而不是当你即将撑爆上下文窗口时。压缩应在某些工作负载约 5–20k token 时触发，对于更复杂的任务则在 50–100k token 时触发。等到极限时再进行摘要，意味着你会在恐慌中摘要，质量下降。

```python
def maybe_compact(messages, model_call, threshold_tokens=15000):
    if estimate_tokens(messages) < threshold_tokens:
        return messages
    summary_prompt = (
        "总结到目前为止的轨迹：已做出的决策、触及的文件、"
        "未解决的问题、下一步行动。要密集，这将替代完整历史。"
    )
    summary = model_call(messages + [{"role": "user", "content": summary_prompt}])
    return [
        {"role": "system", "content": messages[0]["content"]},
        {"role": "assistant", "content": f"[压缩的历史]\n{summary}"},
    ]
```

需要了解的关键失败模式：**上下文腐朽（context rot）**——随着 token 增长，性能下降，与是否接近极限无关。Chroma 的实证研究表明，在 Claude Sonnet 4、GPT-4.1、Qwen3-32B 和 Gemini 2.5 Flash 上，随着输入 token 数量增加，性能都会下降——即使在故意控制的任务上也是如此。100 万 token 窗口并不能解决这个问题——它只是把悬崖移动了。百万级 token 窗口并不能解决问题；它们只是把问题转移了。

**3. 子代理分解（Sub-agent decomposition）——为每个子任务隔离上下文**

不要使用一个不断累积所有内容的滚动上下文，而是为每个子任务生成一个子进程/子代理，该子代理获得一个范围限定的提示，并返回简短的结果。这是“任务分解”范式与单代理累积范式的对比。单代理策略累积整个轨迹，而任务分解方法则将工作拆分为返回更短结果的子代理。

```bash
# orchestrator.sh — 用于 Claude Code 的 Task 工具的模式，也适用于 CLI 代理
for subtask in $(jq -r '.todos[]' task_state.json); do
    result=$(zz agent --isolated --prompt "$subtask" --max-turns 20)
    jq --arg r "$result" '.done += [$r]' task_state.json > tmp && mv tmp task_state.json
done
```

每个子代理调用都是一个全新的上下文——没有来自无关早期子任务的累积残留。只有提炼后的结果返回给协调器。

**4. 结构化驱逐（Structured eviction）而非简单截断**

不要丢弃最旧的消息。按类型标记上下文（计划/工具输出/推理轨迹/决策），并按优先级+依赖关系驱逐，而不是按时间顺序。代理在其工作过程中，将轨迹标注为带类型、依赖关联的片段，当超过 token 预算时，一个确定性的、无需 LLM 的策略在该结构内按优先级顺序驱逐内容。原始工具输出（巨大的日志转储、已应用的文件内容）最先被丢弃——决策和未解决的问题最后被保留。

**如果你在决定是否值得构建这些功能，具体数据如下**：将上下文编辑（压缩）与持久记忆工具结合，能获得比单独使用压缩高出显著的效果。Anthropic 的内部评估显示，仅上下文编辑就能带来 29% 的性能提升，而将其与记忆工具结合可达到 39%。因此：状态文件（记忆）+ 压缩，而不是两者择一。

针对你的 `zz`/`iclaw` 堆栈具体而言：这映射为（a）一个 `task_state.json`，代理每轮都会读写它；（b）一个压缩钩子，在每次 LLM 调用之前检查 token 计数并触发；（c）对于任何会污染主轨迹的操作（大型文件读取、探索性搜索），使用 `--isolated` 子代理生成。

参考文献：

- [Context Engineering: Agent Reliability Playbook 2026](https://www.digitalapplied.com/blog/context-engineering-agent-reliability-playbook-2026)
- [Beyond Compaction: Structured Context Eviction for Long-Horizon Agents](https://arxiv.org/pdf/2606.11213)
- [Slipstream: Trajectory-Grounded Compaction Validation for Long-Horizon Agents](https://arxiv.org/pdf/2605.08580)
- [Self-Compacting Language Model Agents](https://arxiv.org/pdf/2606.23525)
