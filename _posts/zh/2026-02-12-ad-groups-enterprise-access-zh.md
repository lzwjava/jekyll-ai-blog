---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 企业访问控制的 AD 组
translated: true
type: note
---

Question: 请解释 Windows 中的 AD groups，以及如何使用它们在企业环境中控制员工访问权限？

Answer: 

Windows 中的 **Active Directory (AD) groups** 是 Active Directory 中的对象，用于组织用户账户（user accounts）、计算机账户（computer accounts）和其他组。它们简化了企业环境中的 **access control**（访问控制）和权限管理。

### Active Directory 中的主要组类型

- **Security Groups** — 用于为资源（如文件共享、文件夹、打印机、应用程序、数据库、Azure 资源等）分配 **permissions**（权限，如 read、write、modify、full control 等）。
  它们还可以被分配 **user rights**（用户权利，如本地登录、remote desktop 登录等）。

- **Distribution Groups** — 仅用于电子邮件分发列表（例如在 Exchange 或 Microsoft 365 中）。它们 **不能** 用于分配权限。

在控制员工访问权限时，只有 **security groups** 是相关的。

### Group Scopes（在企业环境中非常重要）

| Scope          | 可以包含的成员来自                  | 可以被分配权限的范围                | 典型用途                                |
|----------------|------------------------------------|-------------------------------------|----------------------------------------|
| **Domain Local**   | 林 (forest) 中的任何域 + 信任域      | 仅限于其所属的域                    | 资源权限（文件夹、共享、打印机、应用） |
| **Global**         | 仅限同一个域                       | 林中的任何位置                      | 按 **role** 或部门对用户进行分组（如 "Marketing Users"） |
| **Universal**      | 同一个林中的任何域                 | 林中的任何位置                      | 跨域角色或非常广泛的组（需谨慎使用）    |

**Builtin Local** 组（如 Administrators、Backup Operators）存在于 Builtin 容器中，其行为类似于 Domain Local 组。

### 企业访问控制模型最佳实践 (RBAC)

Microsoft 强烈建议使用 **group nesting**（组嵌套）来实现 **role-based access control (RBAC)**。两种标准模式是：

1. **AGDLP** — 用于 **single-domain** 环境（最常用）  
   **A**ccounts → **G**lobal groups → **D**omain **L**ocal groups → **P**ermissions

2. **AGUDLP** — 用于 **multi-domain** 森林 (forests)  
   **A**ccounts → **G**lobal groups → **U**niversal groups → **D**omain **L**ocal groups → **P**ermissions

#### 实际案例（单域 – AGDLP）

- 为 **roles** / 部门创建 **Global** 组：
  - FIN-Finance-Users (global)
  - HR-Employees (global)
  - Sales-Team-EMEA (global)

- 为 **resources** 创建 **Domain Local** 组：
  - FIN-Share-Modify (domain local)
  - HR-Payroll-FullControl (domain local)
  - Sales-Reports-Read (domain local)

- 进行嵌套：
  - 将用户 John 放入 FIN-Finance-Users (global)
  - 将 FIN-Finance-Users 设置为 FIN-Share-Modify (domain local) 的成员
  - 在 \\server\Finance 文件夹上授予 FIN-Share-Modify 组 **Modify** 权限

结果：当 John 调离部门时，你只需更改他的 global group 成员身份，所有权限都会自动更新。

### 使用 AD Groups 的企业最佳实践

- 遵循 **least privilege**（最小特权）原则 —— 绝不给予超出需要的访问权限
- 使用 **consistent naming convention**（统一命名规范，在大公司中非常重要）：
  - 角色组：`GRP-GLB-Finance-Users`, `GRP-GLB-HR-Staff`
  - 资源组：`GRP-DL-Files-Finance-Modify`, `GRP-DL-App-SAP-Execute`
  - 前缀很有帮助：`SEC-`, `GRP-`, `DL-`, `GL-`, `UNI-`

- 避免将用户 **直接** 添加到资源权限中 —— 始终使用组
- 尽量减少强大内置组的成员数量：
  - Domain Admins, Enterprise Admins, Schema Admins, Administrators
  - 尽可能使用 **delegated groups**（委派组）代替

- 定期审查和清理组：
  - 删除未使用或空的组
  - 审计特权组的成员身份
  - 使用 **Active Directory Users and Computers**、**PowerShell** (`Get-ADGroupMember`) 或第三方解决方案（Netwrix, ManageEngine, Semperis 等）

- 启用 **group nesting**，但避免过多层级（通常 3–4 层已足够）

- 对于 **hybrid / cloud**（混合/云）环境 (Entra ID / Azure AD)：
  - 使用 **cloud-only groups** 或 **synced security groups**
  - 为管理员访问考虑使用 **Microsoft Entra ID roles** 和 **PIM** (Privileged Identity Management)

使用这种结构化方法（特别是 AGDLP/AGUDLP）可以显著减少管理工作量，提高安全性，简化审计，并且即使在拥有数万名用户的超大型企业中也能保持良好的扩展性。

References:  

- [Active Directory Security Groups | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups)
- [5 Best practices for AD security groups - ManageEngine](https://www.manageengine.com/products/active-directory-audit/kb/best-practices/active-directory-security-groups-best-practices.html)
- [Active Directory Group Management Best Practices - Netwrix](https://netwrix.com/en/resources/guides/active-directory-group-management-best-practices)
- [AGDLP - Wikipedia](https://en.wikipedia.org/wiki/AGDLP)