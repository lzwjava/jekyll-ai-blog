---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 详细记录 Git HTTPS 请求日志
translated: true
type: note
---

Question: 在运行 git pull --rebase 时，如何记录 HTTP 和 HTTPS 请求？

Answer:

你提供的示例输出显示的是 **SSH** 连接（`Authenticated to github.com ([20.205.243.166]:22) using "publickey"`），而**不是** HTTP/HTTPS。当你的 remote URL 格式为 `git@github.com:...` 时，GitHub 默认使用 SSH。

要真正查看 HTTP/HTTPS 流量，你需要：

1. 确保你使用的是 HTTPS remote（通常在看到密码/PAT 提示时使用）
2. 启用 Git 内置的 curl（Git 用于处理 http/https 的工具）详细日志记录

### 检查当前的 remote URL

```bash
git remote -v
```

- 如果你看到 `git@github.com:...` → 你正在使用 **SSH**
- 如果你看到 `https://github.com/...` → 你正在使用 **HTTPS**

### 切换到 HTTPS（如果你想记录 HTTP/HTTPS 请求）

```bash
git remote set-url origin https://github.com/owner/repo.git
# 或者针对带 token 的 GitHub：https://username:ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/owner/repo.git
```

### 记录 HTTP/HTTPS 请求（使用 HTTPS remote 时）

在 git 命令前使用一个或多个环境变量：

```bash
# 最常用且最有效的组合 – 显示完整的 curl 详细输出（headers, TLS handshake 等）
GIT_CURL_VERBOSE=1 git pull --rebase

# 更详尽的信息（packet 层级 + curl + 常规 trace）
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_CURL_VERBOSE=1 git pull --rebase

# 保存到文件（非常推荐）
GIT_CURL_VERBOSE=1 git pull --rebase 2>&1 | tee git-http.log

# 或者最大程度的调试
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_TRACE_CURL=1 GIT_CURL_VERBOSE=1 git pull --rebase 2>&1 | tee git-debug.log
```

### 每个变量的作用

- `GIT_CURL_VERBOSE=1` → 显示所有 curl 详细消息（类似于 `curl -v`），包括：
  - 所有的 request/response headers
  - TLS 协商过程
  - 重定向（Redirects）
  - 已发送/接收的数据大小
- `GIT_TRACE=1` → 显示运行了哪些 git 内部命令
- `GIT_TRACE_PACKET=1` → 显示底层的 smart-http 协议包（sideband, flush 等）
- `GIT_TRACE_CURL=1` → (Git ≥ 2.9) 提供更多 curl 相关的 trace 信息

### 快速单行命令示例

```bash
# 快速查看 headers 和 TLS
GIT_CURL_VERBOSE=1 git pull --rebase

# 详细日志并保存到文件
GIT_TRACE=1 GIT_TRACE_PACKET=1 GIT_CURL_VERBOSE=1 git fetch --verbose 2>&1 | tee ~/git-network.log
```

### 如果你想记录 SSH 替代

对于 SSH 协议的日志记录：

```bash
GIT_SSH_COMMAND="ssh -vvv" git pull --rebase
```

或者更详细的级别：

```bash
GIT_SSH_COMMAND="ssh -vvvv" git pull --rebase 2>&1 | tee ssh-debug.log
```

当你的 remote 使用 `https://` 时，请使用 `GIT_CURL_VERBOSE=1` —— 这是查看 Git 发出的 HTTP 和 HTTPS 请求的标准方式。

References:

- [Git Internals - Environment Variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
- [GitLab Docs - Troubleshooting Git (debug HTTPS)](https://docs.gitlab.com/topics/git/troubleshooting_git)
- [Stack Overflow - Debug git/git-shell problems (GIT_CURL_VERBOSE)](https://stackoverflow.com/questions/6178401/how-can-i-debug-git-git-shell-related-problems)
