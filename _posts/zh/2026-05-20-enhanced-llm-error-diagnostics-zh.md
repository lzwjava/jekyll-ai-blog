---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 增强的大语言模型错误诊断
translated: true
type: note
---

好的。以下是变更内容的摘要及原因：

## 变更内容

### `ww/llm/openrouter_client.py` — LLM 客户端层

**问题：** 当 `call_openrouter_api_with_messages` 收到空内容的响应（HTTP 200 但 `message.content` 为 `None` 或 `""`）时，仅静默返回了假值。而当收到非 200 的响应时，错误信息仅显示状态码和原始响应体——未包含模型、代理或令牌的相关上下文。

**修复：** 新增两项改进：

1. **`_check_proxy()`** — 新增辅助函数，检查代理环境变量并测试与代理主机/端口的 TCP 连通性。返回人类可读字符串，例如 `"HTTP_PROXY=http://127.0.0.1:7890 (端口 7890 可达)"` 或 `"UNREACHABLE: ..."`。

2. **空内容检测** — 在 HTTP 200 成功后，解析 JSON 主体并检查 `content` 是否为假值。若是，则抛出异常，包含：模型名称、`max_tokens`、`finish_reason`、HTTP 状态码、代理状态以及完整响应体（前 1000 个字符）。这涵盖了您遇到的情况——模型返回了 `content: null`。

3. **增强的 HTTP 错误** — 现在除状态码和响应体外，还包含模型、`max_tokens` 和代理状态。

### `ww/note/create_note_utils.py` — 调用方层

**问题：** `_call_llm_or_exit` 隐藏了所有细节。原有代码如下：
```python
result = call_openrouter_api(prompt, max_tokens=max_tokens)
if not result:
    print("无法生成标题，最多6个词。退出。")
    sys.exit(1)
```
其中未包含模型名称、提示词预览或异常详情。

**修复：** 包裹在 try/except 中，打印：
- `[error] LLM 调用失败。模型：<model>，max_tokens：<N>`
- `[error] 提示词（前 300 个字符）：<prompt preview>`
- `[error] 异常：<完整详情>`
- 完整调用栈

对于空结果路径（由于 LLM 客户端现在会针对空内容抛出异常，该情况不应再出现）：
- `[error] LLM 返回空结果。模型：<model>，max_tokens：<N>`
- `[error] 提示词（前 300 个字符）：<prompt preview>`

---

现在，如果 `ww note` 在标题生成时再次失败，您将看到**模型名称**、其发送的**提示词**、**HTTP 状态码**、来自 API 的 **finish_reason** 以及**代理连接**状态——诊断问题所需的一切信息。
