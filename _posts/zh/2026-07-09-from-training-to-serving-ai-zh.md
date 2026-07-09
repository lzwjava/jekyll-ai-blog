---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从训练到AI服务
translated: true
type: note
---

问题：你成功在 RunPod 上部署了 SGLang Serverless 端点，而 vLLM 无法正常工作。这是一个好的方向吗？对吗？

答案：

是的。根据你发布的内容，你的 **SGLang Serverless 部署是正常工作的**。

证据：

*   你的请求状态为 `"COMPLETED"`。
*   一个 worker 处理了该请求：
    *   `"workerId": "grr2baqhs9xjvr"`
*   模型生成了有效的 OpenAI 兼容响应：
    ```json
    {
      "object": "chat.completion",
      "model": "HuggingFaceTB/SmolLM2-1.7B-Instruct",
      "choices": [...]
    }
    ```
*   端点返回了使用统计信息（`prompt_tokens`, `completion_tokens` 等），说明推理栈完整地完成了端到端处理。

所以你的部署流水线是：

```
Client
    ↓
RunPod Serverless Endpoint
    ↓
SGLang Worker
    ↓
HF Model
    ↓
OpenAI-compatible JSON
```

这正是你想要的结果。

至于 **vLLM 与 SGLang 的对比**，2026年中的格局大致如下：

*   **vLLM**
    *   优秀的通用推理引擎
    *   非常成熟的 OpenAI 兼容服务器
    *   庞大的生态系统
    *   强大的连续批处理能力
*   **SGLang**
    *   针对代理型工作负载进行了优化
    *   更快的结构化解码
    *   对推理模型和工具使用的支持更好
    *   被更新的模型版本越来越广泛地采用

许多近期开放权重的推理模型（包括腾讯混元的几个版本以及其他前沿开放模型）都提供一流的 SGLang 支持，因此你发现 SGLang 是这些模型更顺畅的路径并不奇怪。

由于你正在构建 AI 基础设施和智能体，学习 **两者** 都很有价值：

```
vLLM
    ↓
通用推理
OpenAI API
批量服务

SGLang
    ↓
推理
工具调用
智能体
结构化生成
```

从你最近的对话来看，你已经经历了整个部署周期：

*   ✅ 从头训练了一个 GPT 模型
*   ✅ 尝试了 vLLM
*   ✅ 在 RunPod 上部署了 SGLang Serverless 端点
*   ✅ 暴露了一个 OpenAI 兼容的 API 端点

这意味着你正在从模型训练向 **LLM 服务基础设施** 迈进，这是栈中的另一个核心部分。

接下来自然的步骤是对你的端点进行基准测试：

```bash
# 延迟
time curl ...

# 吞吐量
hey -n 1000 -c 20 ...

# 或
wrk

# 流式延迟
curl -N ...
```

测量指标如：

*   首个 token 时间 (TTFT)
*   tokens/sec
*   并发请求吞吐量
*   冷启动时间
*   每 100 万输出 token 的成本

这些数值比仅仅验证端点有响应更具信息量。