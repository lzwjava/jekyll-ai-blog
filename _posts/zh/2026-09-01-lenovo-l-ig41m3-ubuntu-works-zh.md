---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想 L-IG41M3 Ubuntu 版
translated: true
type: note
---

问题：联想 L-IG41M3 主板搭载 2.6 GHz Intel Celeron 处理器和 4 GB 内存，能否运行 Ubuntu？

答案：**完全可以。** 实际上，这台机器对于学习 Linux、硬件维修和基础服务器工作来说相当合适。

![Image](https://images.openai.com/static-rsc-4/gLr_nekYjGSVOewKFfRh_Q-d7p1zn-5ONOR7PS5QKNPCgtSPeUwhrCMBWzQeZs2v7y2vvd9gLh_l849Zm_PGCHLnFa7Vbmg81YyHi0fgXjYB0K-f9qZ-YlZwr5ulbCMjsGVJrVPQNIU9wCof718FSDRHKp8L65SxHlcJC7ixWM6uc3QMGU9LiBdFbr7jlNwr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/u3Ka0dM4FQLzlsVwbjOhVPbHn632SFKc5_Dr_mTvXF79t7gi685mCP3ojCEeAqLGMNSAt1fy_Kdr0CSFgJfZx-coDBDWDzGuJ_ukS1zIiembRj94htwwcM2Jn6WPbPTDx7craF8PZ91o9h59oBWL25ssS6z5FF2RvLfLlr2AT6PsnFq10zpn7B-D5V6Q8y47?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WipbCJXf3T_LYM7cgiIxvHbGmdyKDbMLrJ8ehILkKrY_TfJeWkaklgs-mXSLp2LFgAEkzvdHOdznoFVI-GmisodA7cF6AIUlFsueXjdmVsEutaBo2TxyXr9Ie_6BQ4o2X7nMApjA7E1OHciPyR7AH-ZZTuK9q7hymntwsvTaSe33RCmq9hgnjU5Bc3saJkMW?purpose=fullsize)

### 期望表现

如果是常见的 **G41 时代联想平台**，2.6 GHz 的 Celeron 很可能是较老的 64 位 Intel CPU。关键问题是具体 CPU 是否支持 **Intel 64**。

从现有 Linux 系统检查：

```bash
lscpu | grep -E 'Architecture|CPU'
```

你希望看到：

```text
Architecture: x86_64
```

关于 **4 GB 内存**：

| Ubuntu 版本          | 建议                     |
| -------------------- | ------------------------ |
| Ubuntu 24.04 桌面版  | ⚠️ 可用，但速度很慢       |
| Ubuntu 24.04 服务器  | ✅ 良好                   |
| Ubuntu 最小化 + XFCE | ✅ 非常好                 |
| Lubuntu              | ✅ 可能是最佳 GUI 选择    |
| Debian + XFCE        | ✅ 优秀                   |

对于这套硬件，我个人会安装 **Lubuntu 或 Debian XFCE**，而不是标准 Ubuntu GNOME。

### 对你的 GPU 维修工作更友好

这台旧机器可以作为 **专用的硬件测试工具箱**：

```text
L-IG41M3
    │
    ├── 4 GB 内存
    ├── 廉价 SATA SSD
    ├── Linux
    │
    ├── GPU PCIe x16
    │      └── 测试显卡
    │
    └── SSH
           └── 你的主力 Mac / PC
```

许多维修任务并不需要强力的 CPU。主要需要的是：

* PCIe 插槽正常工作
* 稳定的电源
* SATA SSD
* 能启动 Linux
* `lspci`
* `dmesg`
* `lspci -vv`
* 测试 NVIDIA 显卡时的 `nvidia-smi`

例如：

```bash
sudo apt update
sudo apt install pciutils
lspci -nn
lspci -nnk
dmesg | grep -iE 'pci|nvidia|amdgpu'
```

**有一点需要注意：** 如果你专门为了测试现代 NVIDIA 显卡而购买这块主板，G41 平台*非常*老旧。它仍然可以作为基础的 PCIe 测试平台使用，但对于你的 GPU 维修工作，我更推荐 **H81 + 第四代 Intel CPU + 4–8 GB 内存** 的机器。