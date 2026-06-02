---
audio: false
generated: true
lang: zh
layout: post
title: 使用VS Code
translated: true
type: note
---

### 核心要点

- VS Code 是一款适用于 Windows、macOS 和 Linux 的流行免费代码编辑器，支持多种编程语言。
- 根据开发者使用情况，其最有用的功能可能包括语法高亮、调试和 Git 集成。
- 证据表明其内置的 30 多项功能可提升生产力，例如多光标编辑和远程开发。

---

### VS Code 入门指南

Visual Studio Code（VS Code）是微软开发的一款轻量级开源代码编辑器，非常适合在 Windows、macOS 和 Linux 系统上进行编码。首先，请从[官网](https://code.visualstudio.com/download)下载。安装完成后，启动 VS Code 即可开始编码。

#### 基本用法

- **创建或打开文件**：使用 `文件 > 新建文件`（Windows/Linux 上为 `Ctrl + N`，macOS 上为 `Cmd + N`）来创建新文件，使用 `文件 > 打开`（Windows/Linux 上为 `Ctrl + O`，macOS 上为 `Cmd + O`）来打开现有文件。使用 `Ctrl + S` 或 `Cmd + S` 保存文件。
- **编辑代码**：享受语法高亮、自动缩进和括号匹配等功能，以提高代码可读性。使用代码片段快速插入代码，使用多光标编辑（`Alt + 单击`）进行同步编辑。
- **导航**：使用 `Ctrl + 单击`跳转到定义，通过右键单击查找引用，并使用 `Ctrl + P` 快速访问文件。顶部的面包屑导航有助于浏览文件路径。
- **调试和版本控制**：在行号旁单击设置断点，使用 `F5` 开始调试，并通过源代码管理面板管理 Git 操作（如提交和推送）。
- **自定义**：通过 `文件 > 首选项 > 颜色主题` 更改主题，并在 `文件 > 首选项 > 键盘快捷方式` 下调整快捷键。

#### 30 个最实用的功能

VS Code 提供了丰富的内置功能，可提升开发者的生产力。以下是 30 个最实用的功能，按类别清晰列出：

| **类别**           | **功能**                           | **描述**                                                                 |
|--------------------|------------------------------------|--------------------------------------------------------------------------|
| **编辑**           | 语法高亮                           | 根据语言为代码着色，提高可读性。                                         |
|                    | 自动缩进                           | 自动缩进代码以保持正确的结构。                                           |
|                    | 括号匹配                           | 高亮匹配的括号以帮助检测错误。                                           |
|                    | 代码片段                           | 快速插入常用的代码模式。                                                 |
|                    | 多光标编辑                         | 通过 `Alt + 单击` 同时编辑多个代码部分。                                 |
|                    | 代码折叠                           | 折叠/展开代码区域以获得更好的概览。                                      |
|                    | Code Lens                          | 显示附加信息，如提交历史记录或测试状态。                                 |
|                    | 速览定义                           | 在悬停窗口中查看函数/变量定义而无需导航。                                |
| **导航**           | 转到定义                           | 通过 `Ctrl + 单击` 跳转到函数/变量定义。                                 |
|                    | 查找所有引用                       | 定位代码库中函数/变量的所有出现位置。                                    |
|                    | 快速打开                           | 使用 `Ctrl + P` 快速打开文件。                                           |
|                    | 面包屑导航                         | 显示文件路径，便于导航到不同部分。                                       |
| **调试**           | 内置调试器                         | 设置断点、单步执行代码并检查变量。                                       |
|                    | 断点                               | 在特定行暂停执行以进行调试。                                             |
|                    | 单步执行代码                       | 在调试过程中逐行执行代码（`F10`、`F11`）。                               |
|                    | 监视变量                           | 在调试会话期间监视变量值。                                               |
| **版本控制**       | Git 集成                           | 开箱即用地支持 Git 操作，如提交、拉取、推送。                            |
|                    | 提交、拉取、推送                   | 直接在 VS Code 中执行 Git 操作。                                         |
|                    | 追溯视图                           | 显示每行代码的最后修改者。                                               |
| **自定义**         | 颜色主题                           | 使用各种配色方案自定义编辑器外观。                                       |
|                    | 键盘快捷方式                       | 自定义或使用默认快捷方式以提高效率。                                     |
|                    | 设置同步                           | 跨多台机器同步设置以确保一致性。                                         |
|                    | 配置文件                           | 为项目保存和切换不同的设置集。                                           |
| **远程开发**       | Remote SSH                         | 通过 SSH 在远程服务器上进行开发，实现灵活访问。                          |
|                    | 容器                               | 在隔离的容器环境中进行开发。                                             |
|                    | Codespaces                         | 使用 GitHub 提供的基于云的开发环境。                                     |
| **生产力**         | 命令面板                           | 通过 `Ctrl + Shift + P` 访问所有命令。                                   |
|                    | 任务运行器                         | 在内部运行构建或测试代码等任务。                                         |
|                    | 集成终端                           | 直接在 VS Code 中访问命令行。                                            |
|                    | 问题面板                           | 显示错误、警告和问题以便快速解决。                                       |

如需详细探索，请访问[官方文档](https://code.visualstudio.com/docs)。

---

### VS Code 及其功能使用全面指南

本节深入探讨如何使用 Visual Studio Code（VS Code）——微软开发的一款多功能代码编辑器，并详细介绍其 30 个最实用的内置功能。这些信息基于截至 2025 年 2 月 27 日对开发者偏好和官方文档的广泛研究。VS Code 适用于 Windows、macOS 和 Linux，支持多种编程语言，并以其可扩展性和性能而闻名。根据 2024 年 Stack Overflow 开发者调查，超过 73.6% 的开发者使用它。

#### 安装与初始设置

首先，从[官网](https://code.visualstudio.com/download)下载 VS Code。安装过程简单，支持多平台，确保所有用户均可访问。启动后，用户会看到一个欢迎页面，提供诸如打开文件夹或创建新文件等操作。对于工作区信任，尤其是在处理下载的代码时，请查看其安全性，如[文档](https://code.visualstudio.com/docs/getstarted/getting-started)中所述。

#### 分步使用指南

1. **创建和打开文件**：使用 `文件 > 新建文件` 或 `Ctrl + N`（macOS 上为 `Cmd + N`）创建新文件，使用 `文件 > 打开` 或 `Ctrl + O`（macOS 上为 `Cmd + O`）打开现有文件。使用 `Ctrl + S` 或 `Cmd + S` 保存。这是启动任何项目的基础，如[介绍视频](https://code.visualstudio.com/docs/introvideos/basics)中所述。
2. **基本编辑功能**：VS Code 开箱即用地提供语法高亮、自动缩进和括号匹配功能，增强了可读性并减少了错误。例如，输入 "console.log" 并按 Tab 键会插入一个 JavaScript 代码片段，此功能在[编辑教程](https://code.visualstudio.com/docs/introvideos/codeediting)中有所强调。
3. **高级编辑**：通过 `Alt + 单击` 激活的多光标编辑允许跨多行同时编辑，是处理重复性任务的生产力助推器。代码片段和折叠进一步简化了工作流程，如[技巧和窍门](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)中所述。
4. **导航与搜索**：使用 `Ctrl + 单击` 进行"转到定义"，右键单击进行"查找所有引用"，使用 `Ctrl + P` 进行"快速打开"。顶部的面包屑导航有助于在复杂的文件结构中导航，详见[用户界面文档](https://code.visualstudio.com/docs/getstarted/userinterface)。
5. **调试能力**：在行号旁单击设置断点，使用 `F5` 开始调试，并使用 `F10`（逐过程）、`F11`（逐语句）和 `Shift + F11`（跳出）进行详细检查。监视变量以监控值，此功能在[此处](https://code.visualstudio.com/docs/editor/debugging)有详细介绍。
6. **使用 Git 进行版本控制**：通过源代码管理视图初始化仓库，使用 `Ctrl + Enter`（macOS：`Cmd + Enter`）提交，并管理拉取/推送操作。追溯视图显示修改历史，增强了协作，如[概述](https://code.visualstudio.com/docs/sourcecontrol/overview)中所述。
7. **自定义选项**：通过 `文件 > 首选项 > 颜色主题` 更改颜色主题，在 `文件 > 首选项 > 键盘快捷方式` 下自定义键盘快捷方式，并使用设置同步跨设备同步设置。配置文件允许保存不同的配置，详见[此处](https://code.visualstudio.com/docs/getstarted/settings)。
8. **远程和云开发**：使用 Remote SSH 进行基于服务器的开发，使用容器进行隔离环境开发，使用 Codespaces 进行基于云的设置，从而扩展开发灵活性，如[此处](https://code.visualstudio.com/docs/remote/remote-overview)所述。

#### 详细功能分析

下表列出了 30 个最实用的内置功能，按类别清晰列出，基于官方文档和开发者使用模式的研究：

| **类别**           | **功能**                           | **描述**                                                                 |
|--------------------|------------------------------------|--------------------------------------------------------------------------|
| **编辑**           | 语法高亮                           | 根据语言为代码着色以提高可读性，支持数百种语言。                         |
|                    | 自动缩进                           | 自动缩进代码以保持正确的结构，增强一致性。                               |
|                    | 括号匹配                           | 高亮匹配的括号以帮助检测错误和提高可读性。                               |
|                    | 代码片段                           | 快速插入常用的代码模式，例如 JavaScript 的 "console.log"。              |
|                    | 多光标编辑                         | 通过 `Alt + 单击` 同时编辑多个代码部分，提高生产力。                     |
|                    | 代码折叠                           | 折叠/展开代码区域以获得更好的概览，改善专注度。                          |
|                    | Code Lens                          | 显示附加信息，如提交历史记录或测试状态，有助于维护。                     |
|                    | 速览定义                           | 在悬停窗口中查看函数/变量定义而无需导航，节省时间。                      |
| **导航**           | 转到定义                           | 通过 `Ctrl + 单击` 跳转到函数/变量定义，增强导航。                       |
|                    | 查找所有引用                       | 定位函数/变量的所有出现位置，对重构很有用。                              |
|                    | 快速打开                           | 使用 `Ctrl + P` 快速打开文件，加快文件访问速度。                         |
|                    | 面包屑导航                         | 显示文件路径，便于导航到不同部分，改善定位。                             |
| **调试**           | 内置调试器                         | 设置断点、单步执行代码并检查变量，对测试至关重要。                       |
|                    | 断点                               | 在特定行暂停执行以进行详细调试，对查找错误至关重要。                     |
|                    | 单步执行代码                       | 逐行执行代码（`F10`、`F11`），允许深入检查。                             |
|                    | 监视变量                           | 在调试期间监视变量值，有助于状态跟踪。                                   |
| **版本控制**       | Git 集成                           | 支持 Git 操作，如提交、拉取、推送，增强协作。                            |
|                    | 提交、拉取、推送                   | 直接在 VS Code 中执行 Git 操作，简化版本控制。                           |
|                    | 追溯视图                           | 显示每行代码的最后修改者，对代码审查和问责制很有用。                     |
| **自定义**         | 颜色主题                           | 自定义编辑器外观，提高视觉舒适度，提供多种选项。                         |
|                    | 键盘快捷方式                       | 自定义或使用默认快捷方式，提高效率，完全可配置。                         |
|                    | 设置同步                           | 跨机器同步设置以确保一致性，详见[此处](https://code.visualstudio.com/docs/getstarted/settings#_settings-sync)。 |
|                    | 配置文件                           | 为不同项目保存和切换设置，增强灵活性。                                   |
| **远程开发**       | Remote SSH                         | 通过 SSH 在远程服务器上进行开发，扩展访问范围，详见[此处](https://code.visualstudio.com/docs/remote/ssh)。 |
|                    | 容器                               | 在隔离的容器环境中进行开发，确保一致性，如[此处](https://code.visualstudio.com/docs/remote/containers)所述。 |
|                    | Codespaces                         | 使用 GitHub 提供的基于云的开发环境，增强协作，详见[此处](https://code.visualstudio.com/docs/remote/codespaces)。 |
| **生产力**         | 命令面板                           | 通过 `Ctrl + Shift + P` 访问所有命令，集中功能。                         |
|                    | 任务运行器                         | 在内部运行构建或测试代码等任务，改进工作流程，详见[此处](https://code.visualstudio.com/docs/editor/tasks)。 |
|                    | 集成终端                           | 在 VS Code 内访问命令行，增强集成性，如[此处](https://code.visualstudio.com/docs/integrated-terminal)所述。 |
|                    | 问题面板                           | 显示错误、警告和问题，有助于快速解决，对调试至关重要。                   |

这些功能是根据广泛研究（包括官方文档和面向开发者的文章）汇编而成，确保它们与 2025 年的当前使用情况保持一致。例如，Git 和远程开发功能的集成反映了 VS Code 为满足现代开发需求而进行的演变，如[更新日志](https://code.visualstudio.com/updates/v1_97)所示。

#### 其他注意事项

VS Code 的可扩展性（拥有超过 30,000 个扩展）是对这些内置功能的补充，但此处重点在于原生功能。例如，虽然 GitHub Copilot 很受欢迎，但它是一个扩展而非内置功能，因此被排除在外。快速的启动时间和高效的内存使用（如[性能讨论](https://code.visualstudio.com/docs/editor/whyvscode)中所述）使其适合日常使用，这对于期望使用更重型 IDE 的用户来说是一个意想不到的细节。

如需进一步学习，请探索[介绍视频](https://code.visualstudio.com/docs/introvideos/basics)和[技巧与窍门](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)，以确保全面了解 VS Code 的功能。

---

### 主要引用文献

- [VS Code 官方文档](https://code.visualstudio.com/docs/)
- [VS Code 功能技巧与窍门](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
- [VS Code 调试指南](https://code.visualstudio.com/docs/editor/debugging)
- [VS Code Git 集成概述](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [VS Code 设置同步文档](https://code.visualstudio.com/docs/getstarted/settings#_settings-sync)
- [VS Code Remote SSH 开发](https://code.visualstudio.com/docs/remote/ssh)
- [VS Code 容器开发](https://code.visualstudio.com/docs/remote/containers)
- [VS Code Codespaces 开发](https://code.visualstudio.com/docs/remote/codespaces)
- [VS Code 任务运行器文档](https://code.visualstudio.com/docs/editor/tasks)
- [VS Code 集成终端指南](https://code.visualstudio.com/docs/integrated-terminal)
- [我们为何构建 VS Code 编辑器](https://code.visualstudio.com/docs/editor/whyvscode)
- [VS Code 介绍视频](https://code.visualstudio.com/docs/introvideos/basics)
- [VS Code 2025 年 1 月更新](https://code.visualstudio.com/updates/v1_97)
