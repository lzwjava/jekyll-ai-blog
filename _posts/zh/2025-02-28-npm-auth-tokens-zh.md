---
audio: false
generated: true
lang: zh
layout: post
title: 在npm注册表URL中使用身份验证令牌
translated: true
type: note
---

### 核心要点
- 要在 npm 注册表 URL 中使用认证令牌，通常需要在 `.npmrc` 文件中进行配置，将令牌与注册表 URL 关联。
- 研究表明标准做法是在 `.npmrc` 文件中添加 `//registry.url.com/:_authToken=your_token`，其中 `registry.url.com` 是注册表 URL，`your_token` 是认证令牌。
- 证据表明应使用 `.npmrc` 文件进行认证，因为将令牌直接包含在 URL 中（如在 HTTP 请求中）不是 npm 的标准做法，且可能无效。

### 直接回答

#### 概述
要在 npm 注册表 URL 中使用认证令牌，通常需要在一个名为 `.npmrc` 的特殊文件中进行配置。该文件告知 npm 命令行工具在访问特定包注册表（如公共 npm 注册表或私有注册表）时如何进行认证。以下是面向初学者的分步配置指南。

#### 配置步骤
1. **确定注册表 URL**：决定要使用的注册表，例如公共 npm 注册表的 `registry.npmjs.org` 或私有注册表的 `privateregistry.com`。
2. **获取认证令牌**：从注册表提供商处获取认证令牌，可能是个人访问令牌或组织提供的其他类型令牌。
3. **编辑 `.npmrc` 文件**：打开或创建 `.npmrc` 文件。该文件可位于项目文件夹中（用于项目特定设置）或主目录中（如 Unix 系统上的 `~/.npmrc`，用于用户全局设置）。
   - 添加如下行：`//registry.url.com/:_authToken=your_token`。将 `registry.url.com` 替换为您的注册表 URL，`your_token` 替换为实际令牌。
   - 例如，对于公共 npm 注册表，可能如下所示：`//registry.npmjs.org/:_authToken=abc123`。
4. **保护文件安全**：确保 `.npmrc` 文件仅对您自己可读可写，以保护令牌安全。在 Unix 系统上，可使用 `chmod 600 ~/.npmrc` 设置权限。
5. **验证配置**：尝试运行 npm 命令（如 `npm install`），检查是否能正常访问注册表。

#### 意外细节
您可能认为可以将认证令牌直接放入 URL（如 `https://registry.url.com?token=your_token`），但这并非 npm 的标准做法。相反，npm 使用 `.npmrc` 文件在后台处理认证，这更安全且易于管理。

