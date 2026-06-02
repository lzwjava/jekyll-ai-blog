---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 自由保险库集成选项
translated: true
type: note
---

**问题：** 如何将 HashiCorp Vault 与 WebSphere Liberty Profile 集成？WLP 是否有 vault-1.0 功能？在 JDBC 配置中，我可以使用类似 `${vault:namespace#db_password}` 的语法吗？

**回答：**

不，**WebSphere Liberty Profile (WLP)** 没有内置的 `vault-1.0` 功能，也没有原生的 `${vault:...}` 变量替换语法，用于在配置时直接从 HashiCorp Vault 获取机密（类似于其他一些平台提供的功能）。

Liberty（以及 Open Liberty）支持在 `server.xml` 中的变量替换（例如 `${db_password}`），但值必须来自：

- `bootstrap.properties`
- `server.env`
- 环境变量
- JVM 系统属性
- 特定目录中的文件（在新版本中，尤其是在容器中运行时）

Liberty 中**没有直接的 Vault 解析器**，如 `${vault:secret/path#key}`。

### HashiCorp Vault 的常见实际集成方法

1. **Vault Agent (Sidecar) + 基于文件的变量（推荐用于容器/Kubernetes）**
   使用 Vault Agent 将机密渲染为文件。然后 Liberty 可以将它们作为来自文件系统的配置变量读取。

   - 以 sidecar 模式运行 Vault Agent（或作为 init container）进行身份验证（例如通过 Kubernetes auth、AppRole 等），并将机密写入文件，如：
     ```
     /config/variables/db_password
     /config/variables/db_username
     ```
   - Liberty 会自动将 `/config/variables/`（或类似配置路径）下的文件视为变量。
   - 在 `server.xml` 中：
     ```xml
     <dataSource id="DefaultDataSource" jndiName="jdbc/myapp">
         <jdbcDriver libraryRef="DerbyLib"/>
         <properties.derby.embedded databaseName="memory:db" user="${db_username}" password="${db_password}"/>
     </dataSource>
     ```
   - 这在 Open Liberty 中得到明确支持/文档化（在 WebSphere Liberty 中同样有效），前提是使用 Vault Agent 来填充文件。

2. **Vault Agent 模板 → 环境变量**
   Vault Agent 可以使用其 supervisor 模式或类似 `envconsul` 的行为，将机密模板化为环境变量。

   - 然后在 Liberty 中通过 `${env.VAULT_DB_PASSWORD}`（如果使用环境变量替换）或在 `bootstrap.properties` 中映射它们来引用。

3. **AppRole + 应用程序中的自定义代码**
   - 对于应用程序级机密（非 server.xml 配置），您的 Java 代码可以使用 AppRole 向 Vault 进行身份验证，并在运行时获取机密（例如用于 JDBC 连接池回调或自定义配置）。
   - 这无法帮助 Liberty 的内置 `<dataSource>` 密码字段。

4. **External Secrets Operator（仅限 Kubernetes）**
   如果在 Kubernetes 上运行，使用 External Secrets Operator 将 Vault 机密同步到 Kubernetes Secrets → 环境变量或挂载文件 → Liberty 变量。

5. **bootstrap.properties + 外部脚本/Init**
   - 在容器启动时，运行一个脚本，使用 AppRole 或 token 向 Vault 进行身份验证，并将值写入 `bootstrap.properties` 或 `server.env`。
   - Liberty 在启动时读取这些文件。

### 选项总结表

| 方法                            | 在 server.xml 中有效？ | 原生 Vault 语法？ | 最适合                | 复杂度   |
|---------------------------------|----------------------|----------------------|-----------------------|----------|
| Vault Agent → files             | 是                   | 否                   | Containers / K8s      | 中等     |
| Vault Agent → env vars          | 是（通过 ${env.}）   | 否                   | Containers            | 中等     |
| 应用程序代码获取机密            | 否（配置级别）       | 否                   | App runtime secrets   | 低-中等  |
| 自定义用户功能                  | 可能                 | 否                   | 非常自定义需求        | 高       |
| 直接 ${vault:...}               | 否                   | 否                   | —                     | —        |

使用 Vault Agent 的基于文件的方法是 Liberty/Open Liberty 环境中最为常见且官方提及的模式。

**参考资料：**

- [Open Liberty 关于 Kubernetes secrets + Vault Agent 示例的博客](https://openliberty.io/blog/2021/10/29/kube-secrets-210011.html)
- [HashiCorp Discuss 关于 WebSphere + Vault 的线程](https://discuss.hashicorp.com/t/websphere-integration-with-vault/55528)
- [Liberty 变量替换文档](https://www.ibm.com/docs/en/was-liberty/base?topic=overview-liberty-variables)
