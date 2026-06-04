---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale VPN 架构简化
translated: true
type: note
---

**问题：** Tailscale 是如何工作的？

**回答：**

Tailscale 是一个 **基于 WireGuard 的网状 VPN**。它解决了一个难题：无需中央服务器即可穿越 NAT/防火墙连接机器，同时将设置变得极为简单。以下是其机制：

---

## 核心架构

**两个平面：**
1. **控制平面** — Tailscale 的服务器（协调、发现、密钥分发）
2. **数据平面** — 直接的点对点 WireGuard 隧道（加密流量）

控制平面 *从不* 接触你的数据。它只负责编排连接。

---

## 工作原理（逐步说明）

### 1. **初始设置**
```bash
tailscale up
# 打开浏览器，你用账户进行身份验证
# Tailscale 为你的机器分配一个 Tailscale IP（100.x.x.x 范围）
# 你的机器生成一个 WireGuard 密钥对
# 公钥发送到 Tailscale 控制服务器
```

此时，Tailscale 知道：
- 你机器的身份和公钥
- 你的公网 IP（或运营商级 NAT 端点）
- 你的内部网络信息（用于子网路由）

### 2. **对端发现**
当你尝试访问 tailnet 中的另一台机器时（例如 `ssh lzw@100.64.1.2`）：

```
你的机器询问 Tailscale 控制服务器：
"机器 100.64.1.2 的地址/密钥是什么？"

控制服务器响应：
{
  "machine_name": "to",
  "public_key": "<WireGuard 公钥>",
  "endpoints": [
    "203.0.113.45:41641",  // 公网 IP:端口
    "192.168.1.36:41641"   // 私有 IP（如果在同一局域网内）
  ],
  "derp_region": "usa-east"  // 备用中继
}
```

你的机器缓存此信息，不再重复询问（除非机器离线）。

### 3. **直接连接（最佳情况）**
如果两台机器均可访问，Tailscale 使用 **直接 WireGuard 连接**：

```
你的 Mac (100.64.2.5)  ←→ 工作站 (100.64.1.2)
         ↓
加密的 WireGuard 隧道
（UDP，端口可变，点对点）
         ↓
不涉及中央服务器
```

这是 **私有的**、**快速的**（如你测得的 ~10ms），并且是 **直接的**。

---

## 4. **NAT 穿透（难点）**

两台机器通常都位于 NAT 之后。Tailscale 使用 **UDP 打洞** + **STUN**：

```
Tailscale STUN 服务器告诉每台机器：
"你从外部看到的公网 IP:端口 是 <IP>:<PORT>"

两台机器都向彼此发现的端点发送 UDP 数据包。
路由器看到出站流量，创建 NAT 映射。
数据包穿透并建立直接连接。
```

**这样做的原因是：**
- 如果出站流量先发起，NAT 路由器允许入站流量
- Tailscale 通过控制服务器协调时序
- 双方都学习到对方的外部端点

**时序很重要** — 如果一台机器在另一台尝试连接时离线，发现会按需进行。

---

## 5. **备用方案：DERP 中继（当直接连接失败时）**

某些网络会屏蔽 UDP 或具有激进的 NAT。Tailscale 有 **DERP 中继**（指定加密中继代理）：

```
如果直接连接在几秒后失败：

你的 Mac → DERP 中继（加密）→ 工作站
```

DERP 是最后手段的中继。它：
- 运行在 Tailscale 控制的服务器上
- 无法解密流量（WireGuard 加密是端到端的）
- 增加延迟（Tailscale 通过最近区域路由）
- 一旦直接连接恢复，自动禁用

---

## WireGuard 层

Tailscale 通过智能协调封装了 WireGuard。WireGuard 本身完成加密工作：

```python
# 简化的 WireGuard 数据包结构：
[IP 头部] [UDP 头部] [WireGuard 加密载荷]
            └─ 每个数据包都经过身份验证 + 加密
               使用临时会话密钥
```

**关键特性：**
- **无状态** — WireGuard 不跟踪连接（与 IPsec/OpenVPN 不同）
- **小开销** — 每个数据包增加约 100 字节
- **前向保密** — 密钥泄露后，旧数据包无法恢复
- **抗量子安全**（有争议，但使用现代原语）

