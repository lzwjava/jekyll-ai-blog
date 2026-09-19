---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主板阻止GPU内存映射
translated: true
type: note
---

重要发现：我们刚诊断的那台机器**确实**是那块主板。DMI数据如下：

```
bios_vendor  : American Megatrends Inc.
bios_version : 4.6.5
bios_date    : 12/09/2016
board_name   : SY-B85N FS        <-- 梅捷 SY-B85N
```

而内核日志则明确给出了P100无法工作的原因：

```
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: can't assign; no space
pci 0000:00:01.0: bridge window [mem size 0x402000000 64bit pref]: can't assign; no space
pci 0000:01:00.0: BAR 1 [mem size 0x400000000 64bit pref]: failed to assign
pci_bus 0000:00: Some PCI device resources are unassigned, try booting with pci=realloc
```

`0x400000000` = **16 GB**。P100的BAR1是一个16 GB的*64位预取* BAR。BIOS从未在4 GB以上创建64位MMIO窗口，因此内核无处安放它。只有BAR0（16 MB）被分配了——所以出现`BAR1 is 0M @ 0x0`并导致驱动探测失败循环。

## 回答你的问题

**Resizable BAR：这块主板不可能支持。句号。**
Resizable BAR需要芯片组/固件支持，而这一支持在英特尔400系列/第10代（约2020年）才出现。Haswell + B85（2014）比它早了六年。BIOS中没有选项，也无法通过跨刷或修改来添加，因为芯片路径根本不存在。（注：P100 *GPU* 端是支持的，因为它是Pascal架构——*平台*才是障碍所在。）

**Above 4G Decoding：这里唯一重要的就是它**——这也是你需要寻找的选项。

### 1. 检查BIOS（启动时按Del键）

B85主板上的AMI BIOS 4.6.5——如果有该选项，通常位于以下路径之一：

```
Advanced → PCI Subsystem Settings → Above 4G Decoding        （最可能的位置）
Chipset   → PCH-IO Configuration  → Above 4G Decoding
Chipset   → System Agent (SA) Config → Above 4G Decoding
Advanced  → PCI Express Configuration
```

此外，请确保**CSM已禁用**，系统以纯UEFI模式启动（这里已经做到了——`/sys/firmware/efi`存在）。Above 4G Decoding是UEFI特性，在传统模式下会被忽略。

**做好它不存在的准备。** B85时代的AMI BIOS通常根本不含此选项。如果它存在，启用它，保存，重启，搞定。如果它*不*存在，你无法将其隐藏——也没什么可隐藏的，因为固件中用于>4 GB MMIO分配的代码路径从未被编译进去。（你可以验证：导出BIOS并运行`strings bios.bin | grep -i "above 4g"`。没有结果 = 固件中不存在该设置对象。）

### 2. 可以先免费尝试——内核端realloc

内核本身就建议了这一点，所以在购买任何东西之前先测试：

```bash
sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pci=realloc pci=nocrs"/' /etc/default/grub
sudo update-grub && sudo reboot
```

然后检查BAR1是否获得了地址：

```bash
lspci -vv -s 01:00.0 | grep -i region      # 期望看到 Region 1 带有真实地址
journalctl -b -k | grep -i "BAR 1"          # 不应再显示 "failed to assign"
```

**预期放低：** `pci=realloc` 只能重新分配ACPI host bridge向OS声明的空间。如果BIOS从未声明64位窗口（这正是"没有Above 4G Decoding"的含义），那么16 GB请求仍然无法放入4 GB以下，会继续失败。`pci=nocrs`有时能让内核更努力地探测。测试只需约5分钟，且零成本。

### 3. 如果BIOS没有Above 4G Decoding

那么这块主板根本无法承载这张卡。你的实际出路：

- **换平台。** X99/C612工作站主板，或较新的消费级主板（厂商已提供Above 4G Decoding的，例如许多B450/B550/Z390/Z490主板、华擎H110 Pro BTC+等）。几乎所有Haswell/B85主板都缺少此功能。
- **在这台机器上放弃使用P100。** 保留Intel iGPU用于显示，把机器当作普通桌面/NAS使用。

### 4. 即使用P100能在这台机器上工作，也需正视现实

即使BAR1分配成功，这个组合也存在严重问题：

| 问题 | 详情 |
|---|---|
| **散热** | P100是*被动散热*的Tesla卡，专为1U/2U服务器风道设计。在开放式桌面环境中会过热并降频/关机；需要导流罩+高静压风扇。 |
| **电源接口** | Tesla P100 PCIe使用**8-pin CPU/EPS接口**，*不是* PCIe 8-pin。使用PCIe线缆会导致无法启动或损坏风险。250W TDP。 |
| **主机内存** | 你有**3.2–4 GB**。一张16 GB的CUDA卡搭配4 GB主机内存，不是一个可用的计算主机。 |
| **无显示输出** | Tesla卡没有视频输出口（这里没关系，iGPU负责显示）。 |
| **PCIe** | i5-4460提供PCIe 3.0 x16——可以接受，但整体搭配不匹配。 |

## 结论

- **Resizable BAR：** B85上不可能——别浪费时间了。
- **Above 4G Decoding：** 在AMI BIOS的`Advanced → PCI Subsystem Settings`下寻找。如果存在，启用它→16 GB的BAR1将被映射，驱动循环停止。如果不存在，这块主板无法实现，`pci=realloc`/`pci=nocrs`是你唯一（希望不大的）免费尝试。
- **另外，无论GPU如何：** 这台机器的缓慢主要由那7200 RPM机械硬盘 + 4 GB内存 + NVIDIA重试风暴导致。禁用`nvidia-persistenced`立即停止CPU消耗，而P100无法使用意味着你应该屏蔽`nvidia`并继续前行。

需要我接下来（a）应用`pci=realloc`/`pci=nocrs`启动参数测试，并（b）在该主机上禁用`nvidia-persistenced`重试循环吗？我需要你的sudo密码才能进行GRUB/systemd修改。