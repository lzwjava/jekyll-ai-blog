---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Debian timedatectl NTP不支持修复
translated: true
type: note
---

问题：Debian 提示 `timedatectl set-ntp true` 不受支持。

回答：这通常是因为**没有安装/运行 NTP 同步服务**。`timedatectl` 本身不一定提供 NTP。

首先检查：

```bash
timedatectl
```

以及：

```bash
systemctl status systemd-timesyncd
```

### 如果 `systemd-timesyncd` 存在

尝试：

```bash
sudo systemctl enable --now systemd-timesyncd
sudo timedatectl set-ntp true
```

然后：

```bash
timedatectl
```

### 如果 `systemd-timesyncd` 未安装

鉴于你的 Debian 安装当前似乎只有有限的 APT 仓库，你可以暂时**手动设置时钟**：

```bash
sudo timedatectl set-timezone Asia/Shanghai
sudo timedatectl set-time '2026-09-02 03:12:00'
```

检查：

```bash
date
timedatectl
```

修复好 APT 仓库配置后，安装 NTP 客户端。我会使用 `chrony`：

```bash
sudo apt update
sudo apt install chrony
sudo systemctl enable --now chrony
```

然后：

```bash
chronyc tracking
```

你应该会看到有效的 `Reference ID` 以及较小的 `System time` 偏差。

**鉴于你当前的状况，我建议先修复 APT。** 一旦 `apt install openssh-server` 能正常工作，安装 `chrony` 也就没问题了。
