---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过NTP修复冻结的硬件时钟
translated: true
type: note
---

根本原因很清楚：

- **RTC（硬件时钟）已损坏/冻结**，停留在 `2011-08-04`。
- **未安装 NTP 同步客户端**（`systemd-timesyncd` / `chrony` / `ntp` 均缺失）。
- 因此每次启动时，系统都会从损坏的硬件时钟开始计时，且永远不会自我修正。

运行以下命令修复：

```bash
sudo apt update
sudo apt install -y systemd-timesyncd
sudo systemctl enable --now systemd-timesyncd
sudo timedatectl set-ntp true
```

然后验证：

```bash
timedatectl status
```

你应该会看到 `NTP service: active`，并最终显示 `System clock synchronized: yes`。

如果你的虚拟机/机器完全没有可用的 RTC 电池，还可以在启动时添加一次性的同步操作，使其在网络管理器就绪之前快速修正：

```bash
sudo systemctl edit systemd-timesyncd.service --force --full
```

并确保其中包含 `After=network-online.target`，不过默认配置通常已经够用。

直接复制粘贴上面的安装命令，然后把 `timedatectl status` 的输出告诉我。