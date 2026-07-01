---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源大语言模型可观测性与评估
translated: true
type: note
---

**问题：** 什么是 Langfuse？

**答案：**

Langfuse 是一个开源的 LLM 可观测性与评估平台。可以把它理解为“LLM 应用的 Datadog”——它在一个地方提供了追踪（tracing）、评估（evals）、提示管理（prompt management）和数据集工具（dataset tooling）。

## 核心原语

```
Trace
 └── Span (generation, retrieval, tool call, etc.)
      ├── input / output
      ├── latency
      ├── token usage + cost
      └── metadata / tags
```

- **Traces** = 一次端到端的 LLM 管道请求
- **Generations** = 一个 trace 中特定的 LLM 调用（跟踪模型、token、成本）
- **Spans** = 其他任何步骤（检索、函数调用、agent 动作）
- **Scores** = 附加到 trace 上的手动或自动化评估标签

## 它实际能做什么

| 特性 | 提供的功能 |
| --- | --- |
| Tracing | 全面了解多步骤 agent/chain 调用 |
| Prompt management | 版本控制的提示、A/B 测试变体 |
| Evals | LLM-as-judge、人工标注、自定义评分 |
| Datasets | 整理输入/输出对用于回归测试 |
| Cost tracking | 按模型、按用户、按功能的花费 |
| Analytics | 延迟 p50/p95、错误率、token 分布 |

## 快速集成（Python）

```python
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

langfuse = Langfuse()  # 从环境变量读取 LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY

@observe()
def my_pipeline(user_query: str) -> str:
    # 自动跟踪为 span
    response = call_llm(user_query)

    # 内联附加评分
    langfuse_context.score_current_observation(
        name="quality",
        value=0.9,
    )
    return response
```

或者使用更低层级的 SDK：

```python
trace = langfuse.trace(name="rag-pipeline", user_id="user-123")
span = trace.span(name="retrieval")
generation = trace.generation(
    name="llm-call",
    model="claude-sonnet-4-6",
    input=[{"role": "user", "content": "..."}],
    output="...",
    usage={"input": 512, "output": 128}
)
```

## 可自托管

```bash
# 大约 5 分钟完成 docker-compose
git clone https://github.com/langfuse/langfuse
cd langfuse
docker compose up
```

Postgres 后端，Next.js 前端。你可以在你的 Ubuntu 工作站上以 `<IP_ADDRESS>` 运行它。

## 为什么它对你的技术栈很重要

考虑到你正在使用 Claude、DeepSeek、MiMo 构建 CLI agent 和银行 AI 系统——Langfuse 让你能够：

- 比较不同模型之间的延迟/成本（Claude vs DeepSeek-v4-flash）
- 在更新 prompt 时捕捉回归问题
- 从生产环境的 trace 中构建评估数据集
- 自动给 agent 轨迹打分（LLM-as-judge）

它与 LangChain、LlamaIndex、OpenAI SDK 以及原生的 `anthropic` SDK 原生集成。对于你的自定义 CLI agent（`ww`、`iclaw`、`zz`），装饰器模式是最快的接入方式。

**参考链接：**

- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [Langfuse Docs](https://langfuse.com/docs)
- [自托管指南](https://langfuse.com/docs/deployment/self-host)
