---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 推理后端检测工具
translated: true
type: note
---

已完成。以下是构建的内容：

**`ww inference test`** — SGLang 与 vLLM 后端检测

**检测逻辑**（基于你提供的信息）：

| 信号 | SGLang | vLLM |
| -------- | -------- | ------ |
| `id` 字段 | 纯32字符十六进制字符串 | 带 `chatcmpl-...` 前缀 |
| 流式 `delta` | 包含 `reasoning` 键（深度思考模型） | 包含 `reasoning_content` 键 |
| 服务器响应头 | `sglang` 或缺失 | 通常为 `uvicorn` |

**已运行的测试：**

1. **流式检测** — 检查第一个数据块的 `id`、`delta` 键以及 TTFT
2. **服务器响应头** — 检查 `Server` 和 `X-Powered-By` 头部
3. **前缀缓存** — 两次请求共享200行前缀，比较 TTFT 下降量

**使用方法：**

```
ww inference test                          # 默认：tencent/hy3-preview
ww inference test --no-prefix-cache        # 跳过前缀缓存测试
ww inference test --model openai/gpt-4o-mini
```

代码已提交 (153a1b4)。从终端运行，确保 `OPENROUTER_API_KEY` 可用，即可获取真实结果。
