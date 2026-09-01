---
audio: false
generated: true
image: false
lang: zh
layout: post
title: timedatectl set-time 被NTP忽略
translated: true
type: note
---

问题：`timedatectl set-time` 执行成功或看似运行，但时钟立即停留在旧时间。

答案：很可能是 **NTP 仍在控制时钟**，或者系统的时间服务将其重置了。

首先运行：

```bash
timedatectl
```

查找：

```text
NTP service: ...
System clock synchronized: ...
```

### 快速修复：关闭 NTP，然后设置时间

```bash
sudo timedatectl set-ntp false
sudo timedatectl set-time '2026-09-02 03:12:00'
date
```

如果 `set-ntp false` 提示 NTP 不受支持，请检查正在运行的时间同步服务：

```bash
systemctl list-units --type=service | grep -E 'ntp|chrony|timesync'
```

另外：

```bash
ps aux | grep -E 'ntpd|chronyd|timesyncd'
```

### 如果只想要当前正确的时间

你可以绕过 `timedatectl`：

```bash
sudo date -s '2026-09-02 03:12:00'
```

然后：

```bash
date
```

如果**连 `date -s` 也立即跳回旧时间**，说明有进程在主动同步/重置时钟。

一个重要的点：如果你只通过以下命令更改了时区：

```bash
sudo timedatectl set-timezone Asia/Shanghai
```

那么**显示的时间会根据时区偏移发生变化**，但底层的 Unix 时间戳不会改变。这与设置实际时钟不同。

请粘贴以下命令的输出：

```bash
timedatectl
systemctl list-units --type=service | grep -E 'ntp|chrony|timesync'
```

我可以准确定位是什么在覆盖你的设置。