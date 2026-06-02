---
audio: false
generated: true
lang: zh
layout: post
title: Ubuntu 24.04 中的按键重映射
translated: true
type: note
---

### 关键要点

- 在 Ubuntu 24.04 中，您似乎可以通过图形工具 GNOME Tweaks 或使用 `gsettings` 命令行来交换左 Ctrl 和 Caps Lock 键。
- 研究表明这两种方法在会话间都是持久的，适合日常稳定使用。
- 现有证据表明 GNOME Tweaks 更用户友好，而命令行方法则为高级用户提供更多控制权。

#### 使用 GNOME Tweaks

GNOME Tweaks 提供了简单的键位交换界面：

- 如需安装，请运行 `sudo apt install gnome-tweak-tool`
- 打开 Tweaks，进入“键盘和鼠标”，点击“额外布局选项”，在“Ctrl 键位置”下选择“交换 Ctrl 和 Caps Lock”

#### 使用命令行

技术用户可使用终端操作：

- 运行 `gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"` 即可持久交换键位

#### 意外发现

与支持精细键位重映射的 Windows PowerToys 不同，Ubuntu 的方法主要交换左 Ctrl 与 Caps Lock，这可能会影响您依赖的其他键盘快捷键。

---

### 调研笔记：Ubuntu 24.04 键位交换功能深度解析

本节将深入探讨在 Ubuntu 24.04 中交换左 Ctrl 和 Caps Lock 键的完整方案，类似于 Windows 系统中 PowerToys 提供的功能。本分析综合多方资料确保准确性与深度，同时满足新手用户和高级用户的需求。

#### 背景与语境

Ubuntu 24.04（代号“Noble Numbat”）作为长期支持版本，继续使用 GNOME 桌面环境（具体为版本 46）。习惯 Windows 系统的用户可能期望类似的定制功能，比如通过 PowerToys 实现左 Ctrl 与 Caps Lock 键交换。在 Linux 系统中，键盘定制通常通过 GNOME Tweaks 等工具或命令行实用程序实现，相比 Windows 需要采用不同的操作方式。

用户交换左 Ctrl 与 Caps Lock 键的需求在开发者和高级用户中十分常见，特别是习惯使用 Emacs 或 Vim 工作流的用户，这些场景中 Ctrl 键使用频率很高。本分析将同时探讨图形界面和命令行方案，确保配置在会话间保持持久性，并与 Ubuntu 24.04 系统完全兼容。

#### 键位交换方法详解

##### 方法一：使用 GNOME Tweaks

GNOME Tweaks 作为图形化工具，可简化包括键盘设置在内的桌面定制流程。根据现有文档，该工具支持通过界面进行键位交换：

1. **安装步骤**：若未预装，用户可通过 Ubuntu 软件中心或运行以下命令安装：

   ```bash
   sudo apt install gnome-tweak-tool
   ```

   该工具包含在 Ubuntu 24.04 的标准软件源中

2. **访问键盘设置**：从应用程序菜单或通过活动概览搜索“Tweaks”启动程序，在左侧菜单中进入“键盘和鼠标”分区

3. **额外布局选项**：点击“额外布局选项”进入高级键盘设置，在该菜单中找到“Ctrl 键位置”区域，选择标有“交换 Ctrl 和 Caps Lock”的选项

4. **持久化机制**：通过 GNOME Tweaks 所做的修改会存储于 `dconf` 数据库，该用户专属配置在登录时自动加载，因此重启后依然有效

