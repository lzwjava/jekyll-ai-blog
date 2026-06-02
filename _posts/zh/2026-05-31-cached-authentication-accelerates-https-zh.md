---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缓存认证加速HTTPS
translated: true
type: note
---

好的，这是从源代码得出的深入回答。

声称"HTTPS + GCM 比 SSH 更快"并非指协议在网络层面的速度，而是指 GCM 实现的**凭证缓存架构**。让我追踪实际的代码路径。

HTTPS + GCM 凭证流程（根据代码）：

1. Git 需要凭证 → 启动 `git-credential-manager get`
2. GCM 读取标准输入的键值对（protocol=https, host=github.com, ...）
3. HostProviderRegistry 按优先级选择提供程序：
   GitHub → GitLab → Bitbucket → AzureDevOps（Normal）
   Generic（Low — 回退）
4. 提供程序调用 GetCredentialAsync(input)
5. **快速路径** — 查看 GitHubHostProvider.cs 第 175-176 行：

   credential = _context.CredentialStore.Get(service, userName);

   以及 GenericHostProvider.cs 第 73 行：

   ICredential credential = _context.CredentialStore.Get(service, input.UserName);

   这是本地操作系统调用 — macOS 钥匙串、Windows 凭据管理器或 Linux libsecret。零网络开销。返回时间以微秒计。

6. 找到凭证 → 将用户名/密码写入标准输出 → Git 使用该凭证。GCM 进程退出。

关键点：**GCM 仅在第一次执行昂贵的 OAuth/浏览器/设备码流程**（在 GenerateCredentialAsync 中）。之后，令牌/PAT 被缓存在操作系统凭据存储中，每次后续的 `git push`/`pull`/`fetch` 都会走快速路径（步骤 5）。

比较网络路径：

SSH：git → ssh → ssh-agent → TCP → ncat → SOCKS5 → mihomo → 互联网
（每个操作：密钥交换、代理签名、连接建立）

HTTPS + GCM（已缓存）：
git → 启动 git-credential-manager → Keychain.Get() → 标准输出
→ git 使用令牌通过 HTTPS → mihomo → 互联网

HTTPS + GCM（冷启动/首次）：
git → GCM → 浏览器 OAuth → 令牌 → Keychain.Store()
（首次比 SSH 慢，但仅发生一次）

GCM 节省时间的地方：

1. 凭证检索：操作系统钥匙串查找约 0.1 毫秒，而 SSH 代理套接字往返 + 密钥签名（约 1-5 毫秒）在每个操作中都会发生。

2. 无 SSH 握手开销：SSH 每次连接需要密钥交换（DH）、签名验证和通道建立。HTTPS 将令牌作为 Bearer 认证头重用——只是一个 HTTP 头，无需密码学协商。

3. 连接复用：HTTPS 连接可以复用 HTTP/2。每个 SSH 会话都是一个独立的 TCP 连接，包含完整的握手过程。

4. 进程数量：GCM 启动一次，读取标准输入，写入标准输出，然后退出。SSH 需要持久的 ssh-agent + ssh 进程 + ncat 隧道。

但在你的设置中（中国 → 通过 mihomo 访问 GitHub），真正的速度差异并非在于协议开销，而是在于你的代理路径。SSH 和 HTTPS 都通过 127.0.0.1:7890 的 mihomo 代理。

GCM 的优势在于它积极缓存令牌。首次认证后，Git 无需重新认证——它只需将缓存的令牌作为 Authorization 头发送。而 SSH 在每个新连接上都会重新认证（密钥交换）。

令牌生命周期（来自 GenericHostProvider 第 291-314 行）：
OAuth 令牌的刷新令牌缓存在凭据存储中，服务名称为 "refresh_token.{host}"。
因此，即使是令牌刷新也只需本地存储查找 + 一次 HTTP 调用，而不是完整的交互式认证流程。

总结：GCM 通过将认证转化为首次登录后的本地缓存查找，使 HTTPS 变得快速。SSH 没有等效的缓存机制——它在每次连接时都进行密码学认证。当你的网络路径具有高延迟时（例如通过洛杉矶代理），差异会累积放大。

一个注意事项：如果你的 SSH 密钥在 ssh-agent 中，并且使用了 SSH 连接多路复用（ControlMaster），那么每次连接的开销会大幅降低。但这需要显式配置——而 GCM 的缓存开箱即用。
