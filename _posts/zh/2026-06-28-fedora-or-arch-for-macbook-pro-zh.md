---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fedora还是Arch：MacBook Pro的选择
translated: true
type: note
---

问题：根据我的情况，2017款MacBook Pro的最佳Linux发行版是什么？

答案：

简短版：**Fedora**或**Arch**，而不是Mint。对于首次安装Linux的普通用户来说，Mint是正确的选择。但你并非这类用户——你训练模型、常驻终端，并且需要前沿工具。Mint的整个价值主张（稳定性、保守的软件包、手把手引导）对你而言反而是阻碍。

然而，2017款MacBook Pro存在一些硬件特性，这些特性比发行版的选择更为重要。让我先搜索一下该硬件支持的现状，然后再给出推荐。实际情况是这样的。2017款13"/15" MacBook Pro（A1707/A1706，MacBookPro14,x）配备的是**T1芯片（iBridge）**——而非更棘手的T2芯片。这一点非常重要。根据维护的跟踪仓库，已知痛点包括：基本键盘可用，但带Esc键和功能键的Touch Bar需要自定义驱动；Wi-Fi部分可用；休眠后无法唤醒大部分硬件；Touch ID不支持。声音也需要树外驱动`snd_hda_macbookpro`——Linux 6.18中上游的cs8409驱动对某些用户仍然不能完全正常工作。

一个关键的陷阱会覆盖发行版的选择：T1芯片提供摄像头、环境光传感器、Touch Bar和Touch ID，所有这些都依赖于macOS存储在EFI系统分区上的固件。保留这些固件可用性的最简单方法是将Linux与macOS一起安装，并保留原有的ESP。因此，**不要擦除磁盘——双系统启动，保留macOS的ESP。** 如果你删除了它，就会丢失摄像头和Touch Bar的固件，恢复过程也会变得很麻烦。

这里决定发行版的两个因素是**内核的新鲜度**和**DKMS的易用性**，因为你需要构建树外驱动（`applespi`、`apple_ib_tb`、声音驱动）。这是推荐的核心考量。

我实际的选择，按优先级排序：

**1. Fedora (Workstation) —— 我的首选推荐。** 搭载较新的主线内核（2026年版本为6.17+），出色的DKMS支持，SELinux/安全默认设置值得你学习，而且很多内核/ML领域的人都在使用它。更新的内核意味着更多硬件可以开箱即用，减少驱动折腾。对于你的CUDA相关/Python ML堆栈，你无需与保守的软件包版本作斗争。

**2. Arch（如果你想更快安装，可以选择EndeavourOS）。** 前沿内核，AUR中已打包`macbook12-spi-driver`和`snd-hda-macbook`，而且Arch Wiki拥有最好的Mac专属文档。这**最符合你的Yin-Wang/第一性原理理念**——你亲手构建系统，理解每一层。代价是时间，在这台笔记本上，你会在Touch Bar和休眠上花费大量时间。如果你将安装过程视为一次学习练习，那么这是值得的；如果你只想要一台能用的机器，那就不值得。

**3. Mint —— 跳过它。** 它基于Ubuntu 24.04基础版，内核为6.8/6.11，这比你处理边缘硬件所需要的**更旧**。有用户在Ubuntu 24.04上让Touch Bar工作，但仅限于6.8.0内核，而非6.11.x内核——这种回归问题正是LTS保守型发行版在特殊硬件上带来的麻烦。对于Mint的手把手引导，你过于大材小用，而其旧内核又无法满足你的需求。

2017款MBP作为一台备用Linux机器还不错，但要清醒认识：这是一个适合喜欢折腾的人的安装过程，而非一个纯粹的体验。如果你主要想要一个无摩擦的Linux体验，那就交给RTX 4070工作站（`lzw@192.168.1.36`）——在上面裸机运行Fedora或Ubuntu，把MBP当作便携终端。如果你*想*深入内核驱动的兔子洞，那么MBP的安装是值得的；如果你只想要一台能用的笔记本，它只会让你沮丧。

如果你选择Fedora的实际操作路径：

- 双系统启动，保留macOS和ESP（上述固件依赖）。
- 安装后，需要构建：`macbook12-spi-driver`（键盘/触控板/Touch Bar）和`snd_hda_macbookpro`（声音），两者都通过DKMS以便在内核更新后继续使用。
- Wi-Fi（Broadcom BCM43xx）需要`broadcom-wl` / `wl` DKMS——根据报告，5GHz频段不稳定，所以安装时请准备一个USB-C以太网转接器。

需要我调整Fedora Workstation ISO的刷写脚本（验证后`dd`，流程与之前相同），或者编写一个安装后的DKMS驱动设置脚本吗？
