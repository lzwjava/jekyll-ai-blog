---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Ubuntu 不显示 WiFi 的问题
translated: true
type: note
---

Ubuntu 中 "WiFi doesn't show"（设置中未列出网络、顶部状态栏没有 WiFi 图标或提示 "No WiFi adapter found"）是一个非常常见的问题。这可能由以下原因引起：

- 硬件/rfkill 开关已关闭
- Driver/firmware 未正常加载
- NetworkManager 服务故障（在 24.04+ 版本更新/重启后非常频繁）
- Interface 处于 down 状态或未被托管 (unmanaged)
- 升级后 Kernel/driver 不匹配

请按照以下排查步骤**依次**在 terminal 中执行（按 Ctrl+Alt+T 打开）。每运行一步后，请检查 Settings → Wi-Fi 或顶部状态栏下拉菜单中是否出现了 WiFi。

### 1. 快速重启（可解决约 50–60% 的案例）

```bash
# 重启 NetworkManager 服务
sudo systemctl restart NetworkManager

# 或者完全 停止/启动
sudo nmcli networking off
sudo nmcli networking on

# 强制 WiFi 重新扫描
nmcli device wifi rescan
nmcli device wifi list
```

完成后，打开 Settings（或运行 `gnome-control-center wifi`）查看网络是否出现。如果没有，执行下一步。

### 2. 检查 WiFi 是否被锁定（硬件开关 / soft block – 非常常见）

```bash
rfkill list all
```

查找 **Wireless LAN** 相关行。

- 如果显示 **Soft blocked: yes** → 使用以下命令修复：
  ```bash
  rfkill unblock wifi
  rfkill unblock all
  ```

- 如果 **Hard blocked: yes** → 这通常是笔记本电脑上的物理开关或 Fn + F键（飞行模式键）。按下它进行切换（寻找功能键上的 WiFi/天线图标）。

再次运行 `rfkill list` 确认两者均为 **no**。

### 3. 检查 WiFi adapter 是否被检测到

```bash
# 推荐命令 – 显示 interface 名称（通常为 wlpXs0 或 wlan0）
ip link show | grep -i wl

# 或者查看更详细信息
sudo lshw -C network | grep -i wireless -A 12

# 备选命令
lspci | grep -i network  # 或 grep -i wireless
# 对于 USB WiFi 适配器：lsusb | grep -i wireless
```

- 如果看到了你的 WiFi 卡（例如 Intel, Realtek, Qualcomm Atheros）→ 很好，继续。
- 如果什么都没有或者旁边显示 "**UNCLAIMED**" → driver 问题（直接跳到第 7 步）。
- 记下 interface 名称（例如 `wlp2s0`）备用。

### 4. 手动启用 interface

将 `wlp2s0` 替换为你从第 3 步中获得的 **你的** interface 名称。

```bash
sudo ip link set wlp2s0 up
nmcli device wifi rescan
nmcli device wifi list
```

### 5. 重新安装 NetworkManager（解决更新后 GUI/图标消失的常见问题）

```bash
sudo apt update
sudo apt install --reinstall network-manager network-manager-gnome
sudo systemctl restart NetworkManager
```

然后注销并重新登录（或重启）。

### 6. 如果仍然无效 – 检查 kernel 消息寻找线索

```bash
dmesg | grep -i -E 'wlan|wifi|iwlwifi|rtl|ath|brcm|firm|error'
```

常见错误：

- "firmware load failed" → 缺少 firmware（例如对于 Intel）：
  ```bash
  sudo apt install linux-firmware
  sudo update-initramfs -u
  sudo reboot
  ```

- iwlwifi 或 Realtek 问题 → 有时 卸载/重载 会有帮助：
  ```bash
  sudo modprobe -r iwlwifi    # 或 rtl8723be / 对应你 driver 的名称
  sudo modprobe iwlwifi
  ```

### 7. 如果检测到了适配器但依然没有网络 / "No WiFi adapter found"

- 尝试在设置中切换飞行模式（或运行 `nmcli radio wifi off && nmcli radio wifi on`）
- 如果你最近进行了更新，尝试启动 **旧版本 kernel**（启动时按住 Shift → Advanced → 选择旧版本 kernel）
- 在极少数情况下（升级损坏），进入 **recovery mode**（按住 Shift → Advanced → Recovery）：
  - 选择 "network" 以启用网络
  - 选择 "dpkg" 以修复损坏的包
  - 恢复正常启动 (Resume)

### 如果以上方法都无效

运行以下命令并将输出结果粘贴反馈（复制完整的运行结果）：

```bash
rfkill list all
ip link show
sudo lshw -C network
lspci | grep -i network
nmcli device status
nmcli radio
```

同时请告诉我：

- 你的 Ubuntu 版本（`lsb_release -a`）
- 笔记本品牌/型号（或已知的 WiFi 卡型号）
- 之前是否正常工作 / 还是在更新/全新安装后出现的？

大多数情况可以通过第 1–5 步解决。请告诉我你的排查结果！
