---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Lubuntu：适用于老旧电脑的轻量级Linux系统
translated: true
type: note
---

![Image](https://images.openai.com/static-rsc-4/Bk0ltW5gIfZEQqJvRsz32OG7JhMZNhtVupJ5tSTpClJU3Wia6fmSkSANPyjRdkHm03x0rRtaE0wG-0jAcf6A3y8jhIu0V-ALrBzVbL5x_FWrOWS3RMcShc34PBJyF63iDqmDVP2NuV9ahFJgQm3JugoJwxRr_5I5LDmSiPI14KtsUWTQlk-5VLcwVjitKEFI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/o9EQc-3hYTX6VRNveBvQ_9N_mhI3OukCDn9QZ8rgne_h4osRgWBjlODUzysmUP4eRtPA7JU9Ueahi2qweKi80PfYNjJQ2phsUhyBAt2SDQkD1C502W-A-dnEPTbvXaaDEMT_pWU7LMyDwuTIej4W8njVa_CrFdV4dGRNk6JlnHB38gCc6h-HDPpHV237q4rH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/QzDt6OfJgBVuTfcEYa9HUMDJC6gYoXeVbZ5NOSJF809iEjUO7wdZqR08H2Ah1vWqKOp9b8v-QSyDavthnnrbYzF8sa5vKlm6aRJkXTM8MJlCkdoMO8Sx2ioGqAS2gy8J_EIUjTfSflxgObkZ5nOqXvmoGN0j4dWhiog9nQijVchb-an20X8_8BpFmb9r6Mje?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/898ZbGdvaeArd8Ig9XD5cc5pHHYYWcSZZpvf9CNs9OLrnyivvwenNE96fmGQrx1t1UcU9etG2xLNdcWD_Qgc8wOCXrTJVY4T_fnS8PdE4DV1maWSgqqr5GS6bxa08fCdfZKccSZjR1L45PatUp7W2K85lKWSLvZfeGEoUZYetBWwRfMNC13ir6j63TFix4iQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/f3UX1h8NK5aTjnO_JsbqFoUS4bdca4tCrOIqFJ_wI8Sk1fPpVPUuA2VXt0JRNZ9DbdacM5Jt7gZAa2zJGkkB0uUj7NzLmf6gHJju3uGZrsC1xd0kjxkF6Wg8HifAjnhVCKXwSuve7nxkd0RyDIWYxdYtr3qXsmZYbiZM1MJ7e5e6X2d4x65S-HaD2vsu8HBG?purpose=fullsize)

**Lubuntu** 是一个基于 Ubuntu 的 Linux 发行版，专为**低配置和老旧计算机**设计。

它与普通 Ubuntu 的关键区别在于桌面环境：

* Ubuntu → **GNOME**
* Lubuntu → **LXQt**
* LXQt 在 RAM/CPU 占用上轻量得多。

对于你之前问的那种老硬件——**赛扬 ~2.6 GHz + 4 GB 内存 + 旧联想 L-IG41M3 主板**——Lubuntu 实际上是一个非常合理的选择。

### 粗略对比

| 操作系统          | 启动后典型内存占用 | 适合老硬件 |
| ----------------- | -----------------: | ---------- |
| Ubuntu GNOME      |        ~1.5–2+ GB  | ⚠️         |
| Kubuntu KDE       |       ~0.8–1.2 GB  | 👍         |
| **Lubuntu LXQt**  |     **~0.5–0.8 GB**| **👍👍**   |
| Debian + LXQt     |       ~0.4–0.7 GB  | 👍👍       |

重要的是，**4 GB 内存是可用的**，不过现代浏览器仍然是主要的瓶颈。

### 你能得到什么

Lubuntu 本质上仍是 Ubuntu，因此你可以使用：

```bash
sudo apt update
sudo apt install git python3 build-essential
```

你可以访问庞大的 Ubuntu/Debian 软件包生态系统。

它也使用相对轻量的应用程序和服务：

```text
Linux 内核
    ↓
Ubuntu 基础系统
    ↓
LXQt
    ↓
PCManFM-Qt        文件管理器
QTerminal         终端
Firefox/Chromium  浏览器
    ↓
你的应用程序
```

### 为什么我会在老 PC 上用它

对于像这样的机器：

```text
Intel Celeron ~2.6 GHz
4 GB 内存
旧 Intel 芯片组
SATA HDD/SSD
PCIe x16
```

我可能会安装 **Lubuntu 而不是标准 Ubuntu**。

而且如果你装上 **SSD**，体验会有巨大提升。CPU 虽然老，但 SSD 能消除很多“老古董电脑”的感觉。

有一点需要注意：**Lubuntu 的当前版本有各自的硬件/CPU 支持要求**，因此在非常老的赛扬上安装前，请确认该 CPU 是否支持所需的 64 位指令集。如果你能提供**具体的赛扬型号**（例如 `Celeron E3400`、`D 347` 等），我可以确切告诉你应该安装哪个 Lubuntu 版本。
