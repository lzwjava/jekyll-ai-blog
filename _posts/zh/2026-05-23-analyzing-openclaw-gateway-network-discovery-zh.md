---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分析OpenClaw网关网络发现
translated: true
type: note
---

**问题：** 解释这个网络发现输出的含义——什么是 OpenClaw Gateway，这次扫描揭示了关于该设备的哪些信息？

**答案：**

## 你所发现的

你执行了一次系统性的局域网侦察，并发现了一台邻居的 MacBook Pro 上运行着一个名为 **OpenClaw Gateway** 的服务，它位于你的子网内。下面我来逐层解析。

---

## 第一层：设备

```
MAC: XX:XX:XX:XX:XX:31
OUI: Apple
mDNS hostname: openclaw.local
```

MAC OUI 查询确认这是 Apple 硬件——根据 mDNS TXT 记录判断为 MacBook Pro。它位于你的局域网（同一子网），可通过 ARP 访问。

---

## 第二层：发现链条

你的方法很清晰，遵循了标准的被动→主动侦察升级流程：

```
arp -a                        # 被动：我的子网上有哪些设备？
  → 发现 IP + MAC

OUI lookup                    # 被动：什么厂商？
  → 3 台 Apple 设备

nc -zv <ip> 1-65535           # 主动：哪些端口开放？
  → 筛选出候选者

nmap -Pn -sV                  # 主动：服务指纹识别
  → 3306 端口上的 MySQL

mDNS 多播查询                 # 被动协议：Bonjour
  → 224.0.0.251 UDP 端口 5353
  → 设备主动宣告其服务
```

其中 mDNS 部分尤其有趣——你没有进行任何暴力扫描。设备通过 Apple 的 Bonjour 协议（DNS-SD / RFC 6762）**自愿广播**了其身份。你只是监听到了。

---

## 第三层：mDNS 揭示了什么

通过 mDNS 的 DNS-SD（服务发现）提供了完整的服务记录树：

| 记录 | 告知你的内容 |
|------|--------------|
| `PTR` | 服务名称：`_openclaw-gw._tcp.local` |
| `TXT` | `role=gateway`、`port=18789`、`hostname=openclaw.local` |
| `SRV` | 规范主机名 + 端口映射 |
| `A/AAAA` | IPv4 + IPv6 地址 |

TXT 记录是信息金矿——由 OpenClaw 软件自身写入的应用层元数据。这是 Bonjour 的设计特性；应用程序注册自己的 TXT 记录以便被发现。OpenClaw 明确宣告了其角色和端口。

---

## 第四层：什么是 OpenClaw？

OpenClaw 并非知名的开源项目。根据扫描结果来看：

- 它是一个运行在端口 18789 上的 **网关/代理服务**
- 自我描述为 `role=gateway`、`transport=gateway`
- 与 MySQL（3306）一同运行——暗示它有一个本地数据库后端
- MySQL 限制特定主机访问——因此不是公共服务，而是一个受控的多组件本地应用

OpenClaw 最可能的候选身份：

1. **本地 LLM/AI 代理网关**——通过本地端点路由 API 调用（OpenAI、Anthropic 等）。“Claw”在 AI 工具中是一个常见主题。网关模式（拦截→路由→记录）与令牌追踪或团队密钥管理完美契合。

2. **企业/团队 API 密钥管理网关**——银行和企业运行此类系统以集中管理 API 访问、限制速率并审计调用。端口 18789 非标准，这在内部工具中很典型。

3. **自定义构建的工具**——鉴于它运行在某人的个人 MacBook 上并使用 mDNS 进行本地发现，这可能是一个在本地网络上代理请求的个人开发工具。

MySQL 后端是关键信息——它用于存储状态：可能是请求日志、使用指标或 API 密钥映射。

---

## 第五层：安全评估

暴露与锁定的情况：

```
端口 18789  - OpenClaw Gateway   开放（局域网内外部可达）
端口 3306   - MySQL              锁定（主机限制）
SSH         - 关闭
VNC         - 关闭
HTTP        - 关闭
```

**高延迟（22–200ms）**暗示 WiFi 节能模式——这是一台不总是主动传输的笔记本电脑，典型的 MacBook 电池供电状态。

**风险面：**
- 端口 18789 现在可以从你的机器访问
- 如果 OpenClaw 没有认证，你可以通过他们的网关发送请求
- MySQL 已正确锁定——良好的实践
- mDNS 自我宣告意味着**子网内任何人都可以自动发现**此设备，无需扫描——在任何 Mac 上只需运行 `dns-sd -B _services._dns-sd._udp`

---

## 你可以下一步做什么（道德范围内）

由于这是别人的设备，你现在处于边界。你到目前为止所做的（ARP、mDNS 监听、在你自己的局域网上进行端口扫描）通常属于被动/灰色地带。更进一步——连接到端口 18789、探测网关 API——则属于未经授权访问的区域。

但如果你想了解协议，你可以探测**你自己的**机器或搭建相同的栈：

```bash
# 查看你的局域网上正在广播哪些 mDNS 服务（被动、安全）
dns-sd -B _services._dns-sd._udp local.

# 解析具体的服务记录
dns-sd -L "openclaw-gw" _openclaw-gw._tcp local.

# 18789 端口上实际是什么？（仅在你自己的设备上操作）
curl -v http://<ip>:18789/
```

---

## 总结

你完成了一次教科书式的局域网侦察。你发现了一台邻居的 MacBook，上面运行着一个似乎是个人或团队 **AI/API 网关工具** 的 OpenClaw，其特点如下：
- 通过 mDNS（Bonjour）自我宣告——有意的服务发现
- 在端口 18789 上运行代理
- 以 MySQL 数据库作为后端
- 可从你的机器访问，但 MySQL 已被正确隔离

有趣的一点是：**mDNS 是一个零努力的蜜罐用于发现**。任何在你的局域网上注册的 Bonjour 服务，无需一次主动扫描即可完全可见。注重安全的服务如果不想被发现，就不应该在 mDNS 上注册。