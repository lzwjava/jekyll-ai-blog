---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hysteria2 端口跳跃设置指南
translated: true
type: note
---

**问题：** 如何在 Hysteria2 中启用和配置 Port Hopping 以避免 UDP 限速和 GFW 封锁？

**答案：**

## Hysteria2 Port Hopping — 完整设置指南

端口跳跃是一种强大的反审查功能。中国用户有时报告他们的 ISP 会封锁或限速持久的 UDP 连接，但这些限制通常仅适用于使用的特定端口。端口跳跃通过让客户端随机选择指定的端口之一进行初始连接，并定期切换到不同的端口来作为变通方法。

---

## 工作原理（架构）

Hysteria 服务器没有内置支持监听多个端口，因此无法在服务器端使用多端口格式作为监听地址。推荐的方法是使用 iptables DNAT 将端口重定向到服务器的监听端口。

因此设置分为两部分：
- **服务器端：** iptables DNAT 规则将端口范围转发 → 一个真实端口
- **客户端：** 多端口地址格式 + `hopInterval` 配置

---

## 步骤 1 — 服务器端：配置 iptables DNAT

服务器本身监听**单个端口**（例如 `5353` 或 `443`）。使用 iptables 将宽端口范围转发到该端口。

**安装 iptables-persistent（以在重启后持久化）：**
```bash
apt install iptables-persistent -y
```

**添加 DNAT 规则，将 UDP 端口 20000–50000 转发到端口 5353：**
```bash
# IPv4
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j DNAT --to-destination :5353

# IPv6
ip6tables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j DNAT --to-destination :5353
```

**永久保存规则：**
```bash
sudo iptables-save > /etc/iptables/rules.v4
sudo ip6tables-save > /etc/iptables/rules.v6
sudo systemctl enable netfilter-persistent
sudo systemctl start netfilter-persistent
```

> 可以使用任何端口范围（例如 20000–40000）。只需确保 VPS 防火墙/安全组也允许该范围的 UDP 流量。

---

## 步骤 2 — 服务器配置（`/etc/hysteria/config.yaml`）

服务器配置保持简单 — 仅监听**一个端口**：

```yaml
listen: :5353   # 单个监听端口

tls:
  cert: /etc/hysteria/server.crt
  key:  /etc/hysteria/server.key

auth:
  type: password
  password: YOUR_STRONG_PASSWORD

masquerade:
  type: proxy
  proxy:
    url: https://bing.com
    rewriteHost: true
```

---

## 步骤 3 — 客户端：多端口地址格式

Hysteria 客户端支持特殊的多端口地址格式。您可以指定多个单个端口、端口范围或两者的组合。指定端口数量没有限制。

示例：
```
example.com:1234,5678,9012          # 多个单个端口
example.com:20000-50000             # 端口范围
example.com:1234,5000-6000,8000-9000  # 组合
```

---

## 步骤 4 — 客户端配置：设置 `hopInterval`

transport 部分的 `hopInterval` 选项控制端口跳跃间隔。只有在使用端口跳跃地址时才相关。

```yaml
server: example.com:20000-50000   # 端口跳跃范围

auth: YOUR_STRONG_PASSWORD

tls:
  sni: example.com
  insecure: false

transport:
  type: udp
  udp:
    hopInterval: 30s   # 每 30 秒切换到新端口

socks5:
  listen: 127.0.0.1:1080

http:
  listen: 127.0.0.1:8080
```

> 推荐的 `hopInterval` 值：`10s` 到 `60s`。较短的间隔提供更强的反指纹识别，但开销略大。

---

## 跳跃工作原理（流量流程）

```
客户端 → 20000-50000 中的随机端口
         ↓ (服务器上的 iptables DNAT)
         → 服务器端口 5353
         ↓ (每 hopInterval 秒)
客户端跳跃到范围内的不同端口 → 仍映射到 :5353
```

假设服务器在您指定的所有端口上均可达，跳跃过程对上层是透明的，不会导致数据丢失或断开连接。

---

## 提示与注意事项

| 项目 | 详情 |
|------|------|
| 端口范围大小 | 越大越好（例如 20000–50000）以进行反指纹识别 |
| 防火墙 | 在 VPS 提供商的安全组中为整个范围打开 UDP |
| hopInterval | `30s` 是良好的默认值；越低越难跟踪，开销越大 |
| IPv6 | 始终与 iptables 规则一起添加 ip6tables 规则 |
| 重启持久化 | 必需 — 使用 `netfilter-persistent` 或等效工具 |

---

**参考资料：**

- [Hysteria2 官方 Port Hopping 文档](https://v2.hysteria.network/docs/advanced/Port-Hopping/)
- [Hysteria2 完整客户端配置](https://v2.hysteria.network/docs/advanced/Full-Client-Config/)
- [Hysteria2 完整服务器配置](https://v2.hysteria.network/docs/advanced/Full-Server-Config/)
- [极客博客：对抗 QoS 阻断/限速，Hysteria2 端口跳跃设置](https://geekbb.xlog.app/dui-kang-QoS-zu-duan--xian-su-Hysteria2-duan-kou-tiao-yue-she-zhi)
- [SQYBI：解决 OpenWrt 上 Hysteria2 Port Hopping 问题](https://sqybi.com/en-US/blog/solving-the-issue-openwrt-homeproxy-hysteria2-port-hopping/)