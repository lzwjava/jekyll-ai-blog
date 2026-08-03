---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang在五种输入长度下的测试
translated: true
type: note
---

完成。新增了 `ww sglang test` 命令，可对运行中的 SGLang 服务器（`Qwen/Qwen2.5-0.5B-Instruct`，端口 30010）进行五种输入长度的测试。

**变更内容：**

- **`ww/sglang/test.py`**（新增）— 以流式方式完成聊天补全，输入长度从约 11 到约 4,700 token；报告每个案例的 TTFT、总延迟、输出 token 数、吞吐量（tok/s）、结束原因及响应片段。利用 SGLang 的 `/v1/tokenize` 扩展获取精确 token 计数（流式分块省略了 `usage`），并在开始时进行非流式探测及健康/模型列表查询。选项：`--url`、`--port`、`--model`、`--max-tokens`、`--no-stream`、`--timeout`。
- **`ww/main.py`** — 添加了 `sglang` 命令组路由及 `_print_help()` 中的帮助文本。
- **`completions/_ww`** — 注册了 `sglang` 顶级命令和用于 Tab 补全的 `sglang_cmds`。

**针对你运行中的服务器进行的示例测试：**

```
case           input     TTFT    total    out    tok/s  finish  response
--------------------------------------------------------------------------------------------
tiny            11t      10ms      37ms     9    240.4  stop      'Hello! How can I assist you today?'
short           73t      10ms      82ms    25    303.2  stop      'The text discusses the beauty and complexity of '
medium         306t       9ms      88ms    27    306.7  stop      'The text describes the beauty of mathematics in '
long         1,189t      10ms     203ms    67    329.5  stop      'Based on the content of the text, here are three'
huge         4,711t      14ms      84ms    24    286.4  stop      'The quick brown fox jumps over the lazy dog whil'

检查：
  [ OK ] tiny     11 in -> 9 out, finish=stop
  ...（全部 5 个 OK）

最差 TTFT：huge（4,711 输入 token）= 14ms
```

同时验证了 `--help`、错误端口处理及语法。用法：`ww sglang test`（默认），`ww sglang test --port 30011`，`ww sglang test --url http://host:30010 --max-tokens 256`。