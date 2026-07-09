---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude代码代理瞬态错误诊断
translated: true
type: note
---

Claude Code 正在运行——第三方代理服务器可达，认证令牌有效。您遇到的错误很可能是临时性的。

以下是完整诊断：

---

**根本原因：第三方 API 代理的临时性故障**

您的 Claude Code `settings.json` 指向一个非官方端点：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://claude2.sssaicode.com/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-sss...0443"
  }
}
```

这是一个第三方代理，提供对 Claude 模型（您的情况是 Opus 4）的访问。它部署在 Cloudflare 后面，解析到美国 IP `50.87.93.246`。

连接路径：

```
Claude Code CLI (Node.js)
  → https_proxy http://127.0.0.1:7890 (mihomo)
    → mihomo: sssaicode.com 无显式规则 → DIRECT
      → cloudflare → claude2.sssaicode.com
```

我刚才测试时，它正常工作——约 2.8 秒返回有效响应。因此问题是暂时的（服务器宕机了几分钟、Cloudflare 重新路由或 DNS 抖动）。

**为什么您看到的是 "ConnectionRefused" 而不是更详细的错误**：Anthropic SDK 的 Node.js HTTP 客户端在 `fetch`/`https` 模块无法建立连接时，会将 TCP 级别的故障统一报告为 "ConnectionRefused"——临时服务器宕机、DNS 失败、代理路由抖动都会归于同一个消息。SDK 层没有重试/回退机制来掩盖短暂的中断。

**要提高稳定性**，您可以：

1. **为 sssaicode.com 添加显式代理规则**，使其始终通过您的 SS/Hysteria2 隧道（而非 DIRECT）路由，以防从中国直连不稳定：
   ```
   - DOMAIN-SUFFIX,sssaicode.com,Proxy
   ```

2. **切换到官方 Anthropic API**（从中国出发，没有可靠代理会比较困难），使用 `ANTHROPIC_API_KEY` 而非第三方代理。不过，该第三方代理在其他情况下似乎运行良好——您刚刚收到了来自 Opus 4 的响应，每次请求花费 $0.27。

3. **直接重试**——该错误是临时性的。如果再遇到，等待一分钟后重试。