---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 如何使用 ARP 命令
translated: true
type: note
---

Question: How to use the arp -a command?

Answer:

`arp -a` 命令用于显示计算机上 ARP (Address Resolution Protocol) 缓存的内容。ARP 缓存是一个表格，它将 IP 地址映射到本地网络中最近与你的计算机通信过的设备的物理 (MAC) 地址。这对于网络故障排查非常有用，例如识别设备、检查 IP 冲突或验证 MAC 地址。

### 如何使用

1. **打开终端或命令提示符**：
   - 在 **Windows** 上：搜索 "cmd" 或 "Command Prompt"（如果需要完全访问权限，请以管理员身份运行）。
   - 在 **Linux** 或 **macOS** 上：打开 Terminal。

2. **运行命令**：
   - 只需输入 `arp -a` 并按回车键。

   注意：在 Windows 上，标志是 `-a`（带连字符）。在 Linux/macOS 上，`-a` 以另一种（BSD 风格）格式显示，但它被广泛使用且功能相同。

### 输出示例

- **在 Windows 上**：

  ```
  Interface: 192.168.1.100 --- 0x3
  Internet Address      Physical Address      Type
  192.168.1.1           aa-bb-cc-dd-ee-ff     dynamic
  192.168.1.10          11-22-33-44-55-66     dynamic
  ```

- **在 Linux/macOS 上**：

  ```
  ? (192.168.1.1) at aa:bb:cc:dd:ee:ff [ether] on en0
  ? (192.168.1.10) at 11:22:33:44:55:66 [ether] on en0
  ```

### 输出解释

- **IP Address** (例如 192.168.1.1)：设备的网络地址。
- **Physical/MAC Address**：设备网络接口的硬件地址（唯一标识符）。
- **Type**：通常为 "dynamic" (自动学习) 或 "static" (手动添加)。
- **Interface**：你计算机上的网络适配器（例如 Wi-Fi 或 Ethernet）。

### 常用选项

- 查看特定 IP 的 entry：`arp -a <IP-address>` (Windows) 或在类 Unix 系统上指定 hostname。
- 查看特定接口：在 Windows 上使用 `-N <interface-IP>`。

### 提示

- 缓存是临时的，会自动更新。
- 如果缓存为空，可以尝试先 ping 网络上的设备（例如 `ping 192.168.1.1`）来填充缓存。
- 获取更多详情，请运行 `arp /?` (Windows) 或 `man arp` (Linux/macOS)。

此命令适用于 Windows、Linux 和 macOS，其语法和输出格式略有不同。

References:

- [Microsoft Learn: arp command](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/arp)
- [GeeksforGeeks: arp command in Linux](https://www.geeksforgeeks.org/linux-unix/arp-command-in-linux-with-examples/)
- [Meridian Outpost: ARP Tutorial](https://www.meridianoutpost.com/resources/articles/command-line/arp.php)
