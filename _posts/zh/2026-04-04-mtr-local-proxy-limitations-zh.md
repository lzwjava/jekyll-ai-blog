---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MTR本地代理限制指南
translated: true
type: note
---

**问题：**能否通过本地代理（如Mihomo或Clash在7890端口等）运行MTR？

**回答：**

### 简短回答
**不能，无法直接且稳定地实现。**

MTR（及其底层使用的 `traceroute` + `ping` 工具）在较低网络层级运行，使用 **ICMP**（用于 ping）和 **UDP** 或 **ICMP**（用于 traceroute）。大多数本地代理如 **Clash**、**Mihomo** 或类似工具主要通过 **SOCKS5** 或 **HTTP** 代理处理 **TCP**（有时也包括 UDP）流量。它们并不原生支持或以标准命令行工具（如 `mtr`）能使用的方式转发原始 **ICMP** 数据包。

### 为何通常无效
- **协议限制**：
  - Ping/MTR 发送 **ICMP Echo Request** 数据包。
  - SOCKS5 代理（Mihomo/Clash 中的混合端口 7890/7891/7892）专为 TCP/UDP 连接设计，不支持原始 ICMP。
  - HTTP 代理限制更多（仅限第7层）。

- **MTR 无内置代理支持**：
  MTR 没有类似 `--proxy`、`-x` 或适用于它的环境变量（`http_proxy`、`all_proxy`）选项。设置 `all_proxy=socks5://127.0.0.1:7890` 会被 MTR 忽略，因为它绕过了尊重这些变量的标准 libc socket 调用。

- **常见结果**：
  当代理处于活动状态时尝试 `mtr example.com`（特别是在 TUN/重定向模式下），MTR 通常：
  - 仅显示本地代理为唯一跳点，或
  - 完全失败，显示高丢包率或“无路由”，或
  - 忽略代理直接连接。

### 可能的变通方案（成功率有限）
以下是实际可行的选项，按从易到难排序：

1. **在 Mihomo/Clash 中使用 TUN 模式（最适合多数用户）**
   在 Clash/Mihomo 客户端启用 **TUN 模式**（虚拟网络接口）。
   这会在系统级别拦截**所有**流量，在许多情况下包括 ICMP。
   - 然后正常运行 `mtr google.com`。
   - 结果：MTR 流量会通过选定的代理节点（如果规则允许）。
   - 限制：TUN 模式对 ICMP 的支持因平台而异（Linux/macOS 在正确配置下表现更好；Windows 较复杂）。如果启用了 fake-IP，DNS 解析也可能受影响。

2. **为 MTR 设置直连规则**
   在 Mihomo/Clash 配置中添加规则，使 MTR 的流量绕过代理：
   - 按进程名：`PROCESS-NAME,mtr,DIRECT`
   - 或按目标：将特定域名/IP 设为 DIRECT。
   这让你可以正常运行 MTR 而免受代理干扰，但**不会**让 MTR 流量*经过*代理。

3. **使用支持代理的替代工具**
   - **tcptraceroute** 或 **traceroute -T**（基于 TCP 的 traceroute）——若配合 `proxychains` 或 `tsocks` 封装，有时能更好地与 SOCKS5 协同工作。
   - **proxychains-ng**（或 `proxychains4`）：
     安装后，配置本地 SOCKS5 端口（如 7890），然后运行：
     `proxychains mtr google.com`
     成功率：对于基于 ICMP 的 MTR 较低，对 TCP 变种更好。
   - **hping3** 或自定义脚本实现 ICMP over TCP 隧道（高级方案，不推荐日常使用）。

4. **在远程服务器上运行 MTR**
   通过 SSH 登录已路由至你所需代理/VPN 的 VPS，然后在那里运行 MTR。这通常是测试*经过*特定代理路径的最清晰方法。

5. **高级设置（仅限 Linux）**
   使用 `redir`/`iptables` + `socat` 或 `iproxy` 等工具转发 ICMP，但此方法脆弱且对多数用户不实用。

### 建议
- 若需快速诊断**实际**网络路径（包括代理影响），启用 **TUN 模式** 并测试 MTR。
- 若要查看代理网络**内部**的路径，在已处于代理后的机器/VPS 上运行 MTR。
- 如果仅需最终目的地的延迟/丢包信息（而非逐跳数据），使用 `proxychains` 封装的 `ping`，或直接通过尊重代理的 curl/wget 测试。

实践中，多数网络工程师在需要准确的逐跳信息时会**停用**本地代理运行 MTR，或在 TUN 模式下使用以获取“代理视角”。

若告知操作系统（Linux、macOS、Windows）和具体 Mihomo/Clash 设置（是否启用 TUN？混合端口或仅 SOCKS？），我可提供更精确的命令。

参考资料：
- 无
