---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS IAM访问权限管理指南
translated: true
type: note
---

AWS Identity and Access Management（IAM）是一项免费服务，可帮助您安全地控制对 AWS 资源的访问。它使您能够管理用户及其权限，确保合适的人员和应用程序能够以恰当方式访问相应的资源。IAM 负责处理身份验证（谁可以登录）和授权（他们可以执行哪些操作）。

## IAM 核心组件

- **用户**：代表需要访问 AWS 的个人或应用程序。每个用户都拥有唯一的安全凭证（例如密码或访问密钥）。
- **组**：用户的集合，便于权限管理。权限直接附加到组而非单个用户。
- **角色**：具有权限的临时身份，可供用户、服务或应用程序担任。角色没有永久凭证，而是提供短期安全令牌。
- **策略**：定义权限的 JSON 文档。它们指定操作（例如读取、写入）、资源（例如 S3 存储桶）和条件（例如 IP 限制）。策略分为 AWS 托管策略、客户托管策略和内联策略。

## 入门指南：分步说明

### 先决条件
- 以根用户身份（使用您的账户邮箱和密码）登录 AWS 管理控制台。**重要提示**：请勿使用根用户执行日常任务——应立即创建管理员用户。
- 为根用户启用多因素认证（MFA）以增强安全性。

### 1. 创建 IAM 用户
为简化操作建议使用 AWS 管理控制台（也可通过 CLI 或 API 实现自动化创建）。

1. 通过 https://console.aws.amazon.com/iam/ 打开 IAM 控制台。
2. 在导航窗格中选择 **Users** > **Create user**。
3. 输入用户名（例如 "admin-user"）并选择 **Next**。
4. 在 **Set permissions** 下选择 **Attach policies directly**，然后选择 AWS 托管策略（如 "AdministratorAccess"）以获取完全访问权限（生产环境请遵循最小权限原则）。
5. （可选）设置控制台密码：选择 **Custom password** 并启用 **Require password reset**。
6. 检查信息后选择 **Create user**。
7. 向用户提供登录 URL（例如 https://[账户别名].signin.aws.amazon.com/console）、用户名和临时密码。

如需编程访问，可生成访问密钥（但建议应用程序优先使用角色）。

### 2. 创建和管理组
通过组可简化权限扩展管理。

1. 在 IAM 控制台中选择 **User groups** > **Create group**。
2. 输入组名称（例如 "Developers"）。
3. 附加策略（例如 "AmazonEC2ReadOnlyAccess"）。
4. 选择 **Create group**。
5. 添加用户：选择目标组 > **Add users to group** > 选择现有用户。

用户将继承所在组的全部权限。单个用户可属于多个组。

### 3. 创建和附加策略
策略用于定义允许执行的操作。

- **类型**：
  - AWS 托管策略：针对常见任务预构建（例如 "ReadOnlyAccess"）。
  - 客户托管策略：根据需求自定义 JSON 策略。
  - 内联策略：直接嵌入用户/组/角色中（请谨慎使用）。

创建自定义策略步骤：
1. 在 IAM 控制台选择 **Policies** > **Create policy**。
2. 使用可视化编辑器或 JSON 选项卡（例如允许对特定存储桶执行 "s3:GetObject"）。
3. 命名策略后选择 **Create policy**。
4. 通过 **Attach policy** 将其附加到用户/组/角色。

最佳实践：遵循最小权限原则——初始设置可稍宽泛，随后使用 IAM Access Analyzer 等工具进行细化。

### 4. 使用 IAM 角色
角色适用于临时访问场景，可避免使用长期凭证。

1. 在 IAM 控制台选择 **Roles** > **Create role**。
2. 选择受信任实体（例如 EC2 选择 "AWS service"，跨账户选择 "Another AWS account"）。
3. 附加权限策略。
4. 添加信任策略（定义可担任角色的 JSON，例如 EC2 服务主体）。
5. 命名角色后选择 **Create role**。

**常见场景**：
- **EC2 实例**：将角色附加到实例，无需嵌入密钥即可安全访问其他服务（如 S3）。
- **跨账户访问**：在账户 A（信任方）创建角色，其信任策略允许账户 B 的主体。B 账户用户通过 AWS STS 担任角色以访问 A 账户资源。

可通过控制台、CLI（`aws sts assume-role`）或 SDK 担任角色以获取临时凭证。

### 5. 启用 MFA 与增强安全
- 为用户启用：在 IAM 控制台 > Users > 选择用户 > **Security credentials** > Manage MFA。
- 建议使用虚拟（基于应用程序）或硬件 MFA 设备。

## 安全最佳实践
- **锁定根用户**：仅用于必需任务（如修改账户设置）。启用 MFA 且勿创建访问密钥。
- **使用临时凭证**：优先采用联合身份验证（例如通过 IAM Identity Center）和角色而非长期密钥。若使用密钥请定期轮换。
- **最小权限原则**：授予最低必要权限；在策略中使用条件限制（如时间/IP 限制）。
- **监控与审计**：启用 AWS CloudTrail，使用 IAM Access Analyzer 检测未使用权限或意外访问，定期查看最后使用时间信息。
- **清理未使用资源**：定期删除闲置用户/角色/策略。
- **多账户管理**：通过 AWS Organizations 结合服务控制策略（SCP）设置防护机制。
- **验证策略**：应用前使用 IAM Access Analyzer 的策略检查功能。

如需实践学习，可通过控制台或文档中的 IAM 教程探索基于属性的访问控制（ABAC）等场景。

## 参考文档
- [什么是 IAM？](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [创建 IAM 用户](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html)
- [IAM 组](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html)
- [IAM 角色](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [IAM 最佳实践](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [IAM 教程](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorials.html)
