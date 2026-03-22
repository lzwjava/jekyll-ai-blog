---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS SSH 代理挂起问题分析
translated: true
type: note
---

参考价值很高！以下是它们与你的 SSH proxy 挂起问题的关联：

## Reference Analysis

**Reference 1 (Apple Discussions)** - 部分相关
- **相似症状**：SSH 挂起且无错误，tcpdump 显示没有流量
- **不同的根因**：Cloudflare Warp VPN 拦截了 SSH，而非 HTTP proxy 环境变量
- **启示**：VPN/proxy 软件可以通过多种方式静默拦截 SSH

**Reference 2 (The Register - Catalina SSH bug)** - 高度相关 ✅
- **直接匹配**：macOS SSH + proxy 配置导致挂起
- **根因**：Auto Proxy Discovery 干扰了 SSH
- **核心见解**：该 bug 会影响通过 hostname 连接到端口 >8192 的 SSH，禁用 proxy 设置后即可修复

## How They Support Your Answer

你的诊断（HTTP_PROXY/HTTPS_PROXY 环境变量拦截了 SSH）非常准确。Reference 2 证实了 **macOS SSH + proxy 设置 = 已知的挂起问题**。虽然 Catalina 的 bug 专门针对 Auto Proxy Discovery，但其模式是完全一致的：

1. Proxy 配置处于激活状态
2. SSH 尝试建立连接
3. Proxy 拦截或错误处理了该连接
4. SSH 静默挂起

## Suggested Addition to Your Answer

你可以在结尾添加以下背景信息：

---

## Known macOS SSH + Proxy Issues

这是 macOS 上反复出现的一种模式：
- **macOS 10.15.4 bug**：Auto Proxy Discovery 破坏了连接到端口 >8192 的 SSH ([source](https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/))
- **VPN interference**：类似 Cloudflare Warp 的应用可能会静默拦截 SSH ([source](https://discussions.apple.com/thread/255263733))
- **HTTP_PROXY env vars**：Clash/V2Ray 等 proxies 会拦截包括发往 LAN IPs 的 SSH 在内的所有 TCP 连接（本案例情况）

共同点：proxy/VPN 软件将 SSH 误当作 HTTP 流量处理，导致无法正确路由。

这两个引用都证明了你的诊断属于 macOS SSH 中一类有据可查的问题，即与 proxy/VPN 干扰相关。