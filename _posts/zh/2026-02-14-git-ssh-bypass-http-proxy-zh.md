---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Git SSH 完全绕过 HTTP 代理
translated: true
type: note
---

Question: 当使用 SSH 运行 `GIT_SSH_COMMAND="ssh -vvv" git pull --rebase` 时，它会绕过系统的 HTTP 和 HTTPS 代理设置（如 `export HTTP_PROXY` 和 macOS 系统设置中的网络代理）吗？

Answer: 

**是的，它会完全绕过这些设置。**

### 为什么会这样

- Git 有两种完全不同的传输协议：
  - **HTTPS** 协议（`https://github.com/...` URLs）→ Git 内部使用 libcurl → 遵循标准的 proxy 环境变量（`http_proxy`, `https_proxy`, `HTTP_PROXY`, `HTTPS_PROXY`, `all_proxy`）以及 macOS 系统网络代理设置（curl 通常通过 macOS API 或环境变量来遵循这些设置）。
  - **SSH** 协议（`git@github.com:...` 或 `ssh://git@github.com/...` URLs）→ Git 只是简单地运行 `ssh` 命令（或者是通过 `GIT_SSH_COMMAND` / `core.sshCommand` 指定的命令）→ **SSH client 永远不会查看 HTTP/HTTPS proxy 变量**。

`ssh` (OpenSSH) **不会**为了自己的连接去读取或使用 `HTTP_PROXY`、`HTTPS_PROXY` 或 macOS 系统 HTTP/HTTPS 代理设置。这些变量仅对支持 HTTP/HTTPS 协议的 client（如 curl, git over https, wget 等）有意义。

### 总结表

| Git 使用的协议 | 是否使用 HTTP_PROXY / HTTPS_PROXY? | 是否使用 macOS 系统设置中的 HTTP 代理? | 控制方式 |
|----------------------|--------------------------------|----------------------------------------|------------------------|
| HTTPS                | 是                            | 是 (通过 curl / 系统集成)    | 环境变量 + git config http.proxy |
| SSH                  | 否                             | 否                                     | ssh config (~/.ssh/config) + GIT_SSH_COMMAND |

### 如何让 SSH 通过代理（如果需要）

你必须手动配置 **SSH client** 本身来使用代理 —— 常见方法如下：

1. **HTTP CONNECT proxy**（大多数公司级 HTTP 代理）
   ```bash
   # 在 ~/.ssh/config 中
   Host github.com
       ProxyCommand connect -H proxy.example.com:8080 %h %p
   ```
   （需要 `connect` 工具或类似工具 —— 可通过 brew install connect 安装）

2. **SOCKS5 proxy**（常用于 Shadowsocks, v2ray, Clash 等工具）
   ```bash
   # 在 ~/.ssh/config 中
   Host github.com
       ProxyCommand nc -x 127.0.0.1:1080 %h %p
   ```
   或者
   ```bash
   GIT_SSH_COMMAND="ssh -o ProxyCommand='nc -x 127.0.0.1:1080 %h %p'" git pull --rebase
   ```

3. **Jump host / bastion** (ProxyJump)
   ```bash
   GIT_SSH_COMMAND="ssh -J user@bastion.example.com" git pull --rebase
   ```

4. **通过 HTTPS 端口 443 使用 SSH**（GitHub 支持此操作）
   - 将 remote 修改为 `ssh://git@ssh.github.com:443/user/repo.git`
   - 虽然使用了 443 端口，但这仍然是 SSH 协议（不是 HTTP），不过对于某些防火墙可能有绕过作用，但**它仍然不会使用 HTTP_PROXY**。

### 快速检查你正在使用的协议

```bash
git remote -v
```

- `git@github.com:...` 或 `ssh://` → SSH（忽略 HTTP 代理）
- `https://github.com/...` → HTTPS（使用 HTTP/HTTPS 代理）

因此，当你运行 `GIT_SSH_COMMAND="ssh -vvv" git pull --rebase` 并看到 SSH 身份验证 / port 22 流量时，你使用的是 SSH 协议 —— HTTP/HTTPS 代理设置（包括 macOS 系统设置）会被完全忽略。

References:  

- [Git - Environment Variables](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables)
- [Configure Git to use a proxy (HTTPS or SSH+GIT)](https://gist.github.com/ozbillwang/005bd1dfc597a2f3a00148834ad3e551)
- [Use Proxy for Git/GitHub](https://gist.github.com/coin8086/7228b177221f6db913933021ac33bb92)
- [How do I pull from a Git repository through an HTTP proxy?](https://stackoverflow.com/questions/128035/how-do-i-pull-from-a-git-repository-through-an-http-proxy)