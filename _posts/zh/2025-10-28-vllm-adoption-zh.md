---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AI提供商纷纷采用vLLM技术
translated: true
type: note
---

### AI提供商对vLLM的使用情况

vLLM是一款常被推荐用于高效部署开源权重模型的开源推理引擎。然而，其在生产环境中的实际应用情况各有不同。以下是根据现有信息的分析：

| 提供商/模型 | 是否在生产环境中使用vLLM？ | 详细信息 |
| --------------- | --------------------------- | --------- |
| **Claude (Anthropic)** | 否 | Anthropic依赖专有基础设施部署Claude模型。vLLM虽然支持通过兼容Anthropic API的方式进行本地或第三方部署，但无证据表明其内部使用vLLM。 |
| **OpenAI (GPT系列模型)** | 否 | OpenAI采用为大规模服务优化的定制化内部部署系统。vLLM支持OpenAI兼容API的本地推理，但OpenAI的生产环境并未基于vLLM构建。 |
| **Minimax AI** | 否 | MiniMax开源了MiniMax-M1/M2等模型，并因性能优势推荐用户使用vLLM进行部署。其核心生产API未确认使用vLLM，可能采用定制分支或专属方案。 |
| **Kimi (Moonshot AI)** | 否 | Moonshot推荐使用vLLM自部署Kimi-K2模型，其Checkpoint-Engine工具支持与vLLM集成更新权重。但生产环境推理很可能结合SGLang或TensorRT-LLM等引擎采用专有优化方案。 |
| **DeepSeek AI** | 是 | DeepSeek基于vLLM开源了定制化推理引擎，融入了其研究成果的优化技术。该引擎已应用于DeepSeek-V3、R1等模型，并为vLLM项目贡献代码。 |

### 参考资料

- [DeepSeek开源基于vLLM的定制推理引擎](https://www.ainews.com/p/deepseek-open-sources-custom-inference-engine-built-on-vllm)
- [DeepSeek推理引擎的开源之路](https://news.ycombinator.com/item?id=43682088)
- [MiniMax-M1混合架构与vLLM的融合实践](https://blog.vllm.ai/2025/06/30/minimax-m1.html)
- [Kimi K2：开放式智能体系统](https://moonshotai.github.io/Kimi-K2/)
- [OpenAI兼容服务器 - vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [支持Anthropic API `/v1/messages`端点 · 议题 #21313 · vllm-project/vllm](https://github.com/vllm-project/vllm/issues/21313)
