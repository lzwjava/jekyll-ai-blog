---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Mac 上运行 Linux：极少数人的小众用途
translated: true
type: note
---

**Question:** 很多人使用 Mac Pro 或 MacBook Air 来运行 Linux 吗？

**Answer:**

不，**并没有很多人**在 MacBook Air 或 Mac Pro 机型上将 Linux 作为主要或原生 OS 运行——这属于一种分众（niche）行为，而非普遍现象。

以下是截至 2026 年初现状的详细分析：

### 总体数量与普及程度

- Desktop Linux（传统 Linux 发行版，不包括 Android 或 ChromeOS）在全球桌面/笔记本电脑市场的份额约为 **4–6%**。macOS 的市场份额约为 **15–16%**。
- 在 Mac 硬件上运行 Linux 的子群体规模更小，仅占 Mac 用户的一小部分。
- 大多数 Mac 用户留在 macOS 是因为其紧密的硬件与软件集成、ecosystem（iPhone/iPad 的 continuity、Final Cut、Logic 等）以及出色的 battery life 和 power management。

### 基于 Intel 的 Mac（旧款 MacBook Air/Pro，旧款 Mac Pro）

- 曾几何时，在爱好者、developers 以及想要复活旧硬件（例如 2012–2019 年款 MacBook Pro/Air）的人群中，原生运行 Linux（双系统或完全替换）相当流行。
- 这种情况现在依然存在，但并非主流。常见问题包括 battery life 不理想、缺少 drivers（webcam、部分功能键、sleep 模式）以及需要大量的 tinkering。
- 许多希望在 Intel Mac 上使用 Linux 的人现在更倾向于在 **virtual machine**（Parallels, UTM, VirtualBox）中运行，而不是原生安装——这种方式更为普遍，因为可以保留 macOS 作为 host。

### Apple Silicon Macs (M1/M2/M3/M4 MacBook Air/Pro, Mac Pro M2 Ultra)

- 这是目前大多数新款 MacBook Air 和 Mac Pro 机型所在的平台（2021年及以后）。
- **Asahi Linux**（以及 Fedora Asahi Remix）是原生或双系统运行 Linux 的主要途径。
- 进展令人瞩目：M1/M2 的支持已经相当完善（GPU acceleration、良好的性能，对许多人来说已可作为 daily-driver）。
- M3/M4/M5 的支持仍在开发中——截至 2026 年初，基础启动已经实现，但 GPU acceleration 和某些功能（如更好的 external display 支持、power management）仍不完整或处于实验阶段。
- Asahi 自身的安装统计显示，已追踪到约 **82,000 次安装**（主要集中在 M1/M2 MacBook Air/Pro 机型；Mac Pro 上非常少）。
- 即使考虑到许多未被追踪的安装，相对于全球数亿台活跃的 Mac 来说，这个数字依然非常小。
- 使用者仍主要集中在 enthusiast 和 developer 群体。大多数 Apple Silicon 用户坚持使用 macOS；部分人在 VM 中运行 Linux（UTM 在 ARM 平台上非常流行且运行快速）。

### 究竟是谁在这么做？

- 需要原生 Linux 环境的 Developers（用于 containers、kernel 开发或特定 tooling）。
- 对 macOS 的变化感到不满，或追求更高程度 customization 和 privacy 的人。
- 复活“过时” Intel Mac 或实验 ARM Linux 的硬件玩家（Hobbyists）。
- 极少有“普通”用户会这样做——这在办公室、学校或一般消费场景中并不常见。

### 总结

在 Mac 硬件上运行 Linux 是存在的，并且在许多情况下表现良好（尤其是 M1/M2 搭配 Asahi），但 **“并没有很多人”这样做**。它只是已经很小的 Desktop Linux 用户群中的一个极小众分支。大多数需要 Linux 的 Mac 拥有者通常会直接使用 VM，或者购买专门的 Linux 硬件。

**References:**

- [https://stats.asahilinux.org/](https://stats.asahilinux.org/)
- [https://en.wikipedia.org/wiki/Usage_share_of_operating_systems](https://en.wikipedia.org/wiki/Usage_share_of_operating_systems)
- [https://asahilinux.org/](https://asahilinux.org/)
- [https://www.phoronix.com/news/Apple-M3-Linux-Boot-To-KDE](https://www.phoronix.com/news/Apple-M3-Linux-Boot-To-KDE)
