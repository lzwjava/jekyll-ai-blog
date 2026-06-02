---
audio: false
generated: true
lang: zh
layout: post
title: 将iOS应用发布至App Store
translated: true
type: note
---

要使用 Apple Developer Program 上传 iOS 应用程序（无论是个人用途还是企业用途），您需要完成注册、准备并打包应用程序、上传以及管理更新。以下是一份分步指南，涵盖了您查询的所有方面，包括企业用途所需的邓白氏 (D-U-N-S) 编号、应用程序打包、归档文件上传以及通过 Apple 网站更新应用程序。

---

### 1. 注册 Apple Developer Program

#### 个人开发者（个人用途）

- **创建 Apple ID**：
  如果您还没有 Apple ID，请访问 [appleid.apple.com](https://appleid.apple.com)，使用个人电子邮件地址注册。
- **注册计划**：
  - 访问 [developer.apple.com/programs/](https://developer.apple.com/programs/)，点击“注册”。
  - 使用您的 Apple ID 登录。
  - 同意条款，提供您的个人法定姓名和地址，并支付每年 99 美元的费用。
- **关键提示**：您的个人姓名将作为 App Store 上的销售者显示。

#### 企业开发者（组织用途）

- **获取 D-U-N-S 编号**：
  - D-U-N-S 编号是由邓白氏分配的唯一九位数标识符，用于验证您组织的法人实体状态。Apple 要求企业账户提供此编号。
  - 在 [dnb.com](https://www.dnb.com) 上检查您的组织是否已有 D-U-N-S 编号。如果没有，请通过其网站免费申请——处理时间可能长达两周。
- **注册计划**：
  - 使用与您组织关联的 Apple ID（例如，企业电子邮件）。
  - 前往 [developer.apple.com/programs/](https://developer.apple.com/programs/)，点击“注册”。
  - 选择“组织”，并提供以下信息：
    - 法人实体名称
    - 总部地址
    - D-U-N-S 编号
  - 注册人必须具有代表组织同意 Apple 条款的法律权限。
  - 支付每年 99 美元的费用。
- **关键提示**：您的组织名称将作为 App Store 上的销售者显示。

---

### 2. 准备和打包应用程序

- **在 Xcode 中开发应用程序**：
  - 使用 Apple 的官方开发工具 Xcode 构建您的 iOS 应用程序。
  - 确保应用程序符合 [App Store 审核指南](https://developer.apple.com/app-store/review/guidelines/)。
  - 在项目设置中设置部署目标，并更新应用程序的版本号和构建号。
- **归档应用程序**：
  - 在 Xcode 中打开您的项目。
  - 选择“Generic iOS Device”（或任何模拟器）作为构建目标。
  - 在菜单栏中选择 **Product** > **Archive**。
  - Xcode 将编译您的应用程序并创建一个归档文件，这是一个准备分发的打包版本，包含代码、资源和签名信息。

---

### 3. 上传应用程序归档文件

- **使用 Xcode**：
  - 归档后，Xcode 会自动打开 Organizer 窗口。
  - 选择您的归档文件，点击 **Distribute App**。
  - 选择 **App Store Connect** 作为分发方法。
  - 按照提示验证并将归档文件上传到 App Store Connect。
- **使用 Transporter（替代方案）**：
  - 从 Mac App Store 下载 [Transporter 应用程序](https://apps.apple.com/us/app/transporter/id1450874784)。
  - 使用您的 Apple ID 登录。
  - 添加归档的应用程序文件（从 Xcode 导出为 `.ipa` 文件）并将其上传到 App Store Connect。
  - 此选项适用于高级用户或批量上传。

---

### 4. 使用 Apple 网站（App Store Connect）更新应用程序

- **访问 App Store Connect**：
  - 前往 [appstoreconnect.apple.com](https://appstoreconnect.apple.com)，使用您的 Apple ID 登录。
- **管理您的应用程序**：
  - 从仪表板中选择您的应用程序。
  - 导航到 **App Store** 选项卡。
  - 更新元数据（例如，应用程序描述、截图、关键词）。
  - 在“版本”部分，选择您上传的新构建版本。
- **提交审核**：
  - 点击 **Submit for Review**，将更新提交给 Apple 的审核团队。
  - 审核通过后，您可以手动发布或安排自动发布。

---

### 补充说明

- **企业特定细节**：
  - 确保您的 D-U-N-S 编号和组织信息准确无误，以避免注册延迟。
  - 您可以通过 App Store Connect 邀请团队成员（例如，开发人员、测试人员）到您的账户，并分配“开发人员”或“管理员”等角色。
- **常见挑战与提示**：
  - **代码签名问题**：在 Xcode 的 **Signing & Capabilities** 下验证您的证书和配置文件。如果不确定，请使用“Automatically manage signing”选项。
  - **应用程序审核被拒**：彻底测试您的应用程序，确保符合 Apple 的指南，以避免延迟。
  - **D-U-N-S 编号延迟**：如果您是企业开发者，请尽早申请 D-U-N-S 编号，因为这是注册的先决条件。

---

通过以上步骤，您可以成功使用 Apple Developer Program 上传和更新您的 iOS 应用程序，无论是作为个人还是企业开发者。更多详细信息，请参阅 Apple 官方文档 [developer.apple.com](https://developer.apple.com)。
