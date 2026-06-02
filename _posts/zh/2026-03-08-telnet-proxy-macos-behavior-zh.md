---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Telnet 代理与 macOS 行为
translated: true
type: note
---

**问题：** Telnet 如何工作？它是否应用 macOS 上的 HTTP 或 HTTPS 代理设置？与 `ping`（绕过代理）相比，如果配置了代理，`telnet` 是否会通过代理？

---

**回答：**

## Telnet 如何工作

Telnet 是一种客户端-服务器应用程序协议，提供对局域网或 Internet 上远程系统虚拟终端的访问。它是一种用于双向 8 位通信的协议。

Telnet 使用 TCP 作为其底层传输协议。客户端向服务器发送命令，服务器以输出响应，允许用户与远程系统的命令行界面进行交互。它主要使用端口 23 进行通信。

以下是连接流程的逐步说明：

1. **您输入：** `telnet hostname port`
2. Telnet 客户端将字符转换为称为 Network Virtual Terminal (NVT) 字符的通用字符集，并将其传递到本地 TCP/IP 协议栈。这些 NVT 字符通过 Internet 传输，到达远程计算机的 TCP/IP 栈。
3. 远程 Telnet 服务器将这些字符转换为远程计算机可理解的格式。远程操作系统从伪终端驱动程序接收它们，并将其传递给适当的应用程序。

**关键特性：**

- Telnet 既未加密也不安全。因为它是一种纯文本协议，网络上的任何人均可访问 Telnet 会话期间输入的用户名、密码和其他私人信息。
- Telnet 客户端是企业应用程序管理员最有用的工具之一。因为 Telnet 是一种非常简单的协议，该客户端可用于创建与远程 Telnet 服务器连接以外的其他用途——特别是用于测试一般的 TCP 连接性。

---

## `telnet` 是否使用 macOS HTTP/HTTPS 代理设置？

**否，`telnet` 不会自动使用 macOS HTTP 或 HTTPS 代理设置。**

原因如下：

**macOS 系统代理设置**（在系统设置 → 网络 → 代理中配置）定义：

- Web Proxy (HTTP)
- Secure Web Proxy (HTTPS)
- SOCKS Proxy
- FTP Proxy

macOS 对图形应用程序的代理配置处理得很好，但此功能不扩展到 Terminal 中的命令行工作。像 `git`、`npm`、`pip` 或 `homebrew` 这样的命令行工具不会自动继承系统代理。

macOS HTTP/HTTPS 代理专门针对 **HTTP 协议流量** 设计。Telnet 在任意端口建立 **raw TCP 连接** —— 它不使用 HTTP 协议，因此 macOS 没有依据将其路由通过 HTTP 代理。

某些图形应用程序（基于 GUI 的软件）不使用系统代理设置。因此，即使在网络级别配置了中介服务器，这些程序也可能忽略它并需要手动配置。如果应用程序根本不支持代理配置，可以使用 Proxifier 等特殊实用程序来拦截流量并将其路由通过配置的代理服务器。

---

## `ping` 与 `telnet` 代理行为比较

| 工具 | 协议 | 是否使用 macOS HTTP 代理？ | 是否使用 macOS SOCKS 代理？ | 备注 |
|---|---|---|---|---|
| `ping` | ICMP | ❌ 否 | ❌ 否 | ICMP 在第 3 层运行；代理在第 4/7 层工作 |
| `telnet` | TCP (raw) | ❌ 否 | ❌ 否（默认） | CLI 工具不会自动读取 macOS 代理 |
| Safari / Chrome | HTTP/HTTPS | ✅ 是 | ✅ 是 | GUI 应用程序尊重系统代理 |

**`ping` 为什么绕过代理：**
`ping` 使用 **ICMP**（Internet Control Message Protocol），它在网络层工作——低于 TCP。代理（HTTP、SOCKS）在传输/应用层运行。代理没有机制拦截 ICMP 流量。

**`telnet` 默认也绕过代理的原因：**
`telnet` 是一个 CLI 工具。macOS 代理系统不会自动配置命令行网络代理。与浏览器不同，`telnet` 建立 **direct TCP 连接**，并且不会自行查询 `HTTPEnable`、`HTTPSEnable` 或 `SOCKSEnable` 系统设置。

---

## 如何强制 `telnet` 通过代理

如果您希望 `telnet`（或其他 CLI 工具）通过代理，您有以下选项：

**选项 1 — 使用环境变量（针对支持 HTTP 的 CLI 工具）：**

```bash
export http_proxy="http://proxyhost:port"
export https_proxy="http://proxyhost:port"
```

注意：`telnet` 本身忽略这些，但像 `curl` 或 `wget` 等其他 CLI 工具会尊重它们。

**选项 2 — 使用 `nc` (netcat) 与 SOCKS 代理：**

```bash
nc -x proxyhost:1080 -X 5 targethost targetport
```

**选项 3 — 使用 Proxifier 或类似工具** 强制特定应用程序（包括 CLI 工具）的所有流量通过系统 SOCKS 代理。

**选项 4 — 在脚本中动态读取 macOS 代理设置：**
`scutil --proxy` 命令允许访问系统代理配置。您可以使用 `awk` 解析其输出，并在 shell 配置文件中相应导出 `http_proxy`。

---

## 总结

- **Telnet** 使用 Telnet 协议创建 raw TCP 连接；它发送和接收无加密的纯文本。
- **macOS HTTP/HTTPS 代理设置** 仅影响明确实现代理感知的应用程序——主要是 GUI 浏览器和一些检查环境变量的 CLI 工具。
- **`ping` 和 `telnet`** 默认均绕过 macOS 系统代理——`ping` 因为 ICMP 无法代理，`telnet` 因为它是一个不查询 macOS 代理设置的 raw TCP CLI 工具。
- 要将 `telnet` 路由通过代理，需要使用 Proxifier 等第三方工具，或手动使用带有 SOCKS 标志的 `nc`。

---

**参考资料：**

- [Telnet - Wikipedia](https://en.wikipedia.org/wiki/Telnet)
- [Telnet Explained - ClouDNS](https://www.cloudns.net/blog/telnet-explained-what-is-it-and-how-it-works/)
- [Introduction to TELNET - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-to-telnet/)
- [Mac OS X Network Proxy Settings in Terminal – dmorgan.info](https://dmorgan.info/posts/mac-network-proxy-terminal/)
- [Guide to enable macOS Terminal to respect system proxy – GitHub Gist](https://gist.github.com/MuntashirAkon/fc6e7e85ada12fa1576dd0fe5ff8da8f)
- [MacOS Proxy Settings Guide](https://proxy-ipv4.com/en/blog/how-to-configure-macos-proxy-settings-correctly/)
