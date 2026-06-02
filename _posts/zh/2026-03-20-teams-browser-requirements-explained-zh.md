---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微软 Teams 受支持浏览器要求详解
translated: true
type: note
---

**问题：** 当您的组织要求您安装“approved browser”来查看 Microsoft Teams 链接时——这在大公司中很常见——这意味着什么，如何修复，哪些浏览器是 approved 的，以及为什么 iOS Safari 不起作用？

---

**答案：**

## 为什么会出现“Install an Approved Browser”

此消息来自 **Microsoft Entra ID (Azure AD) Conditional Access policies**，大型企业会强制执行这些策略。当您的 IT/安全团队配置要求“approved client app”或“app protection policy”的策略时，除非使用 Microsoft 正式认可为合规且可通过 Intune 管理的浏览器或应用，否则会阻止访问 Microsoft 365 资源——包括 Teams。

Safari 支持托管设备上的基于设备的 Conditional Access，但它 **无法满足** “Require approved client app”或“Require app protection policy”条件。像 Microsoft Edge 这样的托管浏览器可以满足 approved client app 和 app protection policy 要求。在使用非 Microsoft MDM 解决方案的 iOS 上，只有 Microsoft Edge 浏览器支持设备策略。

这就是 iOS Safari 失败的核心原因——它根本无法通过这些企业合规检查，无论更新到什么程度。

---

## 什么是“Approved”浏览器？

Teams web 客户端可在 **Microsoft Edge**、**Chrome**、**Firefox** 和 **Safari** 浏览器上使用——但仅限于 **desktop computer**。

然而，对于企业 Conditional Access 策略，具体层级如下：

| Browser | Desktop Support | iOS/Mobile | Passes "Approved App" Policy |
|---|---|---|---|
| **Microsoft Edge** | ✅ Full | ✅ (Intune-managed) | ✅ Yes |
| **Google Chrome** | ✅ Full | ❌ No web Teams | ⚠️ Partial |
| **Firefox** | ✅ Full | ❌ No | ⚠️ Partial |
| **Safari (macOS)** | ✅ With issues | ❌ Not supported | ❌ No |
| **iOS Safari** | N/A | ❌ Not supported | ❌ No |

Microsoft 推荐使用 **Google Chrome** 或 **Microsoft Edge** 访问 Microsoft 365 在线应用，包括 Teams。在 Apple 电脑上的 Safari 和 macOS/Windows 上的 Firefox 上已注意到已知问题。

---

## 如何修复（按场景）

### ✅ 修复 1：在 Desktop/Laptop 上——使用 Microsoft Edge 或 Chrome

最简单的修复。在最新版本的 **Microsoft Edge**（企业 SSO 首选）或 **Google Chrome** 中打开 Teams 链接。对于 cookies，您可能还需要在浏览器的“Privacy and Security”设置中允许 Microsoft Teams URL 的第三方 cookies。

### ✅ 修复 2：在 iOS 上——安装 Microsoft Teams 移动应用

Teams web 当前 **不支持移动设备**。要在移动设备上使用 Teams，必须下载 **Teams 移动应用**。这是 iOS 用户的官方解决方案。

### ✅ 修复 3：在 iOS（企业托管）上——使用 iOS 版 Microsoft Edge

iOS 版 Microsoft Edge 被认可为托管/approved 浏览器，因此可以满足 conditional access grant controls。其他非 Microsoft 应用会被重定向到 Edge 完成身份验证。如果您的 IT 团队已将您的 iPhone 注册到 Intune (MDM)，安装 **iOS 版 Microsoft Edge** 并使用公司帐户登录可能允许访问。

### ✅ 修复 4：联系 IT / 请求豁免

在企业或学术环境中，IT 管理员可能强制执行特定登录方法或限制外部会议链接。如果您怀疑策略在干扰，请联系 IT 部门确认您是否有权限加入外部或公共 Teams 会议。

### ✅ 修复 5（管理员）：审查 Conditional Access 策略

组织必须在 **2026 年 6 月 30 日** 前将使用“Require approved client app”的 Conditional Access 策略过渡到同时包含“Require app protection policy”。Microsoft 将在该日期后停止强制执行旧的“Require approved client app” grant control。IT 管理员应审查这些策略，确保不会无意中锁定有效用户。

---

## 为什么 iOS Safari 特别失败

iOS（和 iPadOS）浏览器从根本上受限：

1. 所有 iOS 浏览器——Edge、Safari、Chrome、Firefox——都会显示页面提示“Your browser version isn't supported. Quickest solution? Download the mobile app.” 这适用于 iOS 浏览器上的 web 客户端。

2. 截至 2025 年中，Teams 不再支持通过 Safari 安装为 PWA。Microsoft 官方文档现在仅将 **Edge 和 Chrome** 列为支持安装 Teams 作为 PWA 的浏览器。

3. 此外，企业 Conditional Access 策略要求浏览器通过 Intune app protection 检查——在 Apple 移动设备上，只有 iOS 版 Edge 可以做到这一点。

---

## 总结

企业 Microsoft Teams 访问的 **正确 approved 浏览器** 是：

- **Desktop**：Microsoft Edge（SSO 最佳）、Google Chrome、Firefox
- **iOS/iPhone**：Microsoft Teams 应用（官方）或 iOS 版 Microsoft Edge（Intune 托管）
- **iOS Safari**：不支持——改用 Teams 应用

---

**参考资料：**

- [Microsoft Learn: Teams for Web — Overview and Prerequisites](https://learn.microsoft.com/en-us/microsoftteams/teams-client-web)
- [Microsoft Learn: Conditional Access Conditions (Browser support)](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-conditions)
- [Microsoft Learn: Migrate Approved Client App Policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/migrate-approved-client-app)
- [Microsoft Q&A: Teams is not supported on any iOS browser](https://learn.microsoft.com/en-us/answers/questions/4382369/teams-is-not-supported-on-any-ios-browser)
- [Microsoft Q&A: Did Microsoft remove Safari support for Teams PWA?](https://learn.microsoft.com/en-us/answers/questions/5518049/did-microsoft-remove-safari-support-for-teams-pwa)
- [Microsoft Learn: Troubleshooting Teams sign-in loops](https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-sign-in/sign-in-loop)
