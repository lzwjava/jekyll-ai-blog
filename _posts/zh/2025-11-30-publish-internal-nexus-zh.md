---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 发布至内部Nexus仓库
translated: true
type: note
---

以下是向**内部 Nexus 仓库管理器**（当前版本为 Sonatype Nexus 3）发布软件包最常用且可靠的方法，具体取决于软件包格式。

### 1. 使用 Maven（JVM 语言最常用）

#### 方案 A：maven-deploy-plugin（命令行）

```bash
mvn deploy -DaltDeploymentRepository=internal-nexus::default::https://your-nexus.company.com/repository/maven-releases/
```

或用于快照版本：

```bash
mvn deploy -DaltDeploymentRepository=internal-nexus::default::https://your-nexus.company.com/repository/maven-snapshots/
```

#### 方案 B：在 pom.xml 中配置（推荐用于项目）

```xml
<distributionManagement>
    <repository>
        <id>internal-nexus</id>
        <name>Internal Releases</name>
        <url>https://your-nexus.company.com/repository/maven-releases/</url>
    </repository>
    <snapshotRepository>
        <id>internal-nexus</id>
        <name>Internal Snapshots</name>
        <url>https://your-nexus.company.com/repository/maven-snapshots/</url>
    </snapshotRepository>
</distributionManagement>
```

然后只需运行：

```bash
mvn deploy
```

确保在 `~/.m2/settings.xml` 中配置凭据：

```xml
<servers>
  <server>
    <id>internal-nexus</id>
    <username>your-username</username>
    <password>your-password-or-token</password>
  </server>
</servers>
```

### 2. 使用 Gradle

在 `build.gradle`（Groovy）或 `build.gradle.kts`（Kotlin）中：

```groovy
publishing {
    repositories {
        maven {
            name = "InternalNexus"
            url = version.endsWith('SNAPSHOT')
                ? "https://your-nexus.company.com/repository/maven-snapshots/"
                : "https://your-nexus.company.com/repository/maven-releases/"
            credentials {
                username = "your-username"
                password = "your-password-or-token"
            }
        }
    }
}
```

然后运行：

```bash
gradle publish
```

### 3. npm 软件包

```bash
# 一次性设置注册中心
npm config set registry https://your-nexus.company.com/repository/npm-internal/

# 登录（使用 Nexus 凭据或令牌）
npm login

# 发布
npm publish
```

### 4. PyPI（Python）软件包

```bash
# 创建或更新 ~/.pypirc
[distutils]
index-servers = internal-nexus

[internal-nexus]
repository = https://your-nexus.orgcompany.com/repository/pypi-internal/
username = your-username
password = your-password-or-token

# 然后构建并上传
python -m build
twine upload --repository internal-nexus dist/*
```

### 5. NuGet（.NET）

```bash
nuget sources add -Name "InternalNexus" -Source https://your-nexus.company.com/repository/nuget-hosted/ -UserName your-user -Password your-token
nuget push YourPackage.1.0.0.nupkg -Source InternalNexus
```

### 6. Raw / 通用仓库（任意文件）

使用 curl 通过 Nexus REST API 上传：

```bash
curl -v -u username:password \
     -H "Content-Type: application/octet-stream" \
     --data-binary @your-artifact-1.0.0.zip \
     "https://your-nexus.company.com/repository/raw-hosted/path/to/your-artifact-1.0.0.zip"
```

用于带目录结构的原始托管仓库：

```bash
curl -v -u user:pass \
     --upload-file myfile.tar.gz \
     "https://your-nexus.company.com/repository/raw-hosted/some/folder/myfile.tar.gz"
```

### 7. Docker 镜像

```bash
docker login your-nexus.company.com
docker tag myimage:latest your-nexus.company.com/myimage:latest
docker push your-nexus.company.com/myimage:latest
```

### 推荐方案

- 对于 Maven/Gradle/Java 项目 → 配置 `distributionManagement` / `publishing` 代码块（最清晰的 CI/CD 集成）
- 对于其他所有情况 → 使用指向内部 Nexus 的原生工具（npm、twine、nuget、docker 等）
- 仅当不存在原生工具时，才回退使用原始 curl API

大多数公司还会使用 CI/CD 流水线（Jenkins、GitLab CI、GitHub Actions 等），在将凭据配置为密钥后直接运行 `mvn deploy` 或 `gradle publish`。

请告知您正在使用的软件包类型（Maven、npm、PyPI、Docker 等），我可以为您提供适用于您场景的精确可用命令/配置！
