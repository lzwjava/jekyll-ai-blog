---
audio: false
generated: true
lang: zh
layout: post
title: Traceroute选项
translated: true
type: note
---

Traceroute 是诊断网络路径的强大工具，虽然其基本用法简单直观，但它还提供了高级选项来自定义行为。下面我将概述常用选项，并通过实际案例解析 traceroute 的高级用法。具体选项取决于操作系统（如 Windows 使用 `tracert`，Linux/macOS 使用 `traceroute`），但我会重点介绍最通用的功能。

### 基础用法
- **Linux/macOS**: `traceroute [目标地址]`
  - 示例：`traceroute google.com`
- **Windows**: `tracert [目标地址]`
  - 示例：`tracert google.com`

该命令会显示您与目标地址之间的路由节点（跃点）及每个节点的往返时延（RTT）。

---

### 常用 Traceroute 选项
以下主要针对类 Unix 系统（Linux/macOS）的 `traceroute` 命令，Windows 的 `tracert` 选项较少但部分概念相通。

1. **`-n`（禁用 DNS 解析）**
   - 跳过 IP 地址到主机名的解析过程，直接显示原始 IP 并加速追踪
   - 用法：`traceroute -n google.com`
   - 适用场景：DNS 解析缓慢或只需关注 IP 地址时

2. **`-m [最大跃点数]`（设置最大跃点数）**
   - 限制追踪的跃点数量（默认通常为 30）
   - 用法：`traceroute -m 15 google.com`
   - 适用场景：避免目标不可达或路径过长时无限循环

3. **`-q [查询次数]`（每跃点发送包数）**
   - 设置每个跃点的探测包数量（默认值为 3），每次查询显示一个延迟值
   - 用法：`traceroute -q 1 google.com`
   - 适用场景：减少输出冗余或加速追踪；增加次数可获取更可靠的延迟数据

4. **`-w [等待时间]`（每跃点超时阈值）**
   - 设置等待响应的时间（单位：秒），超时则标记为无响应
   - 用法：`traceroute -w 2 google.com`
   - 适用场景：适应慢速网络或减少高速网络中的延迟

5. **`-p [端口号]`（指定 UDP 模式端口）**
   - 设置基于 UDP 的 traceroute 目标端口（默认通常为 33434+）
   - 用法：`traceroute -p 53 google.com`
   - 适用场景：针对特定服务（如 DNS 端口 53）或绕过 ICMP 过滤

6. **`-I`（使用 ICMP 替代 UDP）**
   - 从 UDP（多数系统默认）切换为 ICMP 回显请求包
   - 用法：`traceroute -I google.com`
   - 适用场景：某些网络屏蔽 UDP 但允许 ICMP，可提升可见性

7. **`-T`（TCP 模式）**
   - 使用 TCP 数据包（通常为 SYN 包）替代 UDP/ICMP
   - 用法：`traceroute -T -p 80 google.com`
   - 适用场景：绕过屏蔽 ICMP/UDP 的防火墙，特别适用于追踪 Web 服务器（端口 80）

8. **`-f [起始 TTL]`（设置初始 TTL）**
   - 指定起始 TTL 值，跳过前期跃点
   - 用法：`traceroute -f 5 google.com`
   - 适用场景：聚焦特定网络段（如本地网络之后的路由）

9. **`-g [网关]`（松散源路由）**
   - 强制数据包经过指定网关（需网络支持）
   - 用法：`traceroute -g 192.168.1.1 google.com`
   - 适用场景：测试特定路由或绕过默认路径

10. **`-4` 或 `-6`（强制 IPv4/IPv6）**
    - 限制 traceroute 使用 IPv4 或 IPv6 协议
    - 用法：`traceroute -6 google.com`
    - 适用场景：确保测试特定协议，适用于双栈网络

---

### Windows `tracert` 选项
Windows 选项较少，主要包含：
- **`-d`**：禁用 DNS 解析（类似 `-n`）
- **`-h [最大跃点数]`**：最大跃点数（类似 `-m`）
- **`-w [超时时间]`**：等待时间（毫秒，类似 `-w`）
- 示例：`tracert -d -h 20 google.com`

---

### 高级用法示例
以下为组合选项的实战场景：

1. **诊断网络延迟瓶颈**
   - 目标：定位延迟突增的节点
   - 命令：`traceroute -I -q 5 -w 1 google.com`
   - 原理：ICMP 提升可靠性，5 次查询优化延迟统计，1 秒超时加速追踪

2. **绕过防火墙限制**
   - 目标：追踪被 ICMP 过滤的 Web 服务器
   - 命令：`traceroute -T -p 443 google.com`
   - 原理：TCP 端口 443（HTTPS）模拟合法流量，通常不会被防火墙拦截

3. **聚焦外部路由分析**
   - 目标：跳过本地节点分析外部路由
   - 命令：`traceroute -f 3 -m 10 google.com`
   - 原理：从第 3 跃点（越过本地路由器/ISP）开始，限制 10 个跃点

4. **对比 IPv4/IPv6 路径差异**
   - 目标：验证协议选择对路由的影响
   - 命令：
     - `traceroute -4 google.com`
     - `traceroute -6 google.com`
   - 原理：识别网络路径或性能的协议级差异

5. **自动化脚本快速追踪**
   - 目标：生成简洁输出供脚本处理
   - 命令：`traceroute -n -q 1 -w 1 google.com > output.txt`
   - 原理：禁用 DNS、单次查询、短超时，结果重定向至文件

---

### 高级使用技巧
- **工具组合**：结合 `ping`（延迟分析）与 `mtr`（实时路由追踪）深化诊断
- **理解网络环境**：防火墙、NAT 或 VPN 可能导致跃点显示为星号（`*`）——需调整协议（ICMP/TCP）适配
- **权限要求**：类 Unix 系统中部分选项（如 TCP 模式）需 `sudo` 获取原始套接字权限：`sudo traceroute -T google.com`

Traceroute 的精髓在于其灵活性。通过调整选项，可精准定位网络故障、突破访问限制或深度解析路由行为。如有特定场景需求，欢迎进一步探讨！
