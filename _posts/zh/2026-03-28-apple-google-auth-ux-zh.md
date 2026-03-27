---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 苹果与谷歌身份认证用户体验对比
translated: true
type: note
---

问题：在 iOS 上，因为不需要额外的浏览器，Sign in with Apple 是否比 Google Login 更好？Android 支持 Sign in with Apple 吗？关于当用户混淆 Apple 和 Google 登录时产生的重复账号问题——如果两者共享相同的 email，我们需要担心吗？

回答：

## iOS 上的 Sign in with Apple vs Google Login

你是对的，iOS 上的 **Sign in with Apple** 感觉更加流畅。它使用原生的系统 API (Face ID / Touch ID)，不需要打开外部浏览器或 Chrome Custom Tab。相比之下，iOS 上的 Google Sign-In 会重定向到基于 Web 的流程，这会引入短暂的上下文切换。因此对于 iOS 用户来说，Apple Login 的体验确实明显更顺滑。

---

## Android 支持 Sign in with Apple 吗？

**支持，但有局限性。**

你可以在 Android 或 Windows 等其他平台上的参与应用和网站上使用 Sign in with Apple —— 它会显示一个由 Apple 托管的安全网页，让你登录 Apple Account。

然而，这与 iOS 有一个关键区别：

- 在 **iOS** 上，它使用原生的 FaceID/TouchID，没有浏览器弹窗。
- 在 **Android** 上，Apple Login 通过 WebView 对话框进行工作——类似于 Twitter 和 Facebook 登录在 Android 上的工作方式。因此它仍然需要一个类似浏览器的视图，失去了 iOS 用户享有的“流畅、无额外浏览器”的优势。

如果你必须在 iOS 应用中添加 Sign in with Apple，那么你的 Android 应用也需要它——否则用户从 iOS 切换到 Android 时将无法登录。因此，如果你的应用支持双平台，即使在 Android 上的体验稍逊一筹，你也应该实现它。

---

## 重复账号问题

这是一个**真实且广为人知的 UX 问题**。当 Sign in with Apple 被引入现有应用程序时，许多以前使用其他 Provider（如 Google）的用户可能会开始改用 Apple Login —— 从而失去对其原始账号数据的访问权限。这种情况被称为用户重复 (user duplication)。

如果账号共享共同的属性（例如经过验证的 email 地址），有时可以检测到重复的用户。但是，Sign in with Apple 允许用户选择将其 email 地址隐藏在每个应用唯一的别名后面，因此你不能总是依赖 email 匹配。

这是你假设中的**关键陷阱**：

### “如果他们共享相同的 email，两种方法都可以登录” —— **并不总是成立**

Apple 有一个 **"Hide My Email"** 功能。当用户选择隐藏其 email 时，Apple 会生成一个**随机的中继 email**（例如 `abc123@privaterelay.appleid.com`）而不是共享真实的 email。因此：

| 场景 | 是否安全？ |
|---|---|
| 用户使用 Apple Login 并共享真实 email | ✅ 相同 email → 可以匹配 |
| 用户使用 Apple Login 并选择 **Hide My Email** | ❌ 不同 email → 创建重复账号 |
| 用户使用其 Gmail 进行 Google Login | ✅ 真实 email，可匹配 |

---

## 你应该担心吗？这取决于应用类型

对于**轻量使用、低风险的应用**（例如：简单的工具、休闲阅读器），同一个用户拥有两个独立的账号通常是无害的。用户仍然可以独立使用任何一个账号。

对于**重度使用且有记录的应用**（电子商务、订单历史、订阅、积分、医疗数据），重复账号是一个严重的问题——用户的历史记录被拆分到两个账号中，且无法轻易找回。

### 推荐的解决方案：**Account Linking**

Account Linking 允许用户关联两个账号，以便他们可以使用其中任何一个来访问同一个用户 Profile。这可以防止账号重复，降低账号锁定的风险，并改善多平台用户的登录体验。

实践方法：
1. 登录后，检查验证过的 email 是否已存在于你的数据库中。
2. 如果存在，提示用户将新的登录方式 **Link** 到现有账号。
3. 如果使用了 Apple 的 Hide My Email，你可能需要要求用户手动确认其身份。

---

## 总结

| 主题 | 关键点 |
|---|---|
| iOS 上的 Apple Login | 流畅、原生、无浏览器 |
| Android 上的 Apple Login | 支持，但使用 WebView（不够流畅） |
| 重复账号风险 | 真实存在，特别是使用 "Hide My Email" 时 |
| 相同 email = 安全？ | 只有当用户共享真实 email 时才成立 |
| 轻量应用 | 即使有两个账号也可接受 |
| 重度应用 | 必须实现 Account Linking |

References:

- [Sign in with Apple - Apple Support](https://support.apple.com/en-us/102379)
- [Sign In with Apple on Android (Firebase)](https://firebase.google.com/docs/auth/android/apple)
- [Sign in with Apple Button for Android (GitHub)](https://github.com/willowtreeapps/sign-in-with-apple-button-android)
- [Account Linking to Improve Sign in with Apple Experience (Auth0)](https://auth0.com/blog/improving-the-sign-in-with-apple-experience-with-account-linking/)