该方法特别适合不熟悉命令行工具的用户，符合 Windows 用户的图形界面操作习惯。但需注意，“交换 Ctrl 和 Caps Lock”选项在 Ubuntu 24.04 的 GNOME Tweaks 中是否可用，主要基于历史文档的推测，包括 [Ask Ubuntu: 如何重新映射 Caps Lock 和 Ctrl 键？](https://askubuntu.com/questions/33774/how-do-i-remap-the-caps-lock-and-ctrl-keys) 和 [Opensource.com: 如何在 Linux 中交换 Ctrl 和 Caps Lock 键](https://opensource.com/article/18/11/how-swap-ctrl-and-caps-lock-your-keyboard) 等资料均显示该功能具有延续性

##### 方法二：使用 `gsettings` 命令行

对于偏好命令行操作或遇到 GNOME Tweaks 问题的用户，`gsettings` 命令提供了直接修改键盘选项的途径：

1. **启动终端**：通过 Ctrl + Alt + T 快捷键或活动概览访问终端

2. **设置键盘选项**：运行以下命令实现键位交换：

   ```bash
   gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:swapcaps']"
   ```

   该命令通过修改 `org.gnome.desktop.input-sources` 下的 `xkb-options` 键，添加标准的 XKB 选项“ctrl:swapcaps”

3. **验证与持久性**：执行命令后可通过按压左 Ctrl 和 Caps Lock 键测试行为变更。由于设置存储于用户专属的 `dconf` 数据库，配置将在登录时自动应用并保持持久性

此方法特别适合高级用户或自动化部署场景（如多用户配置脚本），[EmacsWiki: 移动 Ctrl 键](https://www.emacswiki.org/emacs/MovingTheCtrlKey) 等资料详细记载了 XKB 选项及其效果，为该方案提供支持

#### 方法对比分析

为帮助用户选择合适方案，以下从易用性、技术要求和持久性维度对比两种方法：

| **对比维度**         | **GNOME Tweaks**                     | **gsettings 命令行**           |
|----------------------|--------------------------------------|--------------------------------------|
| **易用性**           | 高（图形界面）                       | 中（需掌握终端操作）                 |
| **技术要求**         | 低（适合初学者）                     | 中（适合高级用户）                   |
| **持久性**           | 自动（存储于 dconf）                 | 自动（存储于 dconf）                 |
| **需要安装**         | 可能需要安装                         | 无需额外安装                         |
| **灵活性**           | 限于图形界面选项                     | 高（可组合多个选项）                 |

对比表明：GNOME Tweaks 适合追求操作简便的用户，而 `gsettings` 则为熟悉命令行的用户提供更多灵活性

#### 注意事项与潜在问题

- **左 Ctrl 专属性**：两种方法预期都只交换左 Ctrl 键，因为“ctrl:swapcaps”在标准 XKB 配置中通常仅影响左 Ctrl 键。但实际效果可能因键盘布局而异，建议用户验证具体行为
- **快捷键影响**：键位交换可能影响现有快捷键（如 Ctrl+C 复制、Ctrl+V 粘贴），配置后应重点测试终端、IDE 等关键应用的快捷键兼容性
- **潜在问题**：虽然未发现“交换 Ctrl 和 Caps Lock”选项在 Ubuntu 24.04 中失效的具体报告，但用户应注意可能的系统缺陷，如 [Ubuntu 24.04 键盘问题：登录后 Caps Lock 状态反转](https://ubuntuforums.org/showthread.php?t=2497465) 提及的类似问题。若遇异常，命令行方法可作为备用方案

#### 意外发现：与 Windows PowerToys 的差异

与支持精细键位重映射（可单独重映射左 Ctrl 而不影响其他键）的 Windows PowerToys 不同，Ubuntu 的方案更为标准化。GNOME Tweaks 中的“交换 Ctrl 和 Caps Lock”选项或 `gsettings` 的“ctrl:swapcaps”主要交换左 Ctrl 与 Caps Lock，可能影响其他键盘行为。这一差异可能使期待完全对等功能的用户感到意外，凸显了配置后测试的重要性

#### 总结

GNOME Tweaks 和 `gsettings` 均为在 Ubuntu 24.04 中交换左 Ctrl 与 Caps Lock 键的可行方案，能确保持久性并适应用户工作流。GNOME Tweaks 提供图形化入门方案，`gsettings` 则满足高级用户的命令行控制需求。用户应在配置后验证实际效果，并考虑对键盘快捷键的潜在影响，特别是注意其与 Windows PowerToys 的功能差异

### 关键引用

- [如何重新映射 Caps Lock 和 Ctrl 键 Ask Ubuntu](https://askubuntu.com/questions/33774/how-do-i-remap-the-caps-lock-and-ctrl-keys)
- [如何在 Linux 中交换 Ctrl 和 Caps Lock 键 Opensource.com](https://opensource.com/article/18/11/how-swap-ctrl-and-caps-lock-your-keyboard)
- [移动 Ctrl 键 EmacsWiki](https://www.emacswiki.org/emacs/MovingTheCtrlKey)
- [Ubuntu 24.04 键盘问题：登录后 Caps Lock 状态反转 Ubuntu Forums](https://ubuntuforums.org/showthread.php?t=2497465)
