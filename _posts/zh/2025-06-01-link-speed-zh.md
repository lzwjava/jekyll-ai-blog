---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu中检查以太网连接速度
translated: true
type: note
---

在 Ubuntu 系统中，您可以通过多种命令行工具检查以太网连接速度。以下是几种常用方法：

### **1. 使用 `ethtool`（推荐）**

`ethtool` 是检测以太网接口当前连接速度最可靠的方法。

#### 安装 `ethtool`（若未预装）

```bash
sudo apt install ethtool
```

#### 检查连接速度

```bash
sudo ethtool <接口名称>
```

请将 `<接口名称>` 替换为您的以太网接口（如 `eth0`、`enp3s0`、`ens33`）。

#### 示例

```bash
sudo ethtool enp3s0
```

在输出结果中查找 `Speed` 和 `Duplex` 字段：

```
设置项 enp3s0:
    支持的端口：[ TP ]
    支持的链路模式：   10baseT/半双工 10baseT/全双工
                      100baseT/半双工 100baseT/全双工
                      1000baseT/全双工
    支持的暂停帧使用：否
    支持自动协商：是
    支持的 FEC 模式：未报告
    通告的链路模式：  10baseT/半双工 10baseT/全双工
                      100baseT/半双工 100baseT/全双工
                      1000baseT/全双工
    通告的暂停帧使用：否
    通告自动协商：是
    通告的 FEC 模式：未报告
    速度：1000Mb/s   # <--- 当前连接速度
    双工：全双工     # <--- 全双工或半双工
    端口：双绞线
    PHYAD：1
    收发器：内置
    自动协商：开启
    MDI-X：开启（自动）
    支持远程唤醒：pumbg
    远程唤醒：d
    当前消息级别：0x00000007 (7)
                  驱动 探测 链路
    检测到链路：是      # <--- 指示网线是否连接
```

---

### **2. 使用 `ip` 或 `ifconfig`（基础信息）**

这些命令可查看接口是否启用，但不会直接显示连接速度。

#### 使用 `ip`

```bash
ip link show <接口名称>
```

示例：

```bash
ip link show enp3s0
```

（仅显示链路状态，无速度信息）

#### 使用 `ifconfig`（已弃用但仍可使用）

```bash
ifconfig <接口名称>
```

示例：

```bash
ifconfig enp3s0
```

（显示接口启用状态，无速度信息）

---

### **3. 使用 `dmesg`（检查驱动日志）**

有时以太网驱动会在初始化时记录协商的速度。

```bash
dmesg | grep <接口名称>
```

示例：

```bash
dmesg | grep enp3s0
```

寻找类似记录：

```
[    5.123456] e1000e: enp3s0 网卡链路已启用 1000 Mbps 全双工
```

---

### **4. 使用 `mii-tool`（旧版系统）**

针对老旧系统可使用：

```bash
sudo apt install net-tools
sudo mii-tool -v <接口名称>
```

示例：

```bash
sudo mii-tool -v eth0
```

（不适用于现代千兆以太网）

---

### **总结**

- **最佳方案：** `sudo ethtool <接口>`（显示速度、双工模式、自动协商）
- **备选方案：** 当 `ethtool` 不可用时检查 `dmesg` 日志
- **基础状态：** `ip link show` 或 `ifconfig`（不显示速度）

如需进一步说明请随时告知！🚀