更多详情，请查阅官方 npm 文档中关于配置 `.npmrc` 文件的部分[此处](https://docs.npmjs.com/configuring-npm/npmrc)。

---

### 调研说明：npm 注册表 URL 认证令牌使用详解

本节全面分析如何在 npm 注册表 URL 中使用认证令牌，在直接回答的基础上扩展了更多背景信息、技术细节和示例，旨在覆盖研究中的所有方面，确保不同专业水平的用户都能透彻理解。

#### npm 与认证简介
Node Package Manager (npm) 是 JavaScript 开发者的关键工具，用于管理包和依赖项。它与包注册表（如公共注册表 [registry.npmjs.org](https://registry.npmjs.org) 或组织托管的私有注册表）交互。对于私有注册表或发布包等特定操作，通常需要认证，这通过存储在配置文件中的认证令牌处理。

`.npmrc` 文件是 npm 配置的核心，允许自定义注册表 URL、认证方法等设置。它可存在于多个位置，如每个项目（项目根目录中）、每个用户（主目录中，例如 Unix 上的 `~/.npmrc`）或全局（例如 `/etc/npmrc`）。该文件使用 INI 格式，其中键和值定义了 npm 的行为方式，包括如何与注册表进行认证。

#### 在 `.npmrc` 中配置认证令牌
要为特定注册表 URL 使用认证令牌，需配置 `.npmrc` 文件以将令牌与该注册表关联。标准格式为：

```
registry.url.com/:_authToken=your_token
```

此处，`registry.url.com` 是注册表的基础 URL（例如公共注册表的 `registry.npmjs.org` 或私有注册表的 `privateregistry.com`），`your_token` 是注册表提供的认证令牌。`:_authToken` 键表示这是基于令牌的认证，npm 在向注册表发出 HTTP 请求时使用它来设置 `Authorization` 头部为 `Bearer your_token`。

例如，如果您有公共 npm 注册表的令牌 `abc123`，则 `.npmrc` 条目为：

```
registry.npmjs.org/:_authToken=abc123
```

此配置确保任何与 `registry.npmjs.org` 交互的 npm 命令都将包含该令牌进行认证，根据令牌的范围允许访问私有包或发布功能。

#### 处理作用域包
对于作用域包（以 `@` 开头的包，如 `@mycompany/mypackage`），您可以为该作用域指定不同的注册表。首先，设置作用域的注册表：

```
@mycompany:registry=https://mycompany.artifactory.com/
```

然后，将认证令牌与该注册表关联：

```
mycompany.artifactory.com/:_authToken=your_token
```

此设置将所有对 `@mycompany` 包的请求路由到指定的私有注册表，并使用提供的令牌进行认证。这在企业环境中尤其有用，组织通常为自己的内部包托管私有 npm 注册表。

#### `.npmrc` 的位置与安全性
`.npmrc` 文件可位于多个位置，各有不同用途：
- **每个项目**：位于项目根目录（例如与 `package.json` 同目录）。适用于项目特定配置，并覆盖全局设置。
- **每个用户**：位于用户主目录中（例如 Unix 上的 `~/.npmrc`，Windows 上的 `C:\Users\<Username>\.npmrc`）。影响该用户的所有 npm 操作。
- **全局**：位于 `/etc/npmrc` 或由 `globalconfig` 参数指定，通常用于系统范围设置。

鉴于 `.npmrc` 可能包含认证令牌等敏感信息，安全性至关重要。文件必须仅对用户可读可写以防止未经授权的访问。在 Unix 系统上，可使用命令 `chmod 600 ~/.npmrc` 确保此点，将权限设置为仅所有者可读/写。

#### 替代认证方法
虽然基于令牌的认证很常见，但 npm 也支持基本认证，您可以在 `.npmrc` 文件中包含用户名和密码：

```
registry.url.com/:username=your_username
registry.url.com/:_password=your_password
```

然而，出于安全原因，更推荐基于令牌的认证，因为令牌可被撤销且具有范围权限，与存储明文密码相比风险更低。

#### 直接包含在 URL 中：是否可行？
问题中提到“在 npm 注册表 url 中使用 auth 或 authtoken”，这可能暗示将令牌直接包含在 URL 中，如 `https://registry.url.com?token=your_token`。然而，研究表明这不是 npm 的标准做法。npm 注册表 API 文档及相关资源（如 [NPM registry authentication | Rush](https://rushjs.io/pages/maintainer/npm_registry_auth/)）强调使用 `.npmrc` 文件进行认证，令牌在 `Authorization` 头部中以 `Bearer your_token` 形式传递。

尝试将令牌作为查询参数包含在 URL 中不受标准 npm 注册表支持，且可能无效，因为认证是在 HTTP 头部级别处理的。某些私有注册表可能支持自定义的基于 URL 的认证，但这在官方 npm 注册表中未有文档记录。例如，基本认证允许类似 `https://username:password@registry.url.com` 的 URL，但这种方法已过时且不如基于令牌的方法安全。

#### 实际示例与用例
考虑以下场景：

- **带令牌的公共注册表**：如果您需要发布到公共 npm 注册表并拥有令牌，请添加：
  ```
  registry.npmjs.org/:_authToken=abc123
  ```
  然后运行 `npm publish` 上传您的包，npm 将使用该令牌进行认证。

- **作用域包的私有注册表**：对于公司使用私有注册表 `https://company.registry.com` 处理 `@company` 包的情况，配置：
  ```
  @company:registry=https://company.registry.com/
  company.registry.com/:_authToken=def456
  ```
  现在，安装 `@company/mypackage` 将使用令牌通过私有注册表进行认证。

- **CI/CD 集成**：在持续集成环境中，将令牌存储为环境变量（例如 `NPM_TOKEN`）并在 `.npmrc` 文件中动态使用：
  ```
  registry.npmjs.org/:_authToken=${NPM_TOKEN}
  ```
  此方法在 [Using private packages in a CI/CD workflow | npm Docs](https://docs.npmjs.com/using-private-packages-in-a-ci-cd-workflow/) 中有详细说明，确保令牌不被硬编码且安全。

#### 故障排除与最佳实践
如果认证失败，请验证：
- 注册表 URL 正确且可访问。
- 令牌有效且具有必要权限（例如读取用于安装，写入用于发布）。
- `.npmrc` 文件位于正确位置且具有适当权限。

最佳实践包括：
- 切勿将含令牌的 `.npmrc` 提交到版本控制；将其添加到 `.gitignore`。
- 在 CI/CD 管道中使用环境变量存储令牌以增强安全性。
- 定期轮换令牌并撤销未使用的令牌以最小化风险。

#### 认证方法比较分析
为提供结构化概览，以下是 npm 中基于令牌的认证与基本认证的比较表：

| **方法**          | **在 `.npmrc` 中的配置**                          | **安全性**                     | **用例**                     |
|---------------------|-------------------------------------------------------|-----------------------------------|-----------------------------------|
| 基于令牌（推荐） | `registry.url.com/:_authToken=your_token`            | 高（可撤销，有范围）         | 私有注册表，CI/CD        |
| 基本认证| `registry.url.com/:username=your_username`<br>`registry.url.com/:_password=your_password` | 低（明文密码）         | 遗留系统，公共注册表  |

此表突显了为何推荐基于令牌的认证，尤其对于现代工作流程。

#### 结论
在 npm 注册表 URL 中使用认证令牌主要涉及配置 `.npmrc` 文件以将令牌与注册表关联。此方法标准、安全且广泛支持，确保 npm 能在不暴露 URL 中令牌的情况下认证请求。虽然将令牌直接包含在 URL 中不是 npm 的标准做法且可能无效，但 `.npmrc` 方法为公共和私有注册表交互提供了稳健的解决方案。

进一步阅读，请查阅官方 npm 文档关于 [configuring npmrc](https://docs.npmjs.com/configuring-npm/npmrc) 和 [registry authentication](https://docs.npmjs.com/using-private-packages-in-a-ci-cd-workflow/) 的部分。

### 关键引用
- [NPM registry authentication Rush documentation](https://rushjs.io/pages/maintainer/npm_registry_auth/)
- [registry-auth-token npm package details](https://www.npmjs.com/package/registry-auth-token)
- [Globally configure NPM with token Stack Overflow question](https://stackoverflow.com/questions/38764714/globally-configure-npm-with-a-token-registry-to-a-specific-scope-organisation)
- [Configure authentication Artifact Registry Google Cloud](https://cloud.google.com/artifact-registry/docs/nodejs/authentication)
- [Official npm documentation for npmrc file](https://docs.npmjs.com/configuring-npm/npmrc)
- [Using private packages in CI/CD workflow npm Docs](https://docs.npmjs.com/using-private-packages-in-a-ci-cd-workflow/)
