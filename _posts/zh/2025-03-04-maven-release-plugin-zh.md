---
audio: false
generated: true
lang: zh
layout: post
title: Maven发布插件
translated: true
type: note
---

以下是关于如何使用 **Maven Release Plugin** 管理和自动化 Maven 项目发布流程的完整指南。

---

### 什么是 Maven Release Plugin？

**Maven Release Plugin** 是一个用于自动化 Maven 项目发布流程的工具。它负责处理以下任务：

- 更新项目 POM 文件中的版本号。
- 将更改提交到版本控制系统（VCS），例如 Git。
- 在 VCS 中为发布创建标签。
- 构建并部署发布产物。
- 通过再次更新版本号，为下一个开发周期准备项目。

该插件的两个主要目标是：

- **`release:prepare`**：通过更新版本、提交更改并在 VCS 中为发布打标签来准备项目发布。
- **`release:perform`**：使用 VCS 中的标签代码构建并部署发布版本。

---

### 使用 Maven Release Plugin 的逐步指南

#### 1. 将 Maven Release Plugin 添加到 POM 文件

要使用该插件，需要将其包含在项目的 `pom.xml` 中。在 `<build><plugins>` 部分添加如下内容：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-release-plugin</artifactId>
            <version>2.5.3</version> <!-- 使用最新的稳定版本 -->
        </plugin>
    </plugins>
</build>
```

**注意**：请查看 [官方 Maven Release Plugin 页面](https://maven.apache.org/maven-release/maven-release-plugin/) 获取最新版本，并替换 `2.5.3`。

#### 2. 配置 SCM（源代码管理）部分

该插件与您的 VCS（例如 Git）交互以提交更改和创建标签。您必须在 `pom.xml` 的 `<scm>` 部分指定 VCS 详细信息。对于托管在 GitHub 上的 Git 仓库，配置可能如下所示：

```xml
<scm>
    <connection>scm:git:git://github.com/username/project.git</connection>
    <developerConnection>scm:git:git@github.com:username/project.git</developerConnection>
    <url>https://github.com/username/project</url>
</scm>
```

- 将 `username` 和 `project` 替换为实际的 GitHub 用户名和仓库名称。
- 如果使用其他 Git 托管服务（例如 GitLab、Bitbucket），请调整 URL。
- 确保已配置必要的凭据（例如 SSH 密钥或个人访问令牌）以推送更改到仓库。

#### 3. 准备项目发布

在运行发布命令之前，请确保项目已准备就绪：

- 所有测试通过（`mvn test`）。
- 工作目录中没有未提交的更改（运行 `git status` 检查）。
- 您处于正确的分支（例如 `master` 或 `main`）以进行发布。

#### 4. 运行 `release:prepare`

`release:prepare` 目标用于准备项目发布。在终端中执行以下命令：

```bash
mvn release:prepare
```

**`release:prepare` 期间会发生什么**：

- **检查未提交的更改**：确保工作目录干净。
- **提示输入版本**：询问发布版本和下一个开发版本。
  - 示例：如果当前版本是 `1.0-SNAPSHOT`，它可能建议发布版本为 `1.0`，下一个开发版本为 `1.1-SNAPSHOT`。您可以接受默认值或输入自定义版本（例如，补丁发布使用 `1.0.1`）。
- **更新 POM 文件**：将版本更改为发布版本（例如 `1.0`），提交更改，并在 VCS 中为其打标签（例如 `project-1.0`）。
- **为下一个周期准备**：将 POM 更新为下一个开发版本（例如 `1.1-SNAPSHOT`）并提交。

**可选干运行**：要在不进行实际更改的情况下测试流程，请使用：

```bash
mvn release:prepare -DdryRun=true
```

这将模拟准备步骤，但不会提交或打标签。

#### 5. 运行 `release:perform`

准备发布后，使用以下命令构建并部署：

```bash
mvn release:perform
```

**`release:perform` 期间会发生什么**：

- 从 VCS 检出标签版本。
- 构建项目。
- 将产物部署到 POM 的 `<distributionManagement>` 部分指定的仓库。

**配置 `<distributionManagement>`**（如果部署到远程仓库）：

```xml
<distributionManagement>
    <repository>
        <id>releases</id>
        <url>http://my-repository-manager/releases</url>
    </repository>
    <snapshotRepository>
        <id>snapshots</id>
        <url>http://my-repository-manager/snapshots</url>
    </snapshotRepository>
</distributionManagement>
```

- 将 URL 替换为您的仓库管理器地址（例如 Nexus、Artifactory）。
- 确保在 `~/.m2/settings.xml` 文件的 `<servers>` 部分设置了匹配 `id` 的凭据。

#### 6. 验证发布

在 `release:perform` 之后，验证发布：

- 检查您的仓库管理器，确保产物（例如 JAR 文件、源代码）已部署。
- 在另一个项目中通过在其 POM 中添加依赖项来测试发布版本。

---

### 额外配置和提示

#### 处理失败

- **清理**：如果发布过程失败，请使用：

  ```bash
  mvn release:clean
  ```

  以删除插件创建的临时文件。
- **回滚**：要撤销 `release:prepare` 所做的更改：

  ```bash
  mvn release:rollback
  ```

  请谨慎操作，并验证哪些更改被恢复。

#### 多模块项目

对于多模块项目，插件默认会一致地更新所有模块的版本。确保父 POM 包含插件和 SCM 配置。

#### 用于自动化的批处理模式

要以非交互方式运行发布（例如在 CI/CD 流水线中），请使用 `-B` 标志并指定版本：

```bash
mvn release:prepare -B -DreleaseVersion=1.0 -DdevelopmentVersion=1.1-SNAPSHOT
mvn release:perform -B
```

#### 常见问题及解决方案

- **VCS 错误**：确保 Git 命令（例如 `git commit`、`git push`）可以手动运行。检查身份验证（SSH 密钥、令牌）。
- **构建失败**：验证本地构建是否成功（`mvn clean install`）以及依赖项是否正确解析。
- **版本策略**：如果默认值不符合需求，可以在提示期间或通过属性自定义版本。

---

### 命令摘要

1. **准备发布**：

   ```bash
   mvn release:prepare
   ```

2. **执行发布**：

   ```bash
   mvn release:perform
   ```

3. **可选干运行**：

   ```bash
   mvn release:prepare -DdryRun=true
   ```

4. **如有需要，清理或回滚**：

   ```bash
   mvn release:clean
   mvn release:rollback
   ```

---

### 结论

Maven Release Plugin 通过自动化版本管理、VCS 交互和部署，简化了发布流程。通过将插件添加到 POM、配置 SCM 并遵循 `release:prepare` 和 `release:perform` 步骤，您可以高效地发布 Maven 项目。始终通过干运行测试配置并验证结果，以确保发布流程顺利进行。
