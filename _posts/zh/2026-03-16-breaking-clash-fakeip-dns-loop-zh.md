---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 打破 Clash Fake-IP DNS 循环
translated: true
type: note
---

## 解决方案总结与关键障碍

### **识别出的根本原因**
**Clash Fake-IP 模式下的 DNS 循环**：Clash 为其自身 proxy server domain 返回 fake IP（198.18.x.x），从而创建无限路由循环。

### **应用的 3 部分修复方案**

1. **`proxy-server-nameserver` 配置**
   - 添加到 Clash DNS 配置中
   - 专门为 proxy server 主机名使用真实 DNS（223.5.5.5、119.29.29.29）
   - 防止 proxy server domain 获取 fake IP

2. **`fake-ip-filter` 排除**
   - 将 proxy server domain 添加到过滤列表
   - 强制 Clash 为 proxy server domain 返回真实 IP
   - 在过滤层打破 DNS 循环

3. **DIRECT 路由规则**
   - 为 proxy server IP 添加明确的 `IP-CIDR` 规则
   - 确保到 proxy server 的流量走 DIRECT（绕过代理）
   - 防止任何剩余路由问题

### **最具挑战性的障碍**

**“鸡与蛋” DNS 问题** 是最大的障碍：

```
iPad → Clash → 需要 proxy → 解析 proxy domain → 获取 FAKE IP (198.18.x.x) 
→ 尝试路由 fake IP → TUN 拦截 → 返回 Clash → 无限循环
```

这在日志中**不可见** - 流量会到达 TUN，但连接会无声挂起，因为 Clash 无法建立到自身的上游连接。

### **关键洞察**
突破来自于认识到 **Clash 自身的 DNS 在自毁**。当 Clash 尝试连接其 proxy server 时：
- 正常 DNS：`proxy-server.com` → `real.ip.addr` ✓
- Clash Fake-IP DNS：`proxy-server.com` → `198.18.x.x` (FAKE!) ❌

### **当前状态**
- ✅ **DNS 循环已修复**：Proxy server 解析为真实 IP
- ✅ **所有基础设施正常工作**：DHCP、NAT、转发、TUN
- ✅ **iPad 流量流通**：SYN 数据包到达 Clash
- ✅ **干净的单进程**：无剩余僵尸进程

架构现在是**正确的** - DNS 配置确保 proxy server 获取真实 IP，而正常 domain 获取 fake IP 以供 TUN 拦截。