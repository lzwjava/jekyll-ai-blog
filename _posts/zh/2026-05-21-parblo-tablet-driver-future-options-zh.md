---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Parblo数位板驱动未来选项
translated: true
type: note
---

以下是您面临的情况及解决方案：

---

**问题详情**

| 详情 | 值 |
| -------- | ------- |
| 已安装驱动 | Parblo 平板驱动 v3.7.1 |
| 架构 | **x86_64（仅限 Intel）** — 无 arm64 切片 |
| 构建工具 | Xcode 10.3，目标系统 macOS 10.14（Mojave） |
| 运行方式 | Apple Silicon 上的 Rosetta 2 |
| LaunchAgent | `com.parblo.Tablet` — 登录时启动 |
| macOS 版本 | 26.5 |

**为什么 Apple 会警告您**：Apple 已宣布将在未来的 macOS 版本中移除 Rosetta 2。此 Parblo 驱动是仅支持 Intel 的二进制文件，不支持 Apple Silicon。一旦 Rosetta 被移除，驱动将无法运行。这条通知是提醒您需要制定应对计划。

**Parblo 的状态**：其官网（parblo.com）上所有 macOS 驱动仍通用地标注为“Windows&Mac” — 没有提供 Apple Silicon / ARM 专用版本。即使是最新下载内容也似乎是同一款旧 Intel 构建。联系 `cs@parblo.com` 询问是否支持 ARM 原生版本是确认其计划唯一途径，但目前没有证据表明他们已发布相关版本。

---

**您的选择**

**选项 A — OpenTabletDriver（推荐用于未来）**

[OpenTabletDriver](https://opentabletdriver.net/) v0.6.7 是一款免费、开源的平板驱动，**在 Apple Silicon 上原生运行**（无需 Rosetta）。它支持众多 Parblo 型号：

- **完全支持**：Parblo A609、A610 Pro（Variant 2）、A640 V2、Ninos N4、Ninos N7
- **存在小问题**：Parblo A610、Ninos M、Ninos N7B、Ninos S
- **缺少部分功能**：Parblo A610 Pro（滚轮不支持）、A640（辅助按钮）、Intangbo M/S（滚轮）、Intangbo SW（滚轮 + 无线）

如果您的型号在“完全支持”或“存在小问题”列表中，OpenTabletDriver 是一个干净的替代方案。通过 `brew install --cask opentabletdriver` 安装，它能在 ARM 架构上与 Rosetta 共存且无需依赖 Rosetta。

**选项 B — 继续使用当前驱动（现在可用，未来不确定）**

当前驱动通过 Rosetta 运行正常。如果您近期不打算升级 macOS，可以暂时忽略此警告。但一旦 Apple 移除 Rosetta，该驱动将无法使用。

**选项 C — 完全卸载**（如果您不再使用平板）

卸载程序已位于 `/Applications/ParbloTablet/UninstallParbloTablet.app`，或者使用 pkg 收据：在删除应用程序包和位于 `/Library/LaunchAgents/com.parblo.Tablet.plist` 的 LaunchAgent 后，执行 `pkgutil --forget com.parblo.pkg.Tablet`。

---

您使用的是哪款平板型号？我可以确切告诉您 OpenTabletDriver 对它的支持程度，或者帮助您切换过去。
