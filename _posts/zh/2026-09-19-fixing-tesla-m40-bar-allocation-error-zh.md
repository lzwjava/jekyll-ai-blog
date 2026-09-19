---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复特斯拉M40 BAR分配错误
translated: true
type: note
---

问题：如何在搭载AMD A4-5000 / 速龙X4 850的华硕A68HM-E上修复Tesla M40的BAR分配失败？

回答：

你的主板和CPU使情况发生了显著变化。让我重新诊断：

---

## 修订后的硬件配置

| 项目 | 详情 |
|---|---|
| 主板 | 华硕A68HM-E（AMD FM2+插槽） |
| CPU | 速龙X4 850（Kaveri/Godavari，FM2+） |
| 芯片组 | AMD A68H（Bolton D2） |
| PCIe | 来自APU本身的Gen 2.0 x16 |
| GPU | Tesla M40 12 GB（需要16 GiB可预取BAR） |

---

## 核心问题比之前更严重

AMD A68H平台比Intel B150的限制更严格：

**1. 4G以上解码——很可能缺失或损坏**
A68HM-E的BIOS选项非常有限。华硕很少在入门级FM2+主板上暴露4G以上解码选项。即使该选项存在，速龙X4 850（无核显的非APU版本）意味着PCIe BAR窗口预算完全被M40占用——没有其他设备共享，但固件仍然不会在没有明确支持的情况下在4G以上分配16 GiB窗口。

**2. PCIe Gen 2.0 x16带宽**
M40可以运行，但带宽会降低（Gen 2 x16 ≈ 8 GB/s vs Gen 3 x16 ≈ 16 GB/s）。这不是阻碍，只是提醒。

**3. 速龙X4 850没有集成显卡**
这其实没问题——M40本来就没有显示输出。但这意味着你需要确认有单独的显示卡，或者正在无头模式下运行。

---

## 按顺序尝试以下方法

### 步骤 1 — 检查BIOS版本和4G以上选项

进入BIOS（按Del键）并查看：

```
高级 → 系统代理配置 → 4G以上内存/加密货币挖矿
```
或
```
高级 → PCIe配置 → 4G以上解码
```

华硕有时会隐藏该选项。如果找不到，请先更新BIOS。

检查当前BIOS版本：
```bash
sudo dmidecode -s bios-version
```

然后查看华硕A68HM-E的支持页面获取最新BIOS——后续版本有时会解锁此选项。

---

### 步骤 2 — Linux内核启动参数解决方法

如果BIOS中没有4G以上解码选项，请尝试从内核端强制启用。编辑GRUB：

```bash
sudo nano /etc/default/grub
```

将这一行：
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```
改为：
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pci=realloc=on memmap=16G!4G"
```

然后：
```bash
sudo update-grub
sudo reboot
```

重启后，检查BAR是否已分配：
```bash
sudo lspci -v -s 01:00.0 | grep -i "memory\|prefetch\|bar"
```

---

### 步骤 3 — 安装驱动程序（无论如何都要执行）

即使BAR问题未解决，也要安装驱动程序，以便BAR问题修复后立即可用：

```bash
sudo apt update
sudo apt install build-essential dkms linux-headers-$(uname -r)
sudo apt install nvidia-driver-580
echo -e "blacklist nouveau\noptions nouveau modeset=0" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
sudo update-initramfs -u
```

然后重启。

---

### 步骤 4 — 重启后验证

```bash
nvidia-smi
```

如果仍然显示"未找到设备"，说明BAR仍未分配。检查：
```bash
sudo dmesg | grep -i "bar\|pci\|nvidia\|nouveau"
```

---

## 实事求是的评估

| 场景 | 结果 |
|---|---|
| BIOS中有4G以上选项 | 启用它 → M40可以工作 |
| BIOS已更新，选项出现 | 启用它 → M40可以工作 |
| 任何地方都没有4G以上选项，内核解决方法有效 | M40可以工作 |
| 以上都不行 | M40无法在此主板上初始化 |

A68HM-E是大约2014年的入门级micro-ATX主板。Tesla M40是一款期望服务器级固件的数据中心GPU。**如果没有支持4G以上解码的BIOS，这个组合确实有可能根本无法工作。**

---

## 关于sudo密码

我不能也不应该直接询问你的sudo密码——请自己在终端中运行上述命令。如果你想让我帮助解读任何输出，请粘贴到这里，我会指导你进行下一步。