---
audio: false
generated: true
lang: zh
layout: post
title: 修复Ubuntu系统的Wi-Fi断连问题
translated: true
type: note
---

Ubuntu系统在有线网络稳定时出现Wi-Fi断连问题，可能由多种因素导致。以下是逐步诊断与修复指南：

---

### **1. 检查驱动程序问题**

您的MSI B760M Mortar WiFi主板很可能搭载了**Intel Wi-Fi 6E AX211/AX210**无线网卡。虽然Intel驱动在Linux中通常兼容性良好，但仍可能出现问题。

#### **操作步骤：**

- **识别无线网卡芯片型号：**
  在终端执行：

  ```bash
  lspci -knn | grep -iA3 net
  ```

  查找无线网卡设备（通常显示为`Intel Corporation Device [8086:...]`）

- **检查是否正确加载驱动：**

  ```bash
  lsmod | grep iwlwifi
  ```

  若未显示内容则说明驱动未加载

- **安装/更新驱动：**
  Intel无线网卡驱动（`iwlwifi`）已包含在Linux内核中，但可能需要更新固件：

  ```bash
  sudo apt update && sudo apt install --reinstall linux-firmware
  ```

---

### **2. 关闭Wi-Fi省电模式**

Linux系统有时会过度激进的启用无线网卡省电功能，导致连接中断。

#### **操作步骤：**

- 临时禁用省电模式：

  ```bash
  sudo sed -i 's/wifi.powersave = 3/wifi.powersave = 2/' /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
  ```

  或手动检查状态：

  ```bash
  iw dev wlan0 get power_save
  ```

  （请将`wlan0`替换为`ip a`命令显示的网卡名称）

- **应用更改：**

  ```bash
  sudo systemctl restart NetworkManager
  ```

---

### **3. 检查信号干扰或路由器问题**

- **使用其他设备测试**（手机/笔记本）确认是否同样存在断连
- **更换Wi-Fi信道**（使用`iwlist`扫描拥堵信道）：

  ```bash
  sudo iwlist wlan0 scan | grep Frequency
  ```

- 尝试使用**5GHz频段**（若可用）以减少干扰

---

### **4. 禁用IPv6**

部分路由器/运营商存在IPv6兼容性问题。

#### **操作步骤：**

- 编辑`/etc/sysctl.conf`文件并追加：

  ```plaintext
  net.ipv6.conf.all.disable_ipv6=1
  net.ipv6.conf.default.disable_ipv6=1
  ```

- 应用配置：

  ```bash
  sudo sysctl -p
  ```

---

### **5. 更新内核和NetworkManager**

新版内核通常包含无线网络问题修复。

```bash
sudo apt update && sudo apt upgrade
```

如需可安装**主线内核**（例如6.5+版本）：

```bash
sudo apt install linux-image-generic-hwe-22.04
```

---

### **6. 禁用硬件加密（如适用）**

部分Intel无线网卡存在硬件加密兼容问题。
编辑`/etc/modprobe.d/iwlwifi.conf`文件（若不存在请创建）：

```plaintext
options iwlwifi 11n_disable=1
```

随后执行：

```bash
sudo modprobe -r iwlwifi && sudo modprobe iwlwifi
```

---

### **7. 检查RFKill锁定状态**

```bash
rfkill list
```

若显示无线功能被阻止（例如`soft blocked: yes`），请解除锁定：

```bash
sudo rfkill unblock wifi
```

---

### **8. 使用USB无线网卡测试**

若问题持续存在，可尝试**兼容Linux的USB无线网卡**（如TP-Link Archer T4U）以判断是否为Intel网卡硬件问题。

---

### **9. 检查系统日志错误**

```bash
journalctl -u NetworkManager --no-pager -n 50
```

查找`iwlwifi`相关错误或断连事件记录。

---

### **最终建议**

- 若以上方案均无效，可考虑**双启动Windows系统**以排除硬件故障
- 若Wi-Fi持续不稳定，可改用**USB转以太网适配器**

如需进一步调试协助，请随时告知！
