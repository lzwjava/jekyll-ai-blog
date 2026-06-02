---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Yazi 终端文件管理器指南
translated: true
type: note
---

我会搜索关于 Yazi 的全面信息，为您提供这个文件管理工具的详细介绍。让我搜索更多关于 Yazi 的插件和用例的信息。---

## 问题：

什么是 Yazi 这个文件管理工具的全面介绍？

## 答案：

### 概述

Yazi 是一个用 Rust 编写的终端文件管理器，基于非阻塞异步 I/O，旨在提供高效、用户友好且可自定义的文件管理体验。“Yazi”在中文中意为“鸭子”。该工具目前处于公开测试版，可以作为日常驱动使用，尽管它仍在快速发展中，并预计会有破坏性变更。

### 核心性能特性

**异步架构：**
Yazi 具有完整的异步支持，所有 I/O 操作均为异步，CPU 任务分布在多个线程中，充分利用可用资源。该工具内部使用 Tokio 作为异步运行时，以非阻塞（事件驱动）方式处理任务，确保高效性和快速响应时间。

**任务管理：**
该工具提供强大的异步任务调度和管理功能，包括实时进度更新、任务取消以及内部任务优先级分配。

**预览能力：**
结合预缓存机制，大大加速图像和普通文件的加载。Yazi 支持预览文本文件、PDF 文件、图像、视频，并内置语法高亮。

### 主要特性

**图像和媒体支持：**
Yazi 内置支持多种图像协议，还集成了 Überzug++ 和 Chafa，几乎覆盖所有终端。

**插件系统：**
该工具具有并发插件系统，包括 UI 插件（重写大部分 UI）、功能插件、自定义 previewer/preloader/spotter/fetcher 功能，只需 Lua 脚本即可。用户可以通过 Lua 插件扩展 Yazi 的功能，这些插件需放置在 Yazi 配置目录的 plugins 子目录中。

**用户界面和功能：**
额外特性包括批量重命名、归档提取、视觉模式、文件选择器、git 集成和挂载管理器。该工具支持多标签页、跨目录选择、可滚动预览（针对视频、PDF、归档、代码、目录）、主题系统、鼠标支持、废纸篓以及自定义布局。

### 自定义和配置

**配置系统：**
Yazi 使用基于 TOML 的配置文件，选项可覆盖默认设置。在类 Unix 系统上，配置目录位于 `~/.config/yazi/`，在 Windows 上位于 `%AppData%\yazi\config\`。

**按键绑定：**
该工具采用类似于 Vim 的更现代 UI 接口设计，支持批量操作和鼠标滚动，并与 fd、rg、fzf 等常用工具集成。

**主题：**
Yazi 的主题系统通过灵活的三层配置结构（预设主题（dark/light）、flavor 覆盖和用户自定义）为所有界面组件、文件类型和图标提供全面视觉自定义。

### 可用插件和扩展

Yazi 生态系统包含丰富的插件，用于各种目的：

- **文件操作：** Smart-enter（一键打开文件或进入目录）、full-border（添加边框以获得更华丽外观）、toggle-pane（切换不同面板）、chmod（更改文件权限）、smart-paste（智能粘贴文件）
- **导航：** Jump-to-char（类似 vim 的字符跳转）、smart-filter（连续过滤）、bookmarks
- **版本控制：** Git 集成（显示文件变更状态）、lazygit 集成
- **媒体预览：** mediainfo（预览多种媒体类型）、audio-preview（谱图可视化）
- **数据查看：** duckdb（带分析预览 CSV/TSV/JSON/Parquet 文件）
- **系统集成：** mount-manager、sshfs（远程目录挂载）、sudo 操作、trash 管理

### 安装和集成

在 macOS 上使用 Homebrew 安装简单，在 Linux 上使用包管理器也方便，而 Windows 的过程较长。shell 包装函数允许用户在退出 Yazi 时自动进入之前所在的目录。

### 与其他工具的比较

Yazi 与其他终端文件管理器相比表现出色。虽然 Ranger 是经久不衰的经典之选，其首个稳定版于 2009 年发布，但被指出速度有些慢，且基本操作如创建文件需要 vim 命令。Yazi 提供更快的性能、更直观的基于热键的操作，并与现代命令行工具集成。

### 用例

Yazi 特别适合开发者和终端爱好者，他们希望通过现代、可自定义的文件管理器提升生产力，避免 GUI 文件浏览器的开销，同时在终端环境中提供强大的预览和插件功能。

---

## 参考资料：

- [https://github.com/sxyazi/yazi](https://github.com/sxyazi/yazi)
- [https://yazi-rs.github.io/](https://yazi-rs.github.io/)
- [https://yazi-rs.github.io/docs/quick-start/](https://yazi-rs.github.io/docs/quick-start/)
- [https://terminaltrove.com/yazi/](https://terminaltrove.com/yazi/)
- [https://medium.com/@pthapa1/yazi-the-best-terminal-file-manager-to-boost-your-productivity-bf13f244756a](https://medium.com/@pthapa1/yazi-the-best-terminal-file-manager-to-boost-your-productivity-bf13f244756a)
- [https://www.x-cmd.com/pkg/yazi/](https://www.x-cmd.com/pkg/yazi/)
- [https://snapcraft.io/yazi](https://snapcraft.io/yazi)
- [https://www.markpitblado.me/blog/setting-up-the-yazi-file-manager](https://www.markpitblado.me/blog/setting-up-the-yazi-file-manager)
- [https://www.josean.com/posts/how-to-use-yazi-file-manager](https://www.josean.com/posts/how-to-use-yazi-file-manager)
- [https://wiki.nixos.org/wiki/Yazi](https://wiki.nixos.org/wiki/Yazi)
- [https://yazi-rs.github.io/docs/configuration/overview/](https://yazi-rs.github.io/docs/configuration/overview/)
- [https://github.com/yazi-rs/plugins](https://github.com/yazi-rs/plugins)
- [https://yazi-rs.github.io/docs/plugins/overview/](https://yazi-rs.github.io/docs/plugins/overview/)
- [https://yazi-rs.github.io/docs/resources/](https://yazi-rs.github.io/docs/resources/)
- [https://yazi-rs.github.io/docs/installation/](https://yazi-rs.github.io/docs/installation/)
- [https://github.com/AnirudhG07/awesome-yazi](https://github.com/AnirudhG07/awesome-yazi)
