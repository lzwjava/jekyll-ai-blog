---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Node.js中的HTTP和HTTPS日志记录
translated: true
type: note
---

**问题：** 给我关于记录 HTTP 和 HTTPS 日志的 NODE 选项命令，与 `npm install --verbose` 相关。

**答案：**

要启用 Node.js 的详细 **HTTP** 和 **HTTPS** 请求日志（包括 `npm install` 期间触发的请求，例如从 registry 获取包），请使用内置的 `NODE_DEBUG` 环境变量。

### 记录 HTTP/HTTPS 日志的主要命令
在运行 npm 命令之前执行以下命令（在 Unix-like 系统如 Linux/macOS 上）：

```bash
NODE_DEBUG=http,https npm install --verbose
```

在 Windows 上（命令提示符）：

```cmd
set NODE_DEBUG=http,https && npm install --verbose
```

在 Windows 上（PowerShell）：

```powershell
$env:NODE_DEBUG="http,https"; npm install --verbose
```

### 作用说明
- `NODE_DEBUG=http` → 记录所有输出/输入的 HTTP 客户端和服务器活动（请求、响应、头信息、套接字等）。
- `NODE_DEBUG=https` → 记录 HTTPS 特定活动（TLS 握手、安全连接）。
- 用逗号组合两者（`http,https`）可同时启用。
- `--verbose`（或 `--loglevel verbose`）会添加额外的 npm 层级详情，包括在 "http" 日志级别下的一些 HTTP 获取信息。

你也可以包含更多模块以进行更广泛的调试：

```bash
NODE_DEBUG=http,https,http2,tls npm install --verbose
```

### 其他有用的 NODE_OPTIONS
你可以通过 `NODE_OPTIONS` 环境变量传递 Node.js 标志（npm 也支持将其用于生命周期脚本）：

```bash
NODE_DEBUG=http,https NODE_OPTIONS="--trace-warnings" npm install --verbose
```

或与 npm 自身的 HTTP 日志级别结合：

```bash
NODE_DEBUG=http,https npm install --loglevel=http --verbose
```

### 提示
- 输出可能非常冗长——如有需要可重定向至文件：
  `NODE_DEBUG=http,https npm install --verbose > npm-http.log 2>&1`
- 这些日志有助于调试网络问题，如 registry 连接、代理问题、SSL 错误或下载缓慢。
- `NODE_DEBUG` 适用于任何 Node.js 进程，不仅仅是 npm。

这是标准的内置方法，无需安装额外包即可获取低层级的 HTTP/HTTPS 日志。

**参考：**
- https://nodejs.org/api/cli.html （Node.js 命令行选项和环境变量）
- https://docs.npmjs.com/cli/v9/using-npm/logging （npm 日志级别，包括 "http"）
