---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iPhone 13 在 iOS 26 上的 JIT 崩溃
translated: true
type: note
---

发现并诊断了崩溃原因。以下是完整情况：

## 崩溃原因

你的 iPhone 13 在 **应用启动时于 Dart VM 中崩溃**（`dart::Assert::Fail` 在 `Code::FinalizeCode` 中，"在未优化的 JIT 模式下编译未知函数时发生崩溃"）——发生在任何应用代码运行之前。

**根本原因（已对照 Flutter 的问题追踪器确认）：** 你的手机运行的是 **iOS 26.6.2**，而 iOS 26 关闭了 `get-task-allow` 漏洞，Flutter *debug* 构建正是利用该漏洞来实现 **JIT** 的。这台 Mac 上的 Flutter 引擎是 `3.27.1`（Dart 3.6.0），来自 2024 年 12 月，早于 iOS 26 的修复。在 iOS 26 上，Dart VM 无法写入/执行自己的 JIT 页面 → 启动时直接硬性中止。这是 Flutter 问题 **#163984**（相同的堆栈跟踪，相同的修复方向："除了 release 模式或更新版本的 Flutter，没有其他解决方案"）。

我测试中的证据：
- 一个**纯原生** Flutter 应用（无插件）在同一部手机上**可以正常启动** —— 所以问题不在于你的代码或 camera/ML Kit 插件。
- **执行 flutter upgrade 是持久性的修复方案**（新版 Flutter 为 iOS debug 构建使用 Dart 解释器回退方案）。

## 修复方案 — 已安装为 **release 构建**

iOS 上的 release 构建使用 **AOT 原生代码（无 JIT）**，可在 iOS 26 上正常运行（161.6 MB 的构建 vs 42 MB 的 debug —— 这就是 AOT 将 Dart 编译为机器码的结果）。我已完成：

1. 执行了 `flutter build ios --release` ✅
2. 编写了 `scripts/install_ios.sh`（构建 + 安装 + 启动）和 `scripts/watch_install.sh`
3. 启动了一个**后台监视器**，一旦 lzwjava13 重新连接就会自动安装

## 需要你操作的事项（2 分钟）

手机断开了无线配对（凌晨 2 点屏幕锁定了 😄），在它重新连接之前我无法安装。**请：**

- **唤醒/解锁你的 iPhone 13**（回到主屏幕并保持屏幕常亮，连接同一个 Wi-Fi），**或者用 USB 数据线将手机连接到 Mac**（最可靠）。

然后任选其一：
- 我会看到它连接上并自动完成安装，或者
- 你自己运行 `./scripts/install_ios.sh`。

安装完成后，点击 **Myopia Reversal** —— 现在应该可以正常启动了。（如果手机显示"未受信任的开发者"提示，请按照 设置 → 通用 → VPN 与设备管理 → 信任 进行操作。）

我是否也应该执行 **Flutter 升级**（正确的长期修复方案，让 debug 构建也能恢复工作），还是 release 构建暂时就可以了？