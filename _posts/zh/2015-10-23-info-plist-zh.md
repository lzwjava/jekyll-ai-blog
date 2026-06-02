---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 解析 Info.plist 文件
translated: true
type: post
---

如果你曾经从事过 macOS 或 iOS 开发，很可能遇到过一个 `Info.plist` 文件。这个基于 XML 的文件是任何 Apple 应用程序或插件的关键部分，就像一本护照，告诉系统它是谁，它做什么，以及它应该如何行为。今天，我们将探讨来自 "Reveal-In-GitHub" 的 `Info.plist`，这是我们在之前的文章中介绍的一个 Xcode 插件。我们不会逐行分析，而是专注于定义其目的和功能的核心概念和模式。

---

#### 什么是 `Info.plist` 文件？

`Info.plist`（简称“Information Property List”）是一个结构化的文件，包含有关应用程序、插件或捆绑包的元数据。用 XML 编写（具有特定的 Apple 定义的模式），它使用键值对来描述应用程序的名称、版本和兼容性等基本信息。对于 "Reveal-In-GitHub"，这个文件将其标识为一个 Xcode 插件，并确保它能够与 IDE 无缝集成。

与 `.pbxproj` 文件不同，后者是关于如何构建某物，`Info.plist` 是关于某物是什么。它是身份和意图的声明。

---

#### 文件中的关键概念

1. **捆绑基础**
   多个键将插件定义为一个 macOS 捆绑包：
   - **`CFBundleExecutable`**：设置为 `$(EXECUTABLE_NAME)`，这是编译后的二进制文件名称的占位符（在构建过程中定义）。
   - **`CFBundleIdentifier`**：`$(PRODUCT_BUNDLE_IDENTIFIER)` 解析为 `com.lzwjava.Reveal-In-GitHub`，这是一个唯一的反向 DNS 风格的 ID，用于区分这个插件与其他插件。
   - **`CFBundlePackageType`**：`BNDL` 将其标记为一个捆绑包，这是 macOS 上插件和库的常见格式。
   - **`CFBundleName`**：`$(PRODUCT_NAME)` 将成为 "Reveal-In-GitHub"，这是一个人类友好的名称。

2. **版本控制和所有权**
   - **`CFBundleShortVersionString`**："1.0" 是用户可见的版本。
   - **`CFBundleVersion`**："1" 是内部构建号。
   - **`NSHumanReadableCopyright`**："Copyright © 2015年 lzwjava. All rights reserved." 归功于创建者 `lzwjava`，并将插件日期定为 2015 年。
   - **`CFBundleSignature`**："????" 是一个占位符（通常是一个四个字符的代码），尽管对于插件来说它不太重要。

3. **本地化**
   - **`CFBundleDevelopmentRegion`**："en" 将英语设置为默认语言，影响资源（如果有）的本地化方式。

4. **Xcode 插件兼容性**
   这里的突出特性是 **`DVTPlugInCompatibilityUUIDs`**，这是一个长的 UUID 数组。这些 UUID 与特定的 Xcode 版本（例如 Xcode 6、7 等）匹配，确保插件只在兼容的 IDE 中加载。这个列表非常广泛，表明 "Reveal-In-GitHub" 被设计为跨多个 Xcode 发布版本工作——这是一个深思熟虑的向前和向后兼容性的标志。

5. **插件特定设置**
   - **`NSPrincipalClass`**：留空（`<string></string>`），暗示插件可能会动态定义其入口点或依赖 Xcode 的约定。
   - **`XC4Compatible` 和 `XC5Compatible`**：都为 `<true/>`，确认与 Xcode 4 和 5 兼容。
   - **`XCGCReady`**：`<true/>` 表示准备好进行垃圾回收，这是一个较旧的 macOS 内存管理功能（主要在 2015 年之前被 ARC 取代）。
   - **`XCPluginHasUI`**：`<false/>` 表明没有超出 Xcode 内置的自定义 UI——尽管这似乎与 `.pbxproj` 中的 `.xib` 文件冲突。也许 UI 很小或处理方式不同。

---

#### 要注意的模式

1. **占位符以提供灵活性**
   如 `$(EXECUTABLE_NAME)` 和 `$(PRODUCT_BUNDLE_IDENTIFIER)` 这样的键使用与构建系统相关的变量（在 `.pbxproj` 中定义）。这使得 `Info.plist` 可以在不同的配置（例如调试与发布）之间重用。

2. **简洁设计**
   这个文件非常简洁，专注于基本要素。没有花哨的图标、权限或应用程序特定的设置——只是 Xcode 插件需要的功能。这种简洁性对于扩展现有应用程序（Xcode）的插件是典型的，而不是独立程序。

3. **兼容性为重**
   广泛的 `DVTPlugInCompatibilityUUIDs` 列表和 `XC4Compatible` 标志表明这是一个建造来持久的插件。这种模式在开发者工具中很常见，用户可能会因为稳定性而坚持使用较旧的 Xcode 版本。

4. **元数据而非行为**
   与代码文件不同，`Info.plist` 不做任何事情——它描述。它的角色是被动的，提供 Xcode 和 macOS 在运行时解释的信息。

---

#### 这告诉我们关于 Reveal-In-GitHub 的什么？

这个 `Info.plist` 将 "Reveal-In-GitHub" 描绘为一个轻量级、专注的 Xcode 插件，可能由一个独立开发者（`lzwjava`）在 2015 年创建。其广泛的兼容性表明它被设计为广泛使用，而缺少 UI 标志（尽管项目中有一个 `.xib`）暗示着一种微妙的集成——可能是一个菜单项或上下文操作，而不是一个花哨的界面。根据名称和 `.pbxproj` 的上下文，它可能简化了 GitHub 工作流程，例如将 Xcode 文件链接到它们的在线仓库。

---

#### 为什么这很重要

`Info.plist` 是你的应用程序与系统的握手。对于开发者来说，理解它意味着你可以调整兼容性、版本控制或行为，而不需要修改代码。对于 "Reveal-In-GitHub"，它是无缝嵌入 Xcode 的关键。下次你在调试插件或创建自己的插件时，这个文件将是你的起点——小而强大。
