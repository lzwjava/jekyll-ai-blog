---
audio: false
generated: true
lang: zh
layout: post
title: 优化AI工具调用的服务器端执行方案
translated: true
type: note
---

是的，传统聊天机器人中工具或函数调用的往返机制（即AI模型生成调用指令，发送至客户端或其他服务，等待执行，然后接收结果）确实会引入延迟，在实时应用中尤为明显。这通常源于网络开销、序列化/反序列化以及多次API往返的需求。您提出的使用lambda函数或设计能接受Python代码在服务端执行的API，是缓解这一问题的巧妙思路——本质上通过将计算任务转移至服务器来最小化客户端与服务器的交互次数。我将从概念层面解析这个问题，探讨可行性、潜在实施方案及权衡因素。

### 为何传统工具调用可能较慢

在许多AI框架中（例如LangChain、OpenAI的函数调用或Anthropic的工具机制）：

- 模型输出结构化的工具调用（如包含函数名和参数的JSON）。
- 客户端（或代理程序）在本地或通过其他API执行该函数。
- 执行结果被附加到对话历史中，并送回模型进行下一步推理。
这种循环每周期可能增加数秒延迟，在复杂任务（如数据分析或多步推理）中延迟会累积。

### 使用Lambda函数或服务端代码执行

您的想法与“无服务器”或“沙盒化”执行模式不谋而合，即AI生成代码（或类lambda片段）直接在托管模型的服务器上运行。这将所有操作保持在同一环境中，将用户所需的API往返可能减少至仅一次。

- **Lambda函数方法**：AWS Lambda、Google Cloud Functions或Azure Functions等服务允许按需执行小型、临时的Python代码片段，无需管理服务器。在AI应用场景中：
  - 聊天机器人后端可以封装AI模型（例如通过OpenAI API）并将Lambda集成为一个工具。
  - 模型生成一个lambda表达式或短函数，在服务端调用。
  - 优点：可扩展、按使用付费、快速启动（冷启动通常<100毫秒）。
  - 缺点：执行时间有限制（例如AWS上最多15分钟），且如果任务跨多次调用，需要处理状态管理。
  - 示例：AI代理可以生成一个lambda来处理数据（如`lambda x: sum(x) if isinstance(x, list) else 0`），将其发送到Lambda端点，并内联获取结果。

- **设计接受并执行Python代码的API**：
  - 是的，这完全可行，并且已在生产系统中存在。关键在于**沙盒化**，以防止任意代码执行带来的安全风险（例如删除文件或进行网络调用）。
  - 工作原理：API端点接收代码片段（作为字符串），在隔离环境中运行，捕获输出/错误，并返回结果。AI模型可以在不离开服务器的情况下迭代生成并“调用”此代码。
  - 优势：
    - 降低延迟：执行发生在与模型相同的数据中心，通常只需毫秒级时间。
    - 支持复杂任务：如数据处理、数学模拟或文件操作，无需外部工具。
    - 有状态会话：某些实现能跨调用维护类似REPL的环境。
  - 安全措施：
    - 使用容器（Docker）、微虚拟机（Firecracker）或受限Python解释器（例如PyPy沙盒或受限全局变量）。
    - 限制资源：CPU/时间配额、无网络访问、模块白名单（例如允许numpy、pandas，但禁止os或subprocess）。
    - 像`restrictedpython`这样的库或E2B/Firecracker等工具提供了现成的沙盒解决方案。

### 实际案例与实现

多个AI平台已不同程度地支持此功能：

- **OpenAI的Assistants API与代码解释器**：允许模型在OpenAI服务器的沙盒环境中编写和运行Python代码。模型可以上传文件、执行代码并根据结果迭代——全部在服务端完成，无需客户端执行。
- **Google的Gemini API代码执行**：提供内置的Python沙盒，模型可在其中生成并迭代运行代码，无需外部调用即可从输出中学习。
- **自定义解决方案**：
  - **E2B沙盒**：用于创建基于云的沙盒（带Jupyter内核）的SDK/API。AI代理可以安全地发送代码运行，非常适合数据分析工具。
  - **Modal沙盒**：在隔离环境中运行AI生成代码的平台，常用于LLM代理。
  - **SandboxAI（开源）**：专门用于在沙盒中执行AI生成Python代码的运行时。
  - 自行构建：可以创建一个FastAPI或Flask服务器，通过POST接收代码，在受限命名空间中使用`exec()`运行，或为每个请求启动一个Docker容器。

代码层面，一个简单的API端点可能如下所示（伪代码，用于示意）：

```python
from fastapi import FastAPI
import restrictedpython  # 用于安全执行

app = FastAPI()

@app.post("/execute")
def execute_code(code: str):
    safe_globals = {"__builtins__": restrictedpython.safe_builtins}  # 受限环境
    try:
        result = {}
        exec(code, safe_globals, result)  # 运行代码
        return {"output": result.get("output")}
    except Exception as e:
        return {"error": str(e)}
```

将其与聊天机器人集成：AI根据用户输入生成代码，内部调用该端点，并整合结果。

### 潜在缺陷与最佳实践

- **安全风险**：任意代码执行是危险的——务必使用沙盒。如果处理不可信用户，应避免使用。
- **成本与可扩展性**：服务端执行会消耗更多计算资源；使用如New Relic等工具进行监控和优化。
- **调试**：如果处理不当，生成代码中的错误可能导致循环。
- **优化替代方案**：
  - 批量工具调用：将多个函数分组到一次服务器往返中处理。
  - 流式处理：使用支持在并行执行工具时流式传输响应的API。
  - 若延迟容忍度高可在客户端执行：对于非敏感任务，在本地执行。
- 若从零开始构建，可先使用LangChain或Vercel的AI SDK等框架，它们支持自定义工具并可配置为服务端运行。

这种方法可以显著提升聊天机器人的速度和能力，尤其是在计算任务方面。如果您正在实施此方案，可以考虑从OpenAI或Gemini的内置功能入手，以快速见效。

[为AI生成代码执行构建沙盒环境](https://anukriti-ranjan.medium.com/building-a-sandboxed-environment-for-ai-generated-code-execution-e1351301268a)
[substratusai/sandboxai: 在隔离沙盒中运行AI生成的代码](https://github.com/substratusai/sandboxai)
[使用TS和GPT-4o通过沙盒代码执行构建AI数据分析师 - E2B](https://e2b.dev/blog/build-ai-data-analyst-with-sandboxed-code-execution-using-typescript-and-gpt-4o)
[代码执行 | Gemini API](https://ai.google.dev/gemini-api/docs/code-execution)
[助手代码解释器 - OpenAI API](https://platform.openai.com/docs/assistants/tools/code-interpreter)
[Modal沙盒](https://modal.com/use-cases/sandboxes)
[使用New Relic AI监控优化AI聊天机器人性能](https://newrelic.com/blog/how-to-relic/optimizing-ai-chatbot-performance)
