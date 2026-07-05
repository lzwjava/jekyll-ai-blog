---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 区分SGLang和vLLM后端
translated: true
type: note
---

好问题——是的，你可以通过 OpenAI 兼容的 API 来区分 SGLang 和 vLLM，并测量前缀缓存的行为。以下是实用的分析：

1. 如何通过 API 响应区分 SGLang 和 vLLM

两者都暴露 `/v1/chat/completions`，但存在可检测的差异：

| 维度 | vLLM | SGLang |
| ------ | ------ | -------- |
| id 字段 | "chatcmpl-<UUID>" | 通常是一个裸的32位十六进制字符串（无 chatcmpl- 前缀） |
| 流式推理 | delta.reasoning_content（某些版本） | delta.reasoning（深度思考模型）；SGLang 也在第一个 chunk 中使用 reasoning_content: null |
| 服务器头 | Server: uvicorn（典型） | 有时为 Server: sglang 或缺失；检查 /health 或 /v1/models 响应结构 |
| 原生 /generate 端点 | {"prompt": "...", "sampling_params": {...}} 嵌套结构 | {"text": "...", "sampling_params": {...}} 且带有 return_logprob 等 |

快速启发式判断：发送一个流式请求，检查 `response.json()["id"]`。如果它不以 `chatcmpl-` 开头，则很可能是 SGLang。

2. 测试前缀缓存——你的思路是正确的

你的方案是标准做法：

1. **发送请求 A**——长共享系统提示 + 唯一后缀 → 测量 TTFT 和总延迟（冷启动，无缓存）。
2. **发送请求 B**——相同长共享前缀 + 不同后缀 → 再次测量 TTFT。
3. **比较**：
   - 缓存命中 → 请求 B 的 TTFT 大幅下降（只需计算差异后缀部分）。
   - 无缓存/未命中 → 请求 B 的 TTFT ≈ 请求 A 的 TTFT。

SGLang 的 RadixAttention 在 token 级别匹配；vLLM 的 APC（使用 `--enable-prefix-caching`）在块/页面级别匹配（通常为16 token 块），因此部分块的尾部会被重新计算。

最小 Python 测试示例：

```python
from openai import OpenAI
import time

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")

SHARED_PREFIX = "你是一个资深Python工程师，请严格按下方要求作答。\n\n" * 200  # 长共享部分
SUFFIX_A = "问题A：打印1到10。"
SUFFIX_B = "问题B：打印斐波那契数列前10项。"

def ttft(messages):
    t0 = time.perf_counter()
    stream = client.chat.completions.create(
        model="your-model",
        messages=messages,
        max_tokens=64,
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            return time.perf_counter() - t0
    return None

print("请求1（冷启动）:", ttft([{"role":"user","content": SHARED_PREFIX + SUFFIX_A}]))
print("请求2（缓存前缀）:", ttft([{"role":"user","content": SHARED_PREFIX + SUFFIX_B}]))
```

• vLLM 需要在启动时使用 `--enable-prefix-caching` 来展示此效果。
• SGLang 的 RadixAttention 默认开启。

3. 用户体验中的表现

| 维度 | SGLang（RadixAttention） | vLLM（APC，块级别） |
| ------ | -------------------------- | ---------------------- |
| 多轮对话/共享系统提示 | 第2轮及以后 TTFT 几乎即时，命中率高 | 如果前缀对齐到块边界则 TTFT 改善，但不够激进 |
| RAG/模板提示 | 跨用户使用相同模板时复用效果极佳 | 取决于块对齐；可能重新计算尾部 token |
| 共享前缀下的吞吐量 | 通常更高（冗余 KV 计算更少） | 不错，但部分重叠场景缓存效率通常较低 |
| OpenAI API 保真度 | 在某些边缘字段略逊于 vLLM（如旧版 stream_options.include_usage） | 非常接近官方 OpenAI 规范 |

4. 服务端确认（如果你控制部署）

• SGLang 服务器日志会在 RadixAttention 命中时打印 `KV Cache hit for prefix length XXX`。
• vLLM 使用 `--enable-prefix-caching` 时，会在其 Prometheus 指标中记录前缀缓存命中统计（`vllm:prefix_cache_hit`）。

**总结：** 你基于延迟的前缀缓存测试是正确的方法。要识别后端，请检查流式响应中的 `id` 格式以及任何 `reasoning`/`reasoning_content` delta 字段。如果你需要基于 curl 的版本或更正式的基准测试脚本，请告诉我！