---

## Tailscale 在此基础上增加的功能

| 功能 | 实现方式 |
|------|----------|
| **Magic DNS** | 控制服务器响应 DNS 查询，返回 Tailscale IP |
| **ACL** | 控制服务器强制执行访问策略（谁能访问谁） |
| **出口节点** | 可配置一台机器，让所有流量通过它路由 |
| **子网路由** | 通过一台机器作为网关，将整个局域网暴露给 tailnet |
| **Tailscale SSH** | 内置 SSH 服务器，由控制平面签名，无需密钥管理 |

---

## 安全模型

```
假设：你信任 Tailscale Inc. 的服务器

如果服务器被攻破：
  ✗ 攻击者得知你的 tailnet 中有哪些机器
  ✗ 攻击者得知哪些设备在线/离线
  ✓ 攻击者 **无法** 解密你的流量（WireGuard 密钥从未存放在他们的服务器上）

如果你的一台机器被攻破：
  ✗ 攻击者可以访问你的整个 tailnet
  ✓ 攻击者无法伪造身份（WireGuard 密钥对是非对称的）
```

控制平面是 **信任边界**，而非流量的威胁边界。

---

## 代码级别示例（简化）

```python
# 伪代码：当你 SSH 时发生的事情

# 1. Tailscale 守护进程（tailscaled）正在运行
$ ps aux | grep tailscaled
# 监听本地接口以接收连接

# 2. SSH 客户端连接到 Tailscale IP
$ ssh lzw@100.64.1.2

# 3. Tailscale 拦截（或你直接 SSH 到 Tailscale IP）
# 4. Tailscale 守护进程查询控制服务器以获取对端信息
#    （如果近期有缓存则使用，否则获取）
peers = control_plane.get_peer("100.64.1.2")

# 5. 建立 WireGuard 隧道
wg_tunnel = wireguard.connect(
    peer_public_key=peers.public_key,
    endpoint=peers.endpoints,  # 先尝试直接连接，再尝试 DERP
)

# 6. SSH 流量现在通过 wg_tunnel 加密传输
# 控制服务器永远不会看到 SSH 数据包
```

---

## 性能：为何你的设置很快

```
延迟分解（你观察到的 10ms）：

直接局域网（同一网络）：
  - Tailscale 开销：约 1-2ms
  - WireGuard 加密：<1ms
  - 网络 RTT：约 8ms
  ────────────────
  总计：约 10ms ✓

同一局域网意味着：
  - 无需互联网路由（本地交换机/路由器）
  - 两台机器在同一子网（192.168.1.x 范围）
  - Tailscale 发现私有 IP（192.168.1.36）
  - 加密并直接发送
```

跨互联网（咖啡店的 Mac → 家里的工作站）：
- 直接连接：约 50-100ms（ISP 路由）
- 通过 DERP 中继：约 100-200ms（中继增加一跳）

---

## 针对你设置的安全威胁模型

| 威胁 | 可利用？ | 缓解措施 |
|------|----------|----------|
| ISP 看到你 SSH 到工作站 | **否** — WireGuard 已加密 | 不适用 |
| Tailscale Inc. 看到你的命令 | **否** — 控制平面是独立的 | 不适用 |
| 工作站被攻破 | **是** — 攻击者拥有访问权限 | 修补 Ubuntu，防火墙阻止非 Tailscale 端口 |
| Tailscale 身份验证令牌被盗 | **是** — 攻击者加入 tailnet | 使用强账户密码，开启双因素认证 |
| 局域网上的网络嗅探器 | **否** — WireGuard 已加密 | 不适用 |

---

## 总结

Tailscale = **围绕 WireGuard 的智能编排**：
- 控制平面发现对端并交换密钥
- 数据平面使用 WireGuard 进行加密隧道
- UDP 打洞解决 NAT 问题
- 直接连接失败时，DERP 中继作为备用
- 无需手动管理证书或 IP，即可实现网状网络

其核心思想是：**将复杂性移到控制平面，让数据平面保持简单和安全**。