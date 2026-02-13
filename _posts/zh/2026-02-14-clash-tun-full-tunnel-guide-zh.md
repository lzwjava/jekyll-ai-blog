---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Clash TUN 模式全虚拟网卡隧道教程
translated: true
type: note
---

**Question: 如果将 OpenConnect 与 Clash 作为代理程序配合使用，如何让 Clash 像全局隧道（full tunnel）模式一样工作，或者在使用 OpenConnect 的同时支持 VMess/Trojan 协议地址？（参考 Clash 日志示例，显示 gvt2.com、openrouter.ai 等域名的代理使用情况）**

**Answer:**

OpenConnect 严格来说是一个 **SSL VPN client**（用于 Cisco AnyConnect、Pulse、Juniper 等协议）。它**原生不支持** VMess、VLESS、Trojan 或任何基于 V2Ray/Xray 的协议 —— 这些是完全不同的架构。在 OpenConnect 中没有内置的方法直接使用 VMess/Trojan 服务器地址。

Clash（或 Clash Meta/Verge/Premium cores）原生已经支持 VMess、Trojan、Shadowsocks 等 —— 这正是它的核心优势。

你的目标似乎是在使用 VMess/Trojan 节点时实现 **类似全局隧道（full-tunnel-like）的体验**（类似 VPN，所有流量都通过代理路由；如你的日志所示：🐟 漏网之鱼 节点正在处理前往 openrouter.ai、Google 域名等的流量）。

### 选项 1：在 TUN 模式下使用 Clash（推荐用于 macOS 的类全局隧道行为）

Clash 的 **TUN mode**（在 Clash Premium core、Clash Verge、Clash for Windows Premium 等中可用）会创建一个虚拟网络接口（类似轻量级 VPN），并将**所有**（或选定的）系统流量路由通过它 —— 这与 Cisco AnyConnect 的全隧道模式非常相似。

- 完全不需要 OpenConnect。
- 你的 VMess/Trojan 节点可以直接工作。
- 绕过许多应用层限制（例如：游戏、大量 UDP 流量的应用，或忽略系统代理的应用）。

**如何在 macOS 上的 Clash 中开启类全局隧道模式：**

1. 使用支持 TUN 的 Clash 客户端（Clash Verge 在 macOS 上很流行且免费）。
2. 在设置中 → 开启 **TUN Mode**（有时称为“增强模式”或“服务模式”）。
   - 首次开启时，可能会要求安装 TUN 驱动/服务（请授予权限；它使用系统扩展）。
3. 将 **Mode** 设置为 **Global**（所有流量经过代理）或 **Rule**（基于你的规则进行智能路由）。
4. 关闭 **System Proxy**（TUN mode 不需要它 —— 事实上，两者都开启可能会产生冲突）。
5. 在你的 YAML 配置文件中：
   - 确保你的 VMess/Trojan 代理已加载（通过订阅或手动）。
   - 添加一个 proxy-group，例如 `PROXY` 并选择你的 🐟 漏网之鱼 节点。
   - 实现全隧道：将最终规则设置为 `MATCH,PROXY`（或你的分组）。
6. 重启 Clash → 使用 `curl ipinfo.io` 或浏览器测试（应显示代理 IP）。

**优点**：真正的系统级路由，支持 UDP，与真正的 VPN 相比开销较低。  
**缺点**：需要一次性管理员权限，可能需要允许内核扩展（macOS 安全提示）。

你的日志已经显示 Clash 在 **System Proxy** 模式下运行良好 —— 切换到 TUN 会使其行为更像全隧道 VPN。

### 选项 2：继续使用系统代理（System Proxy）模式（即你现在的用法）

你当前的设置（Clash 监听 7890/7891，开启系统代理）已经为遵循系统代理设置的应用（浏览器、curl、HTTPS 上的 git 等）代理了 TCP 流量。

- 这**不是**全隧道 —— UDP、原始套接字或忽略代理的应用会绕过它。
- 为了让它“更像全隧道”：在 Clash GUI 中开启 **Global** 模式。
- 但对于通过 SSH 的 git（或其他非 HTTP 应用），除非你通过 tsocks/proxychains 或环境变量（例如 `all_proxy=socks5://127.0.0.1:7891 git ...`）强制执行，否则它仍然不会被代理。

### 选项 3：如果你确实需要 OpenConnect + VMess/Trojan（高级，不推荐）

你无法让 OpenConnect 直接识别 VMess/Trojan。

变通方法（复杂）：
- 在 TUN mode 下运行 Clash → 然后在这个代理环境中运行 OpenConnect（极少派上用场）。
- 使用 ocproxy（为 OpenConnect 提供基于 lwIP 的 SOCKS proxy）→ 但依然不支持 VMess。
- 链路：OpenConnect → 暴露为 SOCKS → 作为 Clash 的 outbound 输入 → 但这没意义，因为 Clash 已经拥有更好的协议。

最好的建议：**忘掉 OpenConnect**，除非是为了连接到公司的 Cisco/Pulse VPN。对于你的 VMess/Trojan 用例（翻墙、ChatGPT 等），Clash TUN mode 可以在没有任何 Cisco 兼容层的情况下为你提供想要的全隧道体验。

如果你的公司 VPN 要求 Cisco AnyConnect 协议，**同时**你又想使用 VMess/Trojan：先运行 Clash TUN（处理通用流量），然后正常连接 OpenConnect（它可能只路由 VPN 网段流量，或者会产生冲突 —— 请仔细测试）。

References:

- [Clash Verge TUN Mode Guide](https://github.com/clash-verge-rev/clash-verge-rev)
- [OpenConnect Manual (no VMess/Trojan mention)](https://www.infradead.org/openconnect/manual.html)
- [Clash TUN vs System Proxy Discussion](https://github.com/MatsuriDayo/nekoray/issues/739)
- [ocproxy for OpenConnect SOCKS exposure](https://github.com/cernekee/ocproxy)