---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hysteria 2 GFW 绕过状态 2026
translated: true
type: note
---

问题：Hysteria 2 在绕过 GFW 封锁方面表现好吗？

回答： 

**Hysteria 2 在 2026 年初对 Great Firewall (GFW) 仍保持合理有效性，但已不再是绝对最强或最可靠的选择之一。**

以下是基于技术论文、开发者讨论和用户报告的当前情况：

- **Hysteria 2 绕过 GFW 的优势**  
  - 使用 QUIC（基于 UDP，非常类似于 HTTP/3 流量），有助于与正常网页浏览/视频流混淆。  
  - Brutal 拥塞控制在高丢包或不稳定连接上表现出色（中国移动/国际线路差的环境常见）。  
  - 许多用户仍报告日常使用稳定，尤其是配置良好时（合适的伪装域名、一致的 SNI、密码认证、可用时端口跳跃）。  
  - 在低到中等流量场景下，通常比旧的基于 TCP 协议（如 VMess WS、Shadowsocks plain 等）表现更好。

- **2025–2026 年实际问题和弱点**  
  - 自 2024 年中以来，GFW 已部署 **selective QUIC/SNI censorship**（解密 QUIC Initial 数据包并基于 SNI 阻断）。许多基于 QUIC 的工具（包括基础 Hysteria 2）变得更容易被针对。  
  - 2025 年 USENIX Security 论文暴露弱点后，社区在 quic-go、Hysteria、sing-box 等中添加了 **SNI slicing / ECH-like defenses** → 新版 Hysteria 2 + sing-box / 更新客户端再次变得更难阻断。  
  - 仍被某些代理服务分类为 **“partially blocked”**（取决于地区/提供商/服务器）。某些中国运营商（如特定联通/电信区域）对 QUIC/UDP 的干扰比其他运营商更激进。  
  - 自托管服务器如果使用非 443 端口无跳跃、伪装弱、高流量模式，或 IP 被标记运气不好，则几天/几周后经常被阻断。

- **与当前顶级 GFW 抗性协议比较（2026 年初）**  

  | Protocol              | GFW Resistance (2026) | Speed / Lossy Lines | Detection Risk | Notes                              |
  |-----------------------|------------------------|----------------------|----------------|------------------------------------|
  | VLESS + Reality       | ★★★★★                 | Good                 | Very low       | 目前被大多数人视为 #1              |
  | VLESS + gRPC + uTLS   | ★★★★☆                 | Medium               | Low            | 良好指纹下仍很强                   |
  | Hysteria 2            | ★★★☆☆                 | Excellent            | Medium         | 速度快但稳定性更易变               |
  | TUIC v5               | ★★★☆☆                 | Very good            | Medium         | 类似 QUIC 家族                     |
  | WireGuard / AmneziaWG | ★★☆☆☆                 | Good                 | High           | 如今易被指纹识别                   |

**总结**  
Hysteria 2 **仍然不错**（尤其如果你重视差线路上的速度，并使用现代客户端 + 合适伪装），但它 **不再是最坚不可摧的选择**。许多经验用户现在将 **Reality-based flows** 作为首选，并将 Hysteria 2 / TUIC 作为快速备份协议。稳定性高度取决于：  
- 你的 ISP + 地区  
- 服务器提供商 / IP 声誉  
- 确切客户端 + 服务器版本  
- 是否使用端口跳跃 / 频繁更改配置  

如果你的当前 Hysteria 2 节点很快失效，先尝试切换到 Reality。

参考资料：  

- [Exposing and Circumventing SNI-based QUIC Censorship of the Great Firewall of China (USENIX Security 2025)](https://gfw.report/publications/usenixsecurity25/en)
- [Hysteria 2 official documentation and discussions](https://github.com/apernet/hysteria/discussions)
- [Community reports on partial blocking (Xeovo Hub)](https://hub.xeovo.com/posts/115-hysteria-20-launch-new-way-to-bypass-censorship)