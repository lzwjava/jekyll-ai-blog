---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH 连接问题排查方法指南
translated: true
type: note
---

我将创建一个诊断指南，展示我用于确定根源的逐步排查方法。

## SSH 连接故障排查方法论

以下是我用于诊断你的 SSH 问题的系统化方法：

### 第 1 步：检查 Proxy 配置

**命令：**
```bash
env | grep -i proxy
```

**揭示的信息：**
- 所有与 Proxy 相关的环境变量
- 是否设置了 HTTP_PROXY, HTTPS_PROXY, ALL_PROXY
- NO_PROXY 排除了哪些内容

**你的结果：**
```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
ALL_PROXY=http://127.0.0.1:7890
NO_PROXY=localhost,127.0.0.1,.example.com,::1
```

**解读：** Proxy 已激活，但 NO_PROXY 不包含 192.168.* 范围（初步怀疑点）。

---

### 第 2 步：验证 Proxy 服务是否运行

**命令：**
```bash
lsof -i :7890
```

**揭示的信息：**
- 是否有进程在监听 Proxy 端口
- 哪个进程拥有该 Proxy 连接

**你的结果：**
```
node       1870 lzwjava   19u  IPv4 ... TCP localhost:55717->localhost:7890 (ESTABLISHED)
AMPLibrar  2729 lzwjava   13u  IPv4 ... TCP localhost:55704->localhost:7890 (ESTABLISHED)
```

**解读：** Proxy 服务肯定在运行并接受连接。

---

### 第 3 步：测试基础网络连通性

**命令：**
```bash
ping -c 3 192.168.2.1
```

**揭示的信息：**
- 主机在网络层（ICMP）是否可达
- 往返时间（RTT）和丢包率

**你的结果：**
```
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 6.923/7.855/9.023/0.874 ms
```

**解读：** 物理网络连通存在，但 ICMP ≠ TCP（ping 使用不同的协议）。

---

### 第 4 步：在无 Proxy 变量的情况下测试 SSH

**命令：**
```bash
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY ssh -o ConnectTimeout=5 root@192.168.2.1 exit
```

**揭示的信息：**
- 移除 Proxy 变量是否能解决问题
- 问题是与 Proxy 相关还是其他原因

**你的结果：**
```
ssh: connect to host 192.168.2.1 port 22: Operation timed out
```

**解读：** ⚠️ **关键发现** —— 在没有 Proxy 的情况下 SSH 依然失败！这推翻了 Proxy 理论。

---

### 第 5 步：检查 SSH 配置

**命令：**
```bash
cat ~/.ssh/config
```

**揭示的信息：**
- SSH 是否配置了 Proxy 命令
- 特定主机的连接规则

**你的结果：**
```
Host !192.168.*.*
    ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

**解读：** `!` 取反符号意味着“对除了 192.168.*.* 以外的所有地址使用 Proxy” —— 因此 192.168.2.1 本就不该使用 Proxy。

---

### 第 6 步：直接测试 22 端口

**命令：**
```bash
nc -zv -w 3 192.168.2.1 22
```

**揭示的信息：**
- 22 端口是否开放并接受连接
- 绕过 SSH 协议直接测试原始 TCP 连通性

**你的结果：**
```
192.168.2.1 22 (ssh): Operation timed out
```

**解读：** 22 端口不可达 —— 这是一个网络/防火墙问题，而不是 SSH 或 Proxy 问题。

---

### 第 7 步：检查本地网络配置

**命令：**
```bash
ifconfig | grep -A 2 "inet 192.168"
```

**揭示的信息：**
- 你的 Mac 处于哪个子网
- 你的本地 IP 地址

**你的结果：**
```
inet 192.168.1.37 netmask 0xffffff00 broadcast 192.168.1.255
```

**解读：** 你处于 192.168.1.0/24，但路由器处于 192.168.2.0/24 —— **不同的子网！**

---

### 第 8 步：检查 ARP 表

**命令：**
```bash
arp -n 192.168.2.1
```

**揭示的信息：**
- 你的 Mac 是否在二层（Layer 2）直接与路由器通信
- 路由器是否在同一个物理网络段

**你的结果：**
```
192.168.2.1 (192.168.2.1) -- no entry
```

**解读：** 没有 ARP 条目 = 没有直接的二层通信 = 路由器不在同一个网络段。

---

### 第 9 步：检查路由表

**命令：**
```bash
route -n get 192.168.2.1
```

**揭示的信息：**
- 你的 Mac 如何路由到 192.168.2.1 的流量
- 使用了哪个网关

**你的结果：**
```
route to: 192.168.2.1
destination: 192.168.2.1
    gateway: 192.168.1.1
  interface: en0
```

**解读：** 到 192.168.2.1 的流量通过网关 192.168.1.1 转发，而不是直接连接。

---

## 诊断决策树

```
SSH 到 192.168.2.1 失败
│
├─ 检查 Proxy 环境变量 → 设置为 127.0.0.1:7890
│  └─ 假设：Proxy 阻塞了 SSH
│     │
│     ├─ 无 Proxy 测试 SSH → 依然失败 ❌
│     │  └─ Proxy 理论被推翻
│     │
│     └─ 检查 SSH config → 192.168.*.* 已排除 Proxy
│        └─ 确认 Proxy 不是问题所在
│
├─ 使用 netcat 测试 22 端口 → 超时
│  └─ 22 端口不可达（不仅仅是 SSH）
│
├─ 检查本地网络 → 192.168.1.37/24
│  └─ 与路由器 (192.168.2.1) 处于不同子网
│
├─ 检查 ARP 表 → 无条目
│  └─ 无直接二层 (Layer 2) 连通性
│
└─ 检查路由 → 经过网关 192.168.1.1
   └─ **结论：网络隔离/分段问题**
      - Ping 正常（ICMP 经网关路由）
      - SSH 阻塞（网关上的防火墙或路由规则限制）
```

---

## 核心诊断原则

1. **逐层测试：**
   - Layer 3 (网络层): `ping`
   - Layer 4 (传输层): `nc -zv`
   - Layer 7 (应用层): `ssh`

2. **隔离变量：**
   - 移除 Proxy 变量以测试是否为 Proxy 问题
   - 使用 `nc` 绕过 SSH 协议测试原始 TCP

3. **检查配置：**
   - 环境变量 (`env`)
   - SSH 配置 (`~/.ssh/config`)
   - 网络接口 (`ifconfig`)

4. **验证假设：**
   - "Ping 通了" 不代表 SSH 就能通
   - 相同的 IP 范围 (192.168.*) 不代表处于相同的子网

5. **寻找证据：**
   - ARP 表显示二层连通性
   - 路由表显示流量走向
   - `lsof` 显示实际监听状态

---

## 确凿证据 (The Smoking Gun)

以下现象的结合：
- ✅ Ping 正常（ICMP 已路由）
- ❌ 即使没有 Proxy，SSH 依然失败
- ❌ 通过 netcat 发现 22 端口不可达
- ❌ 无 ARP 条目
- ⚠️ 不同子网 (192.168.1.x vs 192.168.2.x)
- ⚠️ 流量经过网关转发

**证明：** 这是一个网络分段/防火墙问题，而不是 Proxy 问题。
