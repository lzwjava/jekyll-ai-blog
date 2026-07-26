---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想USB问题修复方案
translated: true
type: note
---

USB 尚未检测到——请插入 USB，我会继续操作。

在此期间，以下是修复方案：

### 联想小新无法识别的原因

| 原因 | 修复方法 |
| --- | --- |
| **MBR 分区类型**（Ventoy 默认） | 使用 `-g` 参数重新安装 → **GPT** |
| **Secure Boot** 阻止未签名的引导程序 | 在 BIOS 中禁用，或使用 `-S` 重新安装 Ventoy（无需 Secure Boot） |

### 修复步骤（插入 USB 后执行）

```bash
sudo /tmp/ventoy-1.1.17/Ventoy2Disk.sh -I -g /dev/sdb   # 强制安装 GPT
```

然后重新复制 ISO 文件即可。

另外，在联想 BIOS 中：

- 开机按 **F2** → **Security** 选项卡 → **Secure Boot** → **Disabled**
- **Boot** 选项卡 → **Boot Mode** → **UEFI**（不要选 Legacy）
- 保存并退出 → 按 **F12** → USB 应该会显示

插入 USB，我会执行。
