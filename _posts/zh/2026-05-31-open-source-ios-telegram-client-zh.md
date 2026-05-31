---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源iOS Telegram客户端
translated: true
type: note
---

以下是您正在查看的内容：

**Telegram-iOS** — Telegram Messenger 的官方开源 iOS 客户端。

**仓库：** `git@github.com:TelegramMessenger/Telegram-iOS.git`
**大小：** 磁盘上 572 MB
**版本：** 12.7（需要 Xcode 26.2、macOS 26、Bazel 8.4.2）

**代码构成：**
- 4,182 个 Swift 文件（主要语言）
- 901 个 Objective-C (.m/.mm) 文件

**架构：**

该项目通过 `build-system/Make/Make.py` 包装器使用 **Bazel** 构建。其组织结构如下：

| 目录 | 用途 |
|-----------|---------|
| `Telegram/` | 主应用目标、扩展（NotificationContent、Share、Watch、WidgetKitWidget、SiriIntents） |
| `submodules/` | **273 个内部库** — 代码库的主体 |
| `third-party/` | 第三方 C/C++ 依赖（ffmpeg、openssl、sqlcipher、libvpx、opus、webrtc、rlottie、libjxl、dav1d、mozjpeg、libyuv） |
| `build-system/` | Bazel 规则（rules_apple、rules_swift、rules_xcodeproj）和构建配置 |

**关键子模块**（共 273 个）包括：
- **TelegramCore** — 网络、存储、业务逻辑
- **TelegramUI** — UI 组件
- **TelegramApi** — MTProto API 绑定
- **Postbox** — 本地数据库（基于 sqlcipher 的键值存储）
- **TelegramCallsUI** / **TgVoipWebrtc** — 语音/视频通话
- **AccountContext** / **AccountUtils** — 多账户支持
- **AsyncDisplayKit** — 异步基于节点的 UI 渲染（Texture 分支）
- **Display**、**ComponentFlow** — UI 框架层

**正在进行的重构**（记录在 CLAUDE.md 中）：一项超过 45 波的迁移工作，将 `Postbox` 直接导入替换为 `TelegramEngine` 类型别名——这是一次清理分层重构，消除消费模块对数据库的直接依赖。

**Git 历史**（最新提交）：常规修复、投票改进、动画清理——看起来像是上游 Telegram 仓库的活跃维护分支或克隆。

**构建方式：**
```sh
python3 build-system/Make/Make.py --overrideXcodeVersion \
  --cacheDir ~/telegram-bazel-cache \
  build \
  --configurationPath build-system/appstore-configuration.json \
  --gitCodesigningRepository git@gitlab.com:peter-iakovlev/fastlanematch.git \
  --gitCodesigningType development --gitCodesigningCurrent --buildNumber=1 --configuration=debug_sim_arm64
```

这是一个庞大且结构良好的代码库——是最大的开源 iOS 项目之一。