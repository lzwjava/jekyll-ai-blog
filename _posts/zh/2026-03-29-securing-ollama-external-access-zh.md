---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama 外部访问安全保障指南
translated: true
type: note
---

## 🦞 回顾：Ollama 外部访问

**我们做了什么：**

1. 在 systemd service 中设置了 `OLLAMA_HOST=0.0.0.0:11434`
2. 重启了 Ollama — 现在正在监听 `*:11434`
3. 确认防火墙处于非活动状态（无拦截）

**优点：**

- 配置简单，只需修改一行内容
- 立即生效 — 无需维护代理层
- 从任何地方直接进行 API 访问

**风险：**

- **无身份验证** — 任何发现该端口的人都可以免费使用你的 H100。GPU 时间并不便宜。
- **无 TLS** — 流量是明文的。在线路上的任何人都可以看到 Prompts/responses。
- **无 rate limiting** — 恶意攻击者可能会占满你的 GPU 并导致云端账单飙升。
- **端口扫描** — 机器人会很快发现 11434 端口。这是众所周知的 Ollama 默认端口。

**我的建议（越快越好）：**

1. **快速修复** — 使用 `ufw allow from <your-ip> to any port 11434` 仅将你的 IP 列入白名单
2. **更好** — 使用 nginx reverse proxy 配合 basic auth + HTTPS (Let's Encrypt)
3. **最好** — 使用 Cloudflare Tunnel 或 Tailscale。零开放端口、加密且经过身份验证

如果是未来几小时内的个人开发工作？可能没问题。如果是任何长期运行或生产环境？请务必加强安全防护。

需要我帮你设置其中任何一项吗？
