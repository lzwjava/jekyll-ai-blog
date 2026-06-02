---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 通过蓝牙命令行配对罗技键盘
translated: true
type: note
---

### 前置准备

- 确保您的蓝牙5.3发射器（适配器）已插入USB 3.0端口并被Ubuntu识别。在终端运行 `lsusb` 检查是否显示（查找"Bluetooth"或供应商ID）。若未识别，请尝试更换USB端口或重启系统。
- 如未安装蓝牙工具，请执行：

  ```
  sudo apt update
  sudo apt install bluez bluetooth bluez-tools
  ```

- 必要时解除蓝牙屏蔽：

  ```
  rfkill unblock bluetooth
  ```

- 重启蓝牙服务：

  ```
  sudo systemctl restart bluetooth
  ```

### 使用bluetoothctl配对步骤（推荐CLI方式）

`bluetoothctl` 是Linux/Ubuntu管理蓝牙的标准工具。罗技键盘（如MX Keys、K380等型号）通常需要在物理键盘上输入配对PIN码。

1. **启动蓝牙控制台**：

   ```
   bluetoothctl
   ```

   此时将进入交互模式（提示符变为 `[bluetooth]#`）

2. **启用适配器**：

   ```
   power on
   ```

   （若提示"No default controller available"，可运行 `list` 查看适配器，多适配器时需执行 `select <适配器MAC地址>`）

3. **设置配对代理**：

   ```
   agent on
   default-agent
   ```

   这将启用PIN码处理并设置当前会话为默认配对代理

4. **开始扫描设备**：

   ```
   scan on
   ```

   保持扫描状态。约10-20秒后您的罗技键盘会显示（如"Logitech K380"等名称，附带MAC地址 `XX:XX:XX:XX:XX:XX`）

5. **将罗技键盘设为配对模式**：
   - 开启电源（如有独立开关）
   - 长按蓝牙配对键（通常位于侧面或顶部，多设备型号如MX Keys需长按1/2/3通道键3-5秒直至LED快闪）
   - 单设备型号直接长按主配对键

6. **配对设备**：
   扫描到设备后（按Enter刷新显示），执行：

   ```
   pair <MAC地址>
   ```

   - 示例：`pair 12:34:56:78:9A:BC`
   - Ubuntu将提示输入PIN码（罗技设备常为0000或1234，可先尝试默认值）
   - **罗技设备关键步骤**：在物理键盘上直接输入PIN码并按Enter键（若无GUI弹窗提示，此操作至关重要——部分用户需通过 `gnome-control-center` > 通知启用系统通知，但CLI方式通常可绕过此问题）

7. **信任并连接**：

   ```
   trust <MAC地址>
   connect <MAC地址>
   ```

   - 此操作将实现后续自动连接

8. **退出控制台**：

   ```
   exit
   ```

### 故障排除

- **设备未扫描到**：确认键盘处于配对模式（LED闪烁）。运行 `scan off` 后重新执行 `scan on`，最多等待30秒
- **配对失败（如"AuthenticationCanceled"）**：先移除设备（`remove <MAC地址>`）后重试。顽固型号可尝试长按配对键或切换通道键
- **无PIN码提示**：部分键盘无需PIN码可直接连接。若卡顿可查看日志：配对时运行 `sudo journalctl -u bluetooth -f`
- **适配器问题**：若使用USB蓝牙5.3适配器，请确认内核支持（Ubuntu 22.04+对BT 5.3兼容良好）。旧版系统可更新内核：`sudo apt install linux-generic-hwe-22.04`
- **图形界面替代方案**：打开设置 > 蓝牙，启用后通过图形界面配对——但CLI方式对罗技设备兼容性更佳
- **功能测试**：配对成功后在终端输入测试。若正常使用，可通过 `bluetoothctl` 或crontab设置开机自动连接

若您的特定罗技型号（如MX Keys Mini）存在特殊问题，请提供具体型号以获取针对性指导。

### 参考文档

- [在Ubuntu 20.04中配对LOGITECH K380](https://unix.stackexchange.com/questions/590221/pairing-logitech-k380-in-ubuntu-20-04)
- [罗技MX Keys无法通过蓝牙配对](https://askubuntu.com/questions/1270419/20-04-logitech-mx-keys-wont-pair-with-bluetooth)
- [通过蓝牙将罗技MX Keys与Xubuntu配对](https://zroupas.github.io/linux/2021/08/25/pair_mxkeys_xubuntu_bt.html)
- [Ubuntu 20.04无法配对蓝牙键盘](https://askubuntu.com/questions/1398096/ubuntu-20-04-cannot-pair-bluetooth-keyboard)
