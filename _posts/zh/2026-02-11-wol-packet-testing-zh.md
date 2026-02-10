---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 测试 WoL 数据包到达的方法
translated: true
type: note
---

**Question:** 如何测试 Wake-on-LAN？具体来说，如果我手动打开电脑，该如何检查 Magic Packets 是否确实到达了它？

**Answer:**

以下是验证 Wake-on-LAN Magic Packets 是否到达目标计算机（在已开机状态下）最实用且可靠的方法：

### 1. 最好且最直接的方法：在目标计算机上使用 Packet Capture
当 PC 处于开机并连接状态时：

**Windows**
- 安装 Wireshark（免费）
- 在 Ethernet 接口上开始抓包
- 使用 Capture Filter：`udp port 7 or udp port 9 or eth.dst == ff:ff:ff:ff:ff:ff`
- 从另一台设备发送 Wake-on-LAN Packet
- 查找包含你的 MAC 地址（在 6 字节的 FF:FF:FF:FF:FF:FF 之后重复 16 次）的数据包

**Linux / macOS**
```bash
# 快速单行命令（显示包含你 MAC 地址的 Magic Packets）
sudo tcpdump -i eth0 -n -v ether dst ff:ff:ff:ff:ff:ff and udp port 7 or udp port 9

# 或完整捕获并使用 grep（推荐方式）
sudo tcpdump -i eth0 -w wol-test.pcap ether dst ff:ff:ff:ff:ff:ff
# 然后运行：
tcpdump -r wol-test.pcap -X | grep -A 2 -B 2 "FF FF FF FF FF FF"
```

你应该会看到类似以下内容：
```
FF FF FF FF FF FF  04 7c 16 d9 54 5b  ...  04 7c 16 d9 54 5b  （重复 16 次）
```

如果你看到这个模式 → 说明 Magic Packet **正到达 NIC**。

### 2. 快速方法 —— 检查 Link/Activity LED 状态（适用于许多 NIC）
- 将电脑置于睡眠 (S3) 或休眠 (S4) 状态 —— 如果你的 BIOS/NIC 仅在引导后监听 S5，则**不要**完全关机
- 发送 WoL Packet
- 观察电脑上的 Ethernet 端口 LED：
  - 许多 NIC（特别是 Realtek 和部分 Intel）在接收并识别到正确的 Magic Packet 时，会**短暂闪烁**或改变模式 0.5–2 秒 —— 即使电脑由于 BIOS 设置或电源策略没有实际唤醒
  - 这不是 100% 可靠的，但这是一个非常快速的“它到达了吗？”的指示器

### 3. 通过驱动程序 / OS 启用 WoL 日志（较少见但非常整洁）
**Windows（部分 Intel 和 Realtek 驱动）：**
- Device Manager → Network adapters → 你的 Ethernet → Properties → Advanced
- 查找：“Wake on Magic Packet”、“Wake on Pattern Match”、“Energy Efficient Ethernet” → 确保已启用
- Advanced → “Log Wake Source” 或类似项（某些驱动程序提供此功能）
- Event Viewer → Windows Logs → System → 查找来源为 “e1dexpress” / “Netwtw” / “rt640x64” 且包含 “Wake” 或 “Magic Packet” 的事件

**Linux：**
```bash
# 显示 WoL 状态
ethtool eth0 | grep -i wake

# 启用 Magic Packet 日志记录（需要 Kernel 支持）
echo 1 > /sys/class/net/eth0/device/power/wol_reason_log  # 并非所有驱动都可用

# 或在开机状态发送数据包后监控 dmesg
dmesg -w | grep -i "magic\|wol\|wake"
```

### 4. 最简单的测试流程（推荐的实际演练方法）
1. 正常启动电脑
2. 从另一台机器每隔 10–15 秒发送一次 WoL Packets（你的 Python 脚本即可）
3. 在目标 PC 上运行 Wireshark 或带有上述过滤器的 tcpdump
4. 确认数据包到达 → 此时你确定网络路径是正确的
5. 将 PC 关机 / 睡眠
6. 再次发送 → 如果它被唤醒 → 说明整个 End-to-End 流程都在工作

### 总结 – 快速决策树

| 目标                              | 推荐方法                             | 可靠性      |
|-----------------------------------|--------------------------------------|-------------|
| 证明数据包到达 NIC                | Wireshark / tcpdump 捕获             | ★★★★★      |
| 快速视觉检查                      | 观察 Ethernet LED 闪烁               | ★★★☆☆      |
| 确认 OS 识别到唤醒原因            | Event Viewer / dmesg                 | ★★★★☆      |
| 完整的 End-to-End 测试            | 开机时捕获 → 然后睡眠 → 唤醒         | ★★★★★      |

大多数人发现步骤 1（在 PC 开机时抓包）是回答“Magic Packet 是否到达了电脑？”最快的方法。

**References:**

- [https://wiki.wireshark.org/WakeOnLAN](https://wiki.wireshark.org/WakeOnLAN)
- [https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software](https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-pci-express-software)
- [https://man7.org/linux/man-pages/man8/ethtool.8.html](https://man7.org/linux/man-pages/man8/ethtool.8.html)