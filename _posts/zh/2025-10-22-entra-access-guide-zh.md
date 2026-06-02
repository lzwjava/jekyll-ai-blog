---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Microsoft Entra 身份访问管理指南
translated: true
type: note
---

Microsoft Entra ID 是一款基于云的身份和访问管理服务，可帮助保护对应用程序、数据和设备等资源的访问。它支持身份验证（例如登录方法、MFA）、授权（例如基于角色的访问）以及与 Azure 服务的集成。要开始使用，您需要一个 Azure 订阅和适当的权限（例如全局管理员角色）。

## 入门指南
1. **登录 Azure 门户**：访问 [portal.azure.com](https://portal.azure.com) 并使用您的 Microsoft 账户登录。
2. **导航到 Microsoft Entra ID**：在顶部搜索栏中搜索“Microsoft Entra ID”，或在“Azure 服务”下找到它。
3. **浏览仪表板**：查看您的租户概览，包括用户、组和应用程序。根据需要设置自定义域等基础内容。
4. **启用关键功能**：
   - **身份验证**：在“身份验证方法”下配置自助密码重置或多重身份验证（MFA）。
   - **条件访问**：在“安全”>“条件访问”下创建策略，以基于用户、设备或位置强制执行规则。

## 管理用户和组
- **添加用户**：转到“用户”>“新建用户”。输入详细信息，如姓名、用户名（例如 user@yourdomain.com），并分配角色或许可证。
- **创建组**：在“组”>“新建组”下，选择安全组或 Microsoft 365 类型，添加成员，并用于访问分配。
- **分配许可证**：在用户/组详细信息中，转到“许可证”以分配 Entra ID P1/P2，用于高级功能，如 Privileged Identity Management（PIM）。
- **最佳实践**：遵循最小权限原则——分配最小权限，并使用组进行批量管理。

## 管理应用程序
- **注册应用程序**：在“应用注册”>“新建注册”下，提供名称、重定向 URI 和支持的账户类型（单租户、多租户等）。
- **添加企业应用程序**：对于第三方应用程序，转到“企业应用程序”>“新建应用程序”以浏览库或创建非库应用程序。
- **配置访问**：在“用户和组”下将用户/组分配到应用程序，并通过 SAML 或 OAuth 设置单点登录（SSO）。
- **预配身份**：在“预配”下自动将用户同步到应用程序，以实现即时访问。

对于混合设置（本地 AD），使用 Microsoft Entra Connect 同步身份。通过“监控”>“登录日志”下的日志监控使用情况。

# 如何检查对数据库、Kubernetes（AKS）或其他资源的访问权限

Azure 中的访问通过基于角色的访问控制（RBAC）进行管理，并与 Entra ID 集成。用户使用 Entra 凭据进行身份验证，角色定义权限。要检查访问权限，请使用 Azure 门户的 IAM（身份和访问管理）工具。这将列出直接分配、从父范围（例如订阅）继承的分配以及拒绝分配。

## 任何 Azure 资源的通用步骤
1. **打开资源**：在 Azure 门户中，导航到资源（例如资源组、VM、存储账户）。
2. **转到访问控制（IAM）**：从左侧菜单中选择“访问控制（IAM）”。
3. **检查访问权限**：
   - 对于您自己的访问权限：单击“检查访问权限”>“查看我的访问权限”以查看此范围和继承的分配。
   - 对于特定用户/组/服务主体：
     - 单击“检查访问权限”>“检查访问权限”。
     - 选择“用户、组或服务主体”。
     - 按姓名或电子邮件搜索。
     - 查看结果窗格中的角色分配（例如所有者、参与者）和有效权限。
4. **查看符合条件的分配**（如果使用 PIM）：切换到“符合条件的分配”选项卡以获取即时角色。
5. **PowerShell/CLI 替代方案**：使用 `az role assignment list --assignee <user> --scope <resource-id>` 进行脚本化检查。

注意：这不包括子范围分配；如果需要，请向下钻取。

## 检查对 Azure SQL 数据库的访问权限
Azure SQL 使用 Entra 身份验证用于包含的数据库用户（绑定到 Entra 身份，而非 SQL 登录名）。
1. **配置 Entra 管理员（如果未设置）**：在 SQL 服务器概览>“设置”下的“Microsoft Entra ID”>“设置管理员”。搜索并选择用户/组，然后保存。这将在集群范围内启用 Entra 身份验证。
2. **检查服务器级访问权限**：
   - 在 SQL 服务器窗格>“Microsoft Entra ID”中，查看管理员字段以查看分配的身份。
   - 查询 `master` 数据库：`SELECT name, type_desc FROM sys.database_principals WHERE type IN ('E', 'X');`（E 表示外部用户，X 表示外部组）。
3. **检查数据库级访问权限**：
   - 使用 SSMS 通过 Entra 身份验证连接到数据库（在连接对话框中选择“Microsoft Entra - 通用与 MFA”）。
   - 运行 `SELECT * FROM sys.database_principals;` 或 `EXEC sp_helprolemember;` 以列出用户和角色。
4. **故障排除**：如果登录失败（例如错误 33134），请检查 Entra 条件访问策略是否允许 Microsoft Graph API 访问。

默认情况下用户获得 `CONNECT` 权限；通过 T-SQL 授予角色如 `db_datareader`：`ALTER ROLE db_datareader ADD MEMBER [user@domain.com];`。

## 检查对 AKS（Kubernetes 集群）的访问权限
AKS 集成 Entra ID 用于身份验证，并使用 Azure RBAC 或 Kubernetes RBAC 进行授权。
1. **Azure 级访问（对 AKS 资源）**：
   - 在 AKS 集群资源上遵循上述通用步骤。
   - 常见角色：“Azure Kubernetes 服务集群管理员”用于完整的 kubeconfig 访问；“读者”用于仅查看。
2. **Kubernetes API 访问**：
   - 通过 `az login` 进行身份验证（使用 Entra 令牌）。
   - 获取 kubeconfig：`az aks get-credentials --resource-group <rg> --name <cluster>`。
   - 检查绑定：`kubectl auth can-i <verb> <resource> --as <user@domain.com> -n <namespace>`。
   - 列出集群角色：`kubectl get clusterrolebindings | grep <user-or-group>`。
3. **使用 Entra 组**：将 Kubernetes 角色/绑定分配给组以实现可扩展性。命名空间角色的示例 YAML（使用 `kubectl apply -f file.yaml` 应用）：
   ```
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: example-binding
     namespace: default
   subjects:
   - kind: Group
     name: finance-group  # Entra 组
     apiGroup: rbac.authorization.k8s.io
   roleRef:
     kind: Role
     name: example-role
     apiGroup: rbac.authorization.k8s.io
   ```
4. **最佳实践**：使用最小权限角色，与 PIM 集成以实现即时提升，并避免使用固定凭据——对 Pod 使用工作负载身份。

对于访问资源的 Pod（例如从 AKS 访问 SQL），分配托管身份并通过这些身份上的 Azure RBAC 进行检查。

[Microsoft Entra ID 文档](https://learn.microsoft.com/en-us/entra/identity/)
[检查对单个 Azure 资源的访问权限](https://learn.microsoft.com/en-us/azure/role-based-access-control/check-access)
[为 Azure SQL 配置 Entra 身份验证](https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-configure?view=azuresql)
[AKS 身份和访问最佳实践](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-identity)
