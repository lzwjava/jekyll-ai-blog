---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 停止 CUPS 打印服务指南
translated: true
type: note
---

**Question:** Ubuntu 中的 cups.service/stop 是什么？

**Answer:**

`cups.service/stop` 指的是在 Ubuntu 上使用 systemd（控制 service 最常用的方式）**停止 CUPS 打印服务**的操作。

### 什么是 CUPS？

CUPS 全称是 **Common UNIX Printing System**。它是 Ubuntu（以及大多数 Linux 发行版和 macOS）上的标准打印系统。
它负责处理：

- 管理本地和网络打印机
- 处理打印任务 (print jobs)
- 打印机发现（特别是通过 `cups-browsed`）
- 用于打印机管理的 Web 界面 (<http://localhost:631>)

该 systemd service 的名称为 **`cups.service`**，它运行主要的 CUPS daemon (`cupsd`)。

### `cups.service/stop` 是什么意思？

它意味着执行命令来**立即停止** CUPS 服务。

实际的命令是：

```bash
sudo systemctl stop cups.service
```

（或者简写为：`sudo systemctl stop cups`）

### 停止它会发生什么？

- CUPS daemon (`cupsd`) 被终止。
- 无法发送或处理新的打印任务。
- 队列中待处理的任务通常会保留（在重启服务后恢复）。
- 打印机发现 / 自动添加网络打印机的功能停止（如果使用了 `cups-browsed`）。
- CUPS Web 界面（631 端口）变得不可用。
- 在服务重新启动之前，从应用程序进行打印将会失败。

### 常用的相关命令

| 目的 | 命令 | 备注 |
| :--- | :--- | :--- |
| 立即停止 CUPS | `sudo systemctl stop cups` | 立即停止 |
| 启动 CUPS | `sudo systemctl start cups` | - |
| 重启 CUPS | `sudo systemctl restart cups` | 故障排除时最常用 |
| 禁止开机自启 | `sudo systemctl disable cups` | 仍可被手动启动 |
| 允许开机自启 | `sudo systemctl enable cups` | - |
| 检查状态 | `sudo systemctl status cups` | 显示运行/停止状态以及最近的 log |
| 停止 + 禁止自启 | `sudo systemctl stop cups`<br>`sudo systemctl disable cups` | 服务器上的常用操作 |

**关于现代 Ubuntu 版本 (22.04+ / 24.04+) 的注意事项：**
有时 CUPS 是作为 **snap** 包提供的（特别是 `cups` 和 `cups-browsed`）。在这种情况下，`systemctl` 可能不起作用，你需要使用：

```bash
sudo snap stop cups
sudo snap disable cups
```

可以通过以下命令检查你使用的是哪个版本：

```bash
systemctl status cups.service
# 或者
snap list | grep cups
```

**References:**

- [Ubuntu Server Documentation - CUPS](https://documentation.ubuntu.com/server/how-to/networking/cups-print-server)
- [Ask Ubuntu - How to stop and disable CUPS](https://askubuntu.com/questions/1463463/how-to-stop-and-disable-cups-service-in-ubuntu-22-04)
- [OpenPrinting CUPS project](https://openprinting.github.io/cups)
