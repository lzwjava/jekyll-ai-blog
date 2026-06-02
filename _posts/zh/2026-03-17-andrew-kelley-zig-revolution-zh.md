---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安德鲁·凯利与 Zig 革命
translated: true
type: note
---

**问题：** 提供对 Andrew Kelley 的全面介绍，他是 Zig 编程语言的作者/创建者。

**答案：**

Andrew Kelley 是 **Zig** 的创建者、首席开发者以及主要推动力，**Zig** 是一种现代通用编程语言，被设计为 C 的更好替代品，强调健壮性、最优性能、简单性和可重用性。

### 早期背景和兴趣
Andrew 自大学时代起就参与 **free and open-source software**。他的兴趣范围很广：
- 视频游戏开发
- 数字音乐制作和跨平台声音库
- 用户界面设计
- 裸机编程
- Web 开发
- 编译器和数据库

他自称是“样样通，一专精”，Zig 显然是他主要专精和焦点。除了编程之外，他喜欢竞技街机游戏、滑板，以及学习日语 (日本語を勉強します)。

### Zig 的创建和发展
Andrew 大约在 2015–2016 年开始开发 **Zig**。他个人网站上的早期博客文章包括：
- "Introduction to the Zig Programming Language" (2016 年 2 月)
- "Zig Programming Language Blurs the Line Between Compile-Time and Run-Time" (2017 年 1 月)
- "Zig: Already More Knowable Than C" (2017 年 2 月)

Zig 的设计从 C 的简单性和控制力中汲取灵感，同时通过现代特性解决常见痛点，例如：
- **comptime**（编译时代码执行——尽管一些语言专家劝说他这是个坏主意，但他坚持追求；如今已成为 Zig 最受赞誉的功能之一）
- 无隐藏控制流或内存分配
- 出色的跨编译支持
- 内置构建系统和包管理器
- 注重安全性，而无垃圾回收或沉重运行时

2018 年 6 月，Andrew 写道，他辞去了 OkCupid（那里他担任后端工程师）的工作，转而全职依靠捐款追求 Zig——这是一个大胆举动，标志着他向专注开源工作的转变。

### Zig Software Foundation 和全职工作
2020 年，Andrew 创立了 **Zig Software Foundation** (ZSF)，这是一个 501(c)(3) 非营利组织，致力于支持 Zig 的开发。他担任其 **president** 和 **lead developer**。基金会接受捐款（包括某些时期来自 Apple 等公司的显著企业支持），并实现语言和工具链的可持续、社区支持的进展。

截至 2026 年，Andrew 继续全职从事 Zig 工作，定期发布开发日志、发行说明和改进（例如，包管理增强、libc 相关工作，以及性能优化，如 No-Libc 在某些场景中优于 Glibc）。

### 公众形象和影响力
Andrew 是会议和播客的常客演讲者：
- GOTO 会议（多次登台，包括 GOTO 2022 演讲“Intro to the Zig Programming Language”）
- FOSSY 2023
- Software Unscripted 播客（2025 年剧集）
- 各种 YouTube 访谈和技术演讲

他的个人网站 (andrewkelley.me) 托管博客文章、项目链接，并作为其工作的中心枢纽。Zig 的主要仓库已迁移至 Codeberg (codeberg.org/ziglang/zig)，反映了项目的社区导向和开放精神。

### 总结
Andrew Kelley 在系统编程社区中被广泛视为一位有原则、坚定且创新的人物，他单枪匹马启动了 Zig，并将其发展成最有前景的现代低级语言之一。通过技术卓越、对实验的开放态度（例如 comptime）以及对可持续开源资金的承诺，他将 Zig 定位为传统由 C 和 C++ 主导领域的有力竞争者。

**参考资料：**

- [Andrew Kelley's personal website](https://andrewkelley.me/)
- [Zig Programming Language official site](https://ziglang.org/)
- [Zig Software Foundation](https://ziglang.org/zsf/)
- [FOSSY 2023 speaker bio](https://2023.fossy.us/speaker/profile/154/index.html)
- [GOTO Copenhagen 2022 speaker page](https://gotocph.com/2022/speakers/2155/andrew-kelley)
