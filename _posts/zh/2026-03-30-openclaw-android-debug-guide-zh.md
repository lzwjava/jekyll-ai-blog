---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw Android 开发与调试指南
translated: true
type: note
---

**Question:** Android Studio 如何通过 ADB 与 OpenClaw 配合工作，以及如何使用它在连接的实体手机上构建、运行和调试 Android app？

**Answer:**

## OpenClaw + Android Studio + ADB：在实体 Android 手机上构建、运行与调试

OpenClaw 是一个 AI agent 平台（"the lobster way 🦞"），它通过 ADB 连接到 Android。以下是各组件如何协同工作的详细说明。

---

### 🔍 什么是 Android 上的 OpenClaw？

OpenClaw 的 Android app 扮演的是 **companion node**（伴随节点）的角色 —— Android 本身并不运行 Gateway。Gateway 是必需的，且必须通过 WSL2 在 macOS、Linux 或 Windows 上运行。Android node app 通过 mDNS/NSD 和 WebSocket（默认 `ws://<host>:18789`）连接到 Gateway。

Android app 的状态目前处于 **extremely alpha** 阶段，并且正在进行彻底的重构。

---

### 📱 步骤 1：在 Android 手机上启用 ADB

1. 进入 **Settings → About Phone** → 连续点击 **Build Number** 7 次以启用 Developer Options。
2. 进入 **Settings → Developer Options** → 启用 **USB Debugging**。
3. 通过 USB 连接手机，并在手机上 **接受调试信任提示**。

如果 `adb devices -l` 显示 `unauthorized`，请重新插拔电缆并再次接受信任提示。然后使用 `adb reverse`，使 Android 的 `localhost:18789` 隧道连接到笔记本电脑的 `localhost:18789`。

```bash
adb reverse tcp:18789 tcp:18789
```

---

### 🏗️ 步骤 2：在 Android Studio 中打开并构建 Android App

在 Android Studio 中打开 `apps/android` 文件夹。要进行构建和运行：

```bash
cd apps/android
./gradlew :app:assembleDebug
./gradlew :app:installDebug
```

你也可以运行 unit tests：
```bash
./gradlew :app:testDebugUnitTest
```

如果未设置 `ANDROID_SDK_ROOT` / `ANDROID_HOME`，`gradlew` 会自动检测位于 `~/Library/Android/sdk`（macOS 默认路径）的 Android SDK。

或者，你可以构建 Play Store debug 变体：

```bash
./gradlew :app:assemblePlayDebug
```

---

### ▶️ 步骤 3：在实体手机上运行 App

该 app 是 **native Kotlin + Jetpack Compose** 开发的。对于使用 **Compose** 的 UI 修改，请在 debug build 上使用 **Android Studio Live Edit** —— 这适用于实体设备，并要求项目的 `minSdk=31`。

应用更改有三个级别：

| 更改类型 | 方法 |
|---|---|
| Compose UI 修改 | **Live Edit** (即时，无需重新安装) |
| 非结构化代码/资源 | **Apply Changes** |
| 结构化/native/manifest/Gradle | 通过 `pnpm android:run` 完整重新安装 |

当从 Gateway 的 `__openclaw__/canvas/` 加载时，Canvas web 内容已经支持 **live reload**。

---

### 🐛 步骤 4：使用 Android Studio 调试

标准的 Android Studio 调试工具完全可用：

- **Logcat** — 查看实时设备日志
- **Debugger** — 在 Kotlin/Java 代码中设置断点
- **Layout Inspector** — 在设备上实时检查 Compose/View 层级
- **Network Inspector** — 监控流向 OpenClaw Gateway 的 WebSocket 流量

由于 app 使用 Kotlin + Jetpack Compose，你可以使用 **Android Studio Hedgehog 或更高版本** 以获得最佳的 Compose 调试支持（Compose Preview、Live Edit 等）。

---

### 🔌 步骤 5：将 App 连接到 OpenClaw Gateway

打开 app 中的 **Connect** 选项卡。使用 **Setup Code** 或 **Manual** 模式进行连接。Android app 作为 node 设备与 Gateway 配对。

对于通过 ADB 的 Gateway 隧道：
```bash
adb reverse tcp:18789 tcp:18789
```

这使得手机可以像访问本地一样访问笔记本电脑上位于 `localhost:18789` 的 Gateway。

---

### 🤖 步骤 6：通过 ADB 进行 AI 驱动的 App 控制 (DroidClaw / OpenClaw Agent)

除了构建你自己的 app，OpenClaw 还可以作为 AI agent **通过 ADB 控制 Android apps**：

OpenClaw 在笔记本电脑上充当桥梁，agent 通过 ADB 在你的 Android 设备上执行任务。Agent 使用 **Perception → Reasoning → Action** 循环 —— 它通过 ADB 导出手机的 accessibility tree，将 XML 解析为交互式 UI 元素，并获取截图。

ClawMobile 是一个相关项目，它直接在移动设备上运行 OpenClaw，并将其与 **structured UI automation 和 deterministic mobile control layers**（ADB、Termux 和基于 Accessibility 的工具）集成。这使得 agent 能够主动操作 app、检查 UI 状态并执行可靠、可重复的工作流 —— 无需任何远程控制服务器。

---

### 🧪 性能基准测试 (Bonus)

你可以通过以下命令运行 macrobenchmarks（启动 + 帧耗时）：

```bash
cd apps/android
./gradlew :benchmark:connectedDebugAndroidTest
```

报告将写入 `apps/android/benchmark/build/reports/androidTests/connected/`。

---

### ⚠️ 运行/调试前的重要检查清单

在运行测试或调试之前：
- Android app 必须连接到 Gateway 并显示为 **paired + connected**。
- 在整个会话期间，app 必须保持 **解锁并在前台运行**。
- 如果需要 canvas/A2UI 命令，**Screen 选项卡** 必须处于打开和活动状态。
- 必须授予所有必需的 **runtime permissions**（摄像头、麦克风、位置、通知）。
- 在测试开始前，不应有待处理的交互式系统对话框。

---

**参考资料：**

- [OpenClaw Android README (GitHub)](https://github.com/openclaw/openclaw/blob/main/apps/android/README.md)
- [OpenClaw Android Docs](https://docs.openclaw.ai/platforms/android)
- [DroidClaw Guide (Medium)](https://medium.com/write-a-catalyst/from-openclaw-to-droidclaw-your-friendly-guide-to-android-ai-automation-2b17de9ed67f)
- [ClawMobile GitHub](https://github.com/ClawMobile/ClawMobile)
- [openclaw-android (AidanPark, single-command Android setup)](https://github.com/AidanPark/openclaw-android)
- [Running OpenClaw Locally on Android via Termux](https://sagartamang.com/blog/openclaw-on-android-termux)
