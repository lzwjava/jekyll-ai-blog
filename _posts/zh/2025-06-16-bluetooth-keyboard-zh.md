---
audio: false
generated: true
lang: zh
layout: post
title: 修复蓝牙键盘连接问题
translated: true
type: note
---

根据 `bluetoothctl` 输出显示尝试连接时出现 `[DEL] Device`，以下是精确解决方案：

### 连接删除问题的即时修复
1. **移除现有设备记录**（对陈旧配置至关重要）：
   ```bash
   bluetoothctl
   remove F4:73:35:78:28:4E  # 移除键盘
   remove 24:27:30:24:C8:31   # 移除可能产生干扰的设备
   exit
   ```

2. **重置蓝牙协议栈**：
   ```bash
   sudo systemctl stop bluetooth
   sudo rm -rf /var/lib/bluetooth/*
   sudo systemctl start bluetooth
   ```

3. **使用正确顺序重新配对**：
   ```bash
   bluetoothctl
   power on
   discoverable on
   pairable on
   agent on  # 启用密码代理
   scan on
   ```
   - **将K380置于配对模式**（LED快速闪烁）
   - 当键盘出现时：
     ```bash
     pair F4:73:35:78:28:4E
     ```
   - **立即在键盘上输入**屏幕上显示的6位密码（例如 `123456`）并按回车键

4. **仅在成功配对后连接**：
   ```bash
   connect F4:73:35:78:28:4E
   trust F4:73:35:78:28:4E
   scan off
   quit
   ```

### 问题成因
- 出现 `[DEL] Device` 是因为：
  - 蓝牙协议栈检测到连接失败并清除设备记录
  - 在连接尝试前**缺少配对步骤**
  - 可能受到其他设备（如 `midea` 设备）的射频干扰

### 额外关键检查
1. **验证天线连接**：
   - 确保蓝牙天线已旋入MSI主板后置I/O面板

2. **检查内核驱动**：
   ```bash
   dmesg | grep -i bluetooth
   ```
   查找如 `hci0: command timeout` 或 `Firmware failed to start` 等错误

3. **更新固件**（如果出现超时错误）：
   ```bash
   sudo apt install linux-firmware
   ```

4. **最小化环境测试**：
   ```bash
   sudo rfkill unblock all
   sudo systemctl stop NetworkManager  # 临时停止
   sudo systemctl restart bluetooth
   ```

### 若问题仍存在
1. **替代配对方法**（绕过代理）：
   ```bash
   echo -e 'remove F4:73:35:78:28:4E\npair F4:73:35:78:28:4E\nconnect F4:73:35:78:28:4E\ntrust F4:73:35:78:28:4E' | bluetoothctl
   ```

2. **检查键盘电池**（对蓝牙连接至关重要）：
   - 如果电压过低请更换电池（K380使用2节CR2032电池）

3. **USB蓝牙适配器测试**：
   - 如果内置蓝牙有问题，可尝试使用$10的CSR4.0 USB适配器

**预期成功指标**：
- 出现 `Pairing successful` 消息
- bluetoothctl中显示 `Connection successful`
- `dmesg` 显示 `HIDP: Bluetooth HID device driver`

配对成功后，您的K380应能保持跨重启连接。如果再次出现断开连接，请检查 `journalctl -u bluetooth -f` 获取实时错误信息。
