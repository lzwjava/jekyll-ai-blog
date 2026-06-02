---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决罗技蓝牙配对问题
translated: true
type: note
---

### 排查 AuthenticationCanceled 错误

该错误常见于罗技蓝牙键盘（您的 MAC 地址 `F4:73:35:78:28:4E` 与罗技的 OUI 前缀匹配）在 Ubuntu 配对过程中，通常由认证超时、缺少 PIN 码提示或 BlueZ 中的代理处理问题导致。日志中短暂的连接/断开表明键盘有响应，但流程在完成前超时。其他设备（如 `54:2B:FC:F1:1C:D8`）可能出现干扰——请先清除它们。

#### 快速准备步骤

1. **移除所有已配对设备** 以避免冲突：
   在 `bluetoothctl` 中，运行 `devices` 列出设备，然后对每个设备执行 `remove <MAC>`（例如 `remove 54:2B:FC:F1:1C:D8`）。使用 `exit` 退出。

2. **重启蓝牙服务**：

   ```
   sudo systemctl restart bluetooth
   sudo systemctl status bluetooth  # 验证服务处于活跃状态
   ```

3. **将键盘置于配对模式**：长按配对按钮（如 Easy-Switch 通道或蓝牙按钮），直到 LED 快速闪烁。每次尝试前都需重新操作。

#### 在 bluetoothctl 中增强配对步骤

重新打开 `bluetoothctl` 并严格按以下步骤操作——代理设置至关重要，先执行信任操作通常能绕过某些超时。对于罗技型号（如 K380、K480、MX Keys），在 `pair` 命令后立即在物理键盘上盲输任意 PIN 码（屏幕上无回显）。

1. **进入 bluetoothctl**：

   ```
   bluetoothctl
   ```

2. **开启电源并设置代理**：

   ```
   power on
   agent on
   default-agent
   ```

3. **扫描并确认设备**：

   ```
   scan on
   ```

   等待 `F4:73:35:78:28:4E` 出现（如有需要可按 Enter 刷新）。然后：

   ```
   scan off  # 停止扫描以集中注意力
   ```

4. **信任设备**（有助于重新连接时自动接受）：

   ```
   trust F4:73:35:78:28:4E
   ```

5. **配对**：

   ```
   pair F4:73:35:78:28:4E
   ```

   - 如果出现 PIN 码/通行密钥（例如 `[agent] PIN code: 390412` 或 `[agent] Passkey: 299595`），立即在物理键盘上输入并按 Enter。请盲输——即使没有活跃提示。
   - 如果未显示 PIN 码（某些罗技设备常见），尝试在键盘上输入 `0000` 或 `1234` 并按 Enter。
   - 观察 `[CHG] Paired: yes`。如果短暂连接后断开，立即重新运行 `connect F4:73:35:78:28:4E`。

6. **连接并信任**：

   ```
   connect F4:73:35:78:28:4E
   trust F4:73:35:78:28:4E  # 如果之前未执行
   ```

7. **退出并测试**：

   ```
   exit
   ```

   打开文本编辑器或终端——输入文字进行验证。如果成功，唤醒时应自动重连。

#### 如果仍然失败

- **图形界面回退方案**：使用 Ubuntu 设置 > 蓝牙（切换开启，选择设备）。这通常会显示可见的 PIN 码提示。如果命令行代理失败，图形界面的 pinentry 处理效果更好。
- **盲输 PIN 码重试**：即使没有显示代码，部分用户通过在 `pair` 后立即输入 `0000` + Enter 成功——键盘会静默完成认证。
- **查看日志线索**：在配对期间于另一个终端运行 `sudo journalctl -u bluetooth -f`。查找 "PIN code" 或超时信息。
- **更新 BlueZ**：确保使用最新版本（Ubuntu 24.04+ 搭载 BlueZ 5.72+，对罗技支持更好）：

  ```
  sudo apt update && sudo apt upgrade bluez
  ```

- **USB 适配器特性**：您的 USB 3.0 接口 BT 5.3 发射器正常，但可在 USB 2.0 端口测试——偶有干扰报告。
- **型号特定操作**：如果是 K480/MX Keys，长按配对按钮 5 秒以上。对于多设备键盘，先切换到未使用的通道。

以上步骤应能解决问题——多数罗技案例源于盲输 PIN 码步骤。如果您提供具体型号或完整日志，我可进一步优化建议。

[蓝牙配对 - AuthenticationCanceled (AskUbuntu)](https://askubuntu.com/questions/1373574/bluetooth-pairing-authenticationcanceled)
[[已解决] 蓝牙键盘：无法配对 (Arch Linux 论坛)](https://bbs.archlinux.org/viewtopic.php?id=174239)
[BlueZ 5.72 勉强配对 Logitech K480 (GitHub)](https://github.com/bluez/bluez/issues/654)
