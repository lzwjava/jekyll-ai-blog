---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI代理的架构限制与并行模式
translated: true
type: note
---

**问题：** AI 代理（如 Hermes 或 Claude Code）在多线程方面的基本限制是什么？克服运行缓慢的正确模式是什么？

**回答：**

是的，你确实触及了一个真正的架构约束。让我来精确地分析一下。

## 为什么代理会串行地慢

AI 代理运行在**顺序的工具调用循环**中：

```
思考 → 调用工具 → 等待 → 观察 → 思考 → 调用工具 → 等待 ...
```

每一步都是阻塞的。代理不能同时发出 10 个 bash 命令——它一次只发出一个，等待结果，然后决定下一个。这是自回归 LLM 的工作方式所固有的：下一个 token 依赖于之前所有的 token，包括工具的结果。

LLM 本身就是串行化的瓶颈。它可以*推理*并行性，但无法*执行*它。

## 摆脱这种局面的两种模式

### 模式 1：代理编写并行代码 → 你来运行它

代理的任务从"完成工作"转变为"编写并行工作器"。你来执行脚本。

```python
# 代理生成这段代码；你运行它
import concurrent.futures
import subprocess

tasks = [
    "总结 file_a.py",
    "总结 file_b.py", 
    "总结 file_c.py",
]

def process(task):
    # 每个任务都调用 LLM API，进行 I/O 等操作
    result = subprocess.run(["python", "worker.py", task], capture_output=True)
    return result.stdout.decode()

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process, tasks))
```

这就是**代码生成逃生舱**——代理只对问题结构进行一次推理，生成并行化代码，然后退出循环。

### 模式 2：多代理编排（并行子代理）

不再是一个代理串行地完成所有工作，而是一个**编排器代理**将任务分发给在并行线程/进程中运行的 N 个**工作器代理**：

```python
import anthropic
import concurrent.futures

client = anthropic.Anthropic()

def run_subagent(task: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": task}]
    )
    return resp.content[0].text

tasks = [
    "分析 auth.py 的安全问题",
    "分析 db.py 的 N+1 查询问题",
    "分析 api.py 的缺失错误处理问题",
]

with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
    futures = {executor.submit(run_subagent, t): t for t in tasks}
    results = {task: f.result() for f, task in 
               [(f, futures[f]) for f in concurrent.futures.as_completed(futures)]}
```

编排器只负责**计划和调度**，工作器并行执行。这正是 Claude Code 的子代理功能正在发展的方向。

## 真实的架构图

```
                    ┌─────────────────┐
                    │    编排器       │  ← 串行 LLM 循环，但很轻量
                    │  (规划任务)     │
                    └────────┬────────┘
                             │ 分发
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         [工作器 1]     [工作器 2]     [工作器 3]
         (并行)         (并行)         (并行)
              │              │              │
              └──────────────┼──────────────┘
                             │ 汇聚
                    ┌────────▼────────┐
                    │    聚合器       │
                    │  (合并结果)     │
                    └─────────────────┘
```

关键见解：**LLM 串行思考是廉价的（token）；I/O 和计算是昂贵的**。将所有昂贵的工作推入并行工作器，让 LLM 仅担任编排器的角色。

## 这对你的 `ww`/`zz` CLI 代理意味着什么

由于你正在构建 CLI 代理，以下是实用的模式：

```python
# 代替代理逐个调用工具：
# agent.run("检查所有50个仓库过时的依赖")

# 你可以这样构建：
def agent_plan(goal: str) -> list[str]:
    """LLM 生成任务分解"""
    ...

def parallel_execute(tasks: list[str], workers: int = 16) -> list[str]:
    """你并行执行，代理从不触及这个循环"""
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(run_task, tasks))

tasks = agent_plan("检查所有50个仓库过时的依赖")
results = parallel_execute(tasks)
summary = agent_summarize(results)  # LLM 只触及规划和总结
```

代理的价值在于**规划和综合**，而不是顺序执行。

## 更深层的限制：上下文窗口作为串行器

即使有并行子代理，还有另一个串行器：**上下文窗口**。当你汇聚结果时，所有内容都必须重新放入一个上下文中进行综合。对于 50 个并行结果，你要么：
- 在汇聚之前对每个结果进行总结（分层归约）
- 使用嵌入 + 检索来代替原始拼接
- 将结果流式传输到结构化存储（数据库/文件），代理来查询

这就是为什么 **MapReduce 是 AI 代理在规模上的正确心智模型**——而不是线程。

## 总结

你是对的——解决办法是：**代理编写并行代码，人类/运行时执行它**。代理永远不应该处于并行 I/O 的热路径中。将 LLM 调用保留用于规划和综合；在它生成或编排的代码中并行化其他所有内容。