---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flarum 移动应用状态
translated: true
type: note
---

**问题：** Flarum 有移动端应用吗？

**回答：**

**没有官方应用。** 以下是当前情况：

**PWA（渐进式 Web 应用）—— 最佳选择**

- Flarum 通过扩展支持 PWA，允许 Android 和 iOS 用户从浏览器像安装应用一样“安装”它。
- 安装 PWA 扩展后，你还可以使用 PWABuilder 为 iOS 和 Android 构建安装包。
- Android 通过 PWA 支持推送通知；iOS 支持情况取决于你的 iOS 版本。

**非官方 / 社区应用**

- 有一个使用 SwiftUI 构建的社区版 Flarum iOS 应用演示，提供登录、浏览讨论、回复、标签支持、用户资料和深色模式等功能，但需要自行编译，且绑定特定的 Flarum 安装地址。
- Flarum BV（Flarum Foundation 的商业合作伙伴）一直在致力于将 PWA 扩展封装为 Android 和 iOS 应用，并计划以小额费用为社区将其发布到应用商店。

**为何没有官方应用？**

- 制作应用是一个复杂的过程，需要大量投入——无论是初期开发还是长期维护——而 Flarum 团队目前缺乏必要的资源来承接此类项目。

**与 Discourse 相比**，后者在 iOS 和 Android 上都有官方 **DiscourseHub** 应用，这对 Flarum 而言是一个明显的差距。

**建议：** 对大多数用户来说，将 Flarum 作为 **PWA** 安装是目前获得接近原生应用体验的最简单途径。

**参考链接：**

- [Flarum 社区 - 推送通知与应用支持](https://discuss.flarum.org/d/31898-edition-422-community-update)
- [Flarum iOS 应用（非官方，SwiftUI）](https://discuss.flarum.org/d/33090-flarum-ios-app-demo-swiftui)
- [将 Flarum 应用构建并发布到 iOS 和 Android](https://discuss.flarum.org/d/34301-building-and-publishing-your-flarum-apps-to-ios-and-android)
