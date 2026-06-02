---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源浏览器指南
translated: true
type: note
---

**问题：** 有哪些好的开源浏览器可以使用？Safari 是否开源了其任何组件？

**答案：**

## 值得使用的开源浏览器

### 第一梯队 — 可作为日常主力

**Firefox**（Mozilla）
- 完全开源（MPL 2.0），自有引擎：**Gecko** + **SpiderMonkey**（JavaScript)
- 仓库：[github.com/mozilla/gecko-dev](https://github.com/mozilla/gecko-dev)
- 除 WebKit 外唯一仍存的主流非 Chromium 引擎
- 优势：隐私保护、开发者工具、扩展生态、非 Google 引擎多样性

**Brave**
- 开源（MPL 2.0），基于 Chromium（Blink 引擎）
- 仓库：[github.com/brave/brave-browser](https://github.com/brave/brave-browser)
- Brave 自动拦截有害广告、跟踪像素和 Cookie，并将网站重定向至 HTTPS。支持 macOS、Windows 和 Linux。
- 许多人认为 Brave 已取代 Firefox 在开源世界的原有领先地位。
- 优势：日常使用、内置广告拦截、Chromium 兼容性、无 Google 跟踪

**Chromium**
- Chrome 的上游项目，完全开源
- 仓库：[chromium.googlesource.com/chromium/src](https://chromium.googlesource.com/chromium/src)
- 优势：可调试与 Chrome 渲染效果完全一致的 Web 应用，且不含 Google 遥测信息

### 第二梯队 — 开发者/小众选择

**ungoogled-chromium**
- 移除所有 Google API 调用的 Chromium 版本
- 仓库：[github.com/ungoogled-software/ungoogled-chromium](https://github.com/ungoogled-software/ungoogled-chromium)

**Ladybird**（从技术层面看最令人兴奋）
- 基于完全原创引擎构建的新浏览器——与 Blink、WebKit、Gecko 或任何现有引擎无代码共享。非盈利支持，完全通过捐赠和赞助运营，无搜索交易、无数据收集、无广告。首个 Alpha 版本计划于 2026 年面向 Linux 和 macOS 发布，目标用户为开发者和早期采用者。目前有八名全职工程师与社区贡献者共同开发。近期更新包括：内联 PDF 查看器、浏览历史、HTTP 缓存、媒体流、CSS 锚点定位、线程外 JavaScript 编译以及全新正则引擎。
- 这是目前架构上最值得关注的浏览器——值得持续跟进。

---

## Safari 与开源

Safari 本身（应用外壳、界面、同步等功能）是**闭源专有**的。但其两大核心引擎是开源的：

**WebKit** — 渲染/布局引擎
- WebKit 是一款面向浏览器及其他应用的开源网页内容引擎。由 Apple 开发并开源。WebKit 项目优先考虑真实网页兼容性、标准合规性、稳定性、性能、电池续航、安全性、隐私、可移植性及可扩展性。
- 仓库：[github.com/WebKit/WebKit](https://github.com/WebKit/WebKit)
- 许可证：LGPL 2.1（WebCore）+ BSD（JavaScriptCore）

**WebKit 内部组件：**
- **WebCore** — HTML/CSS 布局与渲染（DOM、绘制管线）
- **JavaScriptCore (JSC)** — Apple 的 JavaScript 引擎，相当于 V8/SpiderMonkey
- 两者自 2005 年起已开源。2005 年 6 月，Apple 宣布将 WebKit 整体开源（此前仅 WebCore 和 JavaScriptCore 为开源），据称此举是为了与 KDE 及开源社区更紧密合作。

**闭源部分：** Safari 的 UI、iCloud 同步、Handoff、Keychain 集成、Private Relay 等均为专有。

---

## 快速参考

| 浏览器 | 引擎 | 是否开源 | 备注 |
|---|---|---|---|
| Firefox | Gecko/SpiderMonkey | ✅ 完全开源 | 唯一非 Blink/WebKit 的主流引擎 |
| Brave | Blink/V8 | ✅ 完全开源 | 隐私保护最佳日常主力 |
| Chromium | Blink/V8 | ✅ 完全开源 | Chrome 上游项目 |
| ungoogled-chromium | Blink/V8 | ✅ 完全开源 | Chromium 去除 Google 遥测 |
| Ladybird | LibWeb（自定义） | ✅ 完全开源 | 全新构建，Alpha 2026 |
| Safari | WebKit/JSC | ❌ 应用闭源，✅ 引擎开源 | WebKit/JSC 为开源 |
| Chrome | Blink/V8 | ❌ 闭源 | 基于开源 Chromium |

**我的推荐：** 日常使用可选 Brave 或 ungoogled-chromium。Ladybird 值得克隆并运行体验——看看从头构建浏览器引擎是怎样的过程，非常符合 Karpathy 式的学习风格。

参考资料：
- [WebKit 开源项目](https://webkit.org/)
- [Apple 开源项目 — WebKit](https://opensource.apple.com/projects/webkit/)
- [Ladybird 浏览器](https://openalternative.co/alternatives/brave)
