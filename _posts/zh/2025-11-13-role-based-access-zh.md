---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Jenkins中的基于角色的访问控制
translated: true
type: note
---

### 企业级 Jenkins（CloudBees CI）中的基于角色的访问控制（RBAC）

企业级 Jenkins（由 CloudBees CI 提供支持）使用 CloudBees 基于角色的访问控制（RBAC）插件来实现细粒度的、基于角色的权限管理。这允许管理员定义自定义角色，将其分配给用户或组，并在全局、文件夹或作业级别控制访问。它与 Folders 插件集成以实现基于团队的隔离，并支持外部身份提供商（如 LDAP 或 Active Directory）进行组管理。权限从分配给用户组的所有角色中聚合而来，并且除非被固定或过滤，否则可以传播到子对象（例如，子文件夹）。

RBAC 取代或增强了 Jenkins 内置的基于矩阵的授权，使得可以在不拥有完整系统访问权限的情况下委派管理任务。它在 **Manage Jenkins > Manage Security > Authorization** 下配置，在此处选择“基于角色的矩阵授权策略”。

#### 关键权限和访问权限
权限定义了用户可以在 Jenkins 对象（例如，作业、文件夹、代理、视图）上执行的原子操作。企业级 Jenkins 包含核心 Jenkins 权限以及插件扩展的权限。权限是分层的——某些权限隐含其他权限（例如，`Job/Configure` 隐含 `Job/Read`）。

以下是常见权限类别和示例的表格，重点提及构建/读取权限：

| 类别          | 权限示例                                                                                 | 描述 |
|-------------------|-----------------------------------------------------------------------------------------|-------------|
| **读取/只读** | - `Overall/Read`<br>- `Job/Read`<br>- `View/Read`<br>- `Agent/Read`                     | 授予查看配置、构建、日志和产物的权限，无需修改。适用于审计员或查看者。Extended Read Permission 插件增加了细粒度的读取控制（例如，无需构建权限即可查看工作空间）。 |
| **构建/执行** | - `Job/Build`<br>- `Job/Cancel`<br>- `Job/Workspace`<br>- `Job/Read`                    | 允许启动、停止构建或访问构建输出。可以限定到特定的作业/文件夹。 |
| **配置/修改** | - `Job/Configure`<br>- `Job/Create`<br>- `Job/Delete`<br>- `Folder/Configure`            | 允许编辑作业参数、添加触发器或管理子项。 |
| **管理** | - `Overall/Administer`<br>- `Overall/Configure`<br>- `Group/Manage`<br>- `Role/View`     | 完全系统控制或委派的任务，如管理角色/组。`Overall/Administer` 是超级用户权限。 |
| **其他**         | - `SCM/Tag`<br>- `Credentials/View`<br>- `Agent/Launch`<br>- `RunScripts`                | SCM 操作、凭据访问、节点管理或脚本执行。否定权限（例如，`-Job/Build`）可以限制继承的权限。 |

访问权限在多个作用域受控：
- **全局**：适用于整个实例（例如，通过根级组）。
- **对象特定**：在作业、文件夹或代理上覆盖（例如，团队只能在其文件夹中构建）。
- **传播**：角色自动继承到子对象，除非被“固定”（本地覆盖）或过滤（例如，对某个角色隐藏项目）。
- **隐含权限**：某些权限自动授予下级权限（在近期版本中可配置以增强安全性）。

管理员可以过滤角色以防止传播（例如，通过作业上的 **Roles > Filter**）或使用不可过滤的角色来强制执行全局访问。

#### 管理用户角色
角色是预定义的权限集合：
1. 转到 **Manage Jenkins > Manage Roles**。
2. 点击 **Add Role** 并为其命名（例如，“Developer”）。
3. 通过勾选复选框分配权限（使用“Check all”或“Clear all”进行批量操作）。系统角色如“anonymous”（用于未认证用户）和“authenticated”（已登录用户）是预构建的且无法删除。
4. 保存。角色可以标记为“non-filterable”以始终全局应用。

用户从其组分配的角色继承权限——没有直接的用户-角色分配；这是基于组的，以实现可扩展性。

#### 将角色分配给组和用户
组将用户和角色捆绑在一起，便于委派：
1. 在对象（例如，根目录、文件夹或作业）上，转到 **Groups > New Group**。
2. 输入组名（例如，“DevTeam”）。
3. 通过勾选角色来分配它们（默认传播到子对象；取消勾选以在本地固定）。
4. 添加成员（见下文）。
5. 保存。

组支持嵌套（例如，子组）和外部集成（例如，LDAP 组）。

#### 管理员如何将用户添加到组
拥有 `Group/Manage` 权限的管理员可以编辑成员资格：
1. 导航到组的配置（例如，根目录或对象上的 **Groups**）。
2. 在“Members”部分，点击 **Add user**（或 **Add group** 用于外部/嵌套组）。
3. 输入用户 ID（例如，来自 Jenkins 用户数据库的用户名、LDAP DN 或外部组名）。使用 `/whoAmI` 验证 ID。
4. 点击 **Add** 并保存。如果需要，通过提示确认移除。
5. 对于批量/自动化操作：
   - 使用 CLI：`java -jar jenkins-cli.jar group-membership <object-path> <group-name> <user-id>`（列出/设置成员）。
   - REST API：POST 到 `/rbac/api/v1/groups/<group>/members`，附带 JSON 负载。

避免循环组成员资格以防止循环。对于外部领域（例如，Active Directory），首先在 **Manage Security > Security Realm** 下配置安全领域。

此设置确保了安全、可扩展的控制——例如，开发人员在其文件夹中拥有 `Job/Build` + `Job/Read` 权限，而管理员处理所有事务。

[使用基于角色的访问控制限制访问并委派管理任务](https://docs.cloudbees.com/docs/cloudbees-ci/latest/secure/rbac)
