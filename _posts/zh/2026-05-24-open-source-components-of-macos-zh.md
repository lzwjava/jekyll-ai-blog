---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS的开源组件
translated: true
type: note
---

**问题：** macOS 是否有开源组件？在哪里可以找到源代码？

**回答：**

是的——macOS 部分开源。苹果将这个集合称为 **Darwin**，它涵盖了核心操作系统层。具体如下：

## 开源部分

### 1. Darwin / XNU 内核
内核本身——**XNU**（X is Not Unix）——是开源的。它是一个混合内核，结合了：
- **Mach** 微内核（来自 CMU）
- **BSD**（基于 FreeBSD）层
- **IOKit**（驱动框架）

→ **源代码：** https://github.com/apple-oss-distributions/xnu

### 2. Apple OSS Distributions
苹果发布了一大批随 macOS 一起提供的开源组件：

→ **主站：** https://opensource.apple.com/

→ **GitHub 组织：** https://github.com/apple-oss-distributions

其中包括：`dyld`、`libdispatch`（GCD）、`libc`、`launchd`、`zsh`、`bash`、`curl`、`WebKit`、`clang/LLVM`、`Swift stdlib`、`libpthread` 以及数百个其他组件。

### 3. LLVM / Clang
苹果是主要贡献者之一。Xcode 附带的 `clang` 是苹果的分支。

→ https://github.com/llvm/llvm-project

### 4. Swift
完全开源。

→ https://github.com/apple/swift

### 5. WebKit
Safari 背后的浏览器引擎。

→ https://github.com/WebKit/WebKit

---

## 闭源部分

Darwin 层之上的所有内容都是专有的：

- **AppKit / UIKit / SwiftUI** — UI 框架
- **CoreGraphics, Metal** — GPU/渲染栈
- **Finder, Spotlight, Siri** — 面向用户的应用程序
- **安全隔区**固件
- **WindowServer** — 合成器
- **CoreML 运行时内部**

---

## 快速参考

| 组件 | 开源？ | URL |
|---|---|---|
| XNU 内核 | ✅ | github.com/apple-oss-distributions/xnu |
| dyld（动态链接器） | ✅ | github.com/apple-oss-distributions/dyld |
| libdispatch（GCD） | ✅ | github.com/apple/swift-corelibs-libdispatch |
| launchd | ✅ | github.com/apple-oss-distributions/launchd |
| Swift | ✅ | github.com/apple/swift |
| WebKit | ✅ | github.com/WebKit/WebKit |
| AppKit/UIKit | ❌ | 闭源 |
| Metal | ❌ | 闭源 |
| WindowServer | ❌ | 闭源 |

---

## 实用提示

如果你想在阅读 XNU 源代码的同时对照内核行为，可以配合以下命令使用：
```bash
# 查看你的 macOS 版本 → 匹配到 XNU 发行标签
sw_vers -productVersion
# 然后在以下地址找到匹配的标签：
# https://github.com/apple-oss-distributions/xnu/tags
```

苹果并不总是在系统发布的同时发布源代码——通常在重大版本发布后会有数周到数月的延迟。