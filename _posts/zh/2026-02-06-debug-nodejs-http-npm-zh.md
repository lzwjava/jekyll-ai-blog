---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 调试 Node.js HTTP 和 NPM
translated: true
type: note
---

我将帮助你调试 Node.js 中的 HTTP/HTTPS 请求以及 NPM 操作。

## NODE_DEBUG for HTTP/HTTPS

`NODE_DEBUG` 环境变量可以启用 Node.js 内部的 debugging 输出。对于 HTTP/HTTPS 请求：

```bash
# 调试 HTTP 请求
NODE_DEBUG=http node your-script.js

# 调试 HTTPS 请求
NODE_DEBUG=https node your-script.js

# 同时调试两者
NODE_DEBUG=http,https node your-script.js
```

这将向你展示：

- Socket 连接与复用
- 正在发送的 Request headers
- Response status codes
- Keep-alive 行为
- 内部状态转换

**示例输出** 包含如下细节：

```
HTTP 12345: call onSocket 0 0
HTTP 12345: createConnection localhost:3000 {...}
HTTP 12345: outgoing message end
```

## NPM Debug Logging

对于 NPM，你可以控制 logging 的详细程度（verbosity）来查看 request headers 和详细的操作：

```bash
# 最大详细程度（显示所有 HTTP 请求、headers 等）
npm install --loglevel silly

# 或者进行全局设置
npm config set loglevel silly

# 然后运行任何 npm 命令
npm install
```

**使用 npm debug 标志的替代方案：**

```bash
npm install --verbose
# 或者
npm install -d  # debug 模式
npm install -dd # 更加详细
```

**若要查看包含 headers 的实际 HTTP 流量**，请结合使用 NODE_DEBUG：

```bash
NODE_DEBUG=http,https npm install --loglevel silly
```

这将向你展示：

- 正在联系的 Registry URLs
- Request/response headers
- TLS/SSL handshakes
- Package resolution 详情
- Cache 操作

**提示**：如果输出内容过多，可以将其通过管道传输到文件中：

```bash
NODE_DEBUG=http,https npm install --loglevel silly 2>&1 | tee npm-debug.log
```

你可以使用以下命令将 npm logging 重置为正常状态：

```bash
npm config set loglevel warn
```
