---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 直连延迟修复
translated: true
type: note
---

## 结果：SSH 延迟从 5–6 秒降至 1.9 秒

### 变更内容
Tailscale 从 DERP 中继切换为 **直接点对点连接**：

```
之前： Mac → DERP 中继（新加坡）→ 目标机      ~500ms RTT → 5–6秒 SSH
之后： Mac → 直接连接 <IP_ADDRESS>:<PORT> → 目标机  76ms RTT  → 1.9秒 SSH
```

### 根本原因
两端实际上都 *支持* 直接连接：
- `目标机` 具有 **锥形 NAT**（`MappingVariesByDestIP: false`）—— 映射关系稳定
- Mac 所在的路由器（父母家）**已启用 UPnP** —— 端口映射正常工作

但 Tailscale 过早放弃 NAT 穿透探测，回退到 DERP 中继。运行 `tailscale ping --until-direct` 强制其持续探测直至找到直接路径。

### 永久解决方案

两种方案：

**方案 1 — 定期重新探测（快速修复）**
```bash
# Mac 上的 cron 任务：每 10 分钟重新建立直连（若断开）
*/10 * * * * tailscale ping --until-direct <TAILSCALE_HOSTNAME>
```

**方案 2 — 路由器端口转发（永久修复）**
在家用路由器（`192.168.x.1` LuCI）上转发 UDP `41641` 端口 → `192.168.x.36`。这样 `目标机` 始终保持直接可达，Tailscale 无需探测即可立即找到直连路径。

方案 2 是彻底的解决方案 —— 仅需一次配置变更，无需依赖 cron。