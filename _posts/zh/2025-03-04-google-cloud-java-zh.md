---
audio: false
generated: true
lang: zh
layout: post
title: 谷歌云Java客户端
translated: true
type: note
---

### 核心要点
- 要在 Java 中使用 `com.google.cloud`，需要搭建 Java 开发环境、引入 Google Cloud 客户端库依赖、配置身份验证，并使用这些库与 Google Cloud 服务进行交互。
- 研究表明，在 Google Cloud 平台上可自动处理身份验证，本地开发则需使用服务账号凭证手动配置。
- 推荐使用 Maven 或 Gradle 管理依赖，并以 Cloud Storage 为例提供了常见使用场景的示例。

### 搭建开发环境
首先确保安装 Java 开发工具包（JDK）8 或更高版本，以及 Maven 或 Gradle 等构建工具。这些工具可帮助管理项目依赖和构建流程。

### 引入依赖
将 Google Cloud 客户端库依赖添加到项目中。若使用 Maven，请在 `pom.xml` 文件中添加物料清单（BOM）和特定服务库。例如使用 Cloud Storage 时：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.google.cloud</groupId>
            <artifactId>libraries-bom</artifactId>
            <version>latest_version</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<dependencies>
    <dependency>
        <groupId>com.google.cloud</groupId>
        <artifactId>google-cloud-storage</artifactId>
    </dependency>
</dependencies>
```

请将 "latest_version" 替换为 [Google Cloud Java 客户端库 GitHub 仓库](https://github.com/googleapis/google-cloud-java) 中的实际版本号。

### 配置身份验证
若应用运行在 Compute Engine 或 App Engine 等 Google Cloud 平台上，身份验证通常会自动处理。本地开发时，需设置 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量指向服务账号的 JSON 密钥文件，或通过编程方式配置。

### 使用客户端库
完成配置后，导入必要类、创建服务对象并进行 API 调用。例如列出 Cloud Storage 中的存储桶：

```java
import com.google.cloud.storage.*;
Storage storage = StorageOptions.getDefaultInstance().getService();
Page<Bucket> buckets = storage.list();
for (Bucket bucket : buckets.iterateAll()) {
    System.out.println(bucket.getName());
}
```

值得关注的是，这些库支持多种 Google Cloud 服务，每个服务在 `com.google.cloud` 下都有独立子包（如 BigQuery 对应 `com.google.cloud.bigquery`），提供了远超存储功能的丰富特性。

---

### 调研笔记：Java 中使用 `com.google.cloud` 的完整指南

本笔记详细探讨了如何使用 Google Cloud Java 客户端库（特别是 `com.google.cloud` 包）与 Google Cloud 服务交互。在直接回答的基础上，整合了研究中的所有相关细节，按逻辑组织形成清晰深入的指南，适合需要全面理解的开发者参考。

#### Google Cloud Java 客户端库简介
`com.google.cloud` 包下的 Google Cloud Java 客户端库为与 Cloud Storage、BigQuery 和 Compute Engine 等 Google Cloud 服务交互提供了符合语言习惯的直观接口。这些库旨在减少模板代码、处理底层通信细节，并与 Java 开发实践无缝集成。如官方文档强调，它们特别适用于构建云原生应用，可结合 Spring、Maven 和 Kubernetes 等工具使用。

#### 搭建开发环境
首先需要 Java 开发工具包（JDK）8 或更高版本以确保库的兼容性。根据环境配置指南推荐，建议使用经过 Java SE TCK 认证的开源发行版 Eclipse Temurin。此外，需配备 Maven 或 Gradle 等构建自动化工具来管理依赖。还可安装 Google Cloud CLI（`gcloud`）通过命令行与资源交互，方便部署和监控任务。

#### 管理依赖
通过 Google Cloud 提供的物料清单（BOM）可简化依赖管理，帮助跨多个库统一版本。Maven 用户需在 `pom.xml` 中添加：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.google.cloud</groupId>
            <artifactId>libraries-bom</artifactId>
            <version>latest_version</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<dependencies>
    <dependency>
        <groupId>com.google.cloud</groupId>
        <artifactId>google-cloud-storage</artifactId>
    </dependency>
</dependencies>
```

Gradle 用户需进行类似配置以确保版本一致性。版本号应参照 [Google Cloud Java 客户端库 GitHub 仓库](https://github.com/googleapis/google-cloud-java) 的最新信息。该仓库还详细说明了支持的平台（包括 x86_64、Mac OS X、Windows 和 Linux），但注明在 Android 和树莓派上存在限制。

#### 身份验证机制
身份验证是关键步骤，不同环境下的选项有所差异。在 Compute Engine、Kubernetes Engine 或 App Engine 等 Google Cloud 平台上，凭证可自动推断，简化了流程。其他环境（如本地开发）可使用以下方法：

- **服务账号（推荐）**：从 Google Cloud 控制台生成 JSON 密钥文件，并将 `GOOGLE_APPLICATION_CREDENTIALS` 环境变量设置为其路径。或通过编程方式加载：
  ```java
  import com.google.auth.oauth2.GoogleCredentials;
  import com.google.cloud.storage.*;
  GoogleCredentials credentials = GoogleCredentials.fromStream(new FileInputStream("path/to/key.json"));
  Storage storage = StorageOptions.newBuilder().setCredentials(credentials).build().getService();
  ```
- **本地开发/测试**：使用 Google Cloud SDK 执行 `gcloud auth application-default login` 获取临时凭证。
- **现有 OAuth2 令牌**：特定场景下可使用 `GoogleCredentials.create(new AccessToken(accessToken, expirationTime))`。

项目 ID 的指定优先级依次为：服务选项、环境变量 `GOOGLE_CLOUD_PROJECT`、App Engine/Compute Engine、JSON 凭证文件和 Google Cloud SDK，可通过 `ServiceOptions.getDefaultProjectId()` 辅助推断项目 ID。

#### 使用客户端库
完成依赖和身份验证配置后，开发者可使用这些库与 Google Cloud 服务交互。每个服务在 `com.google.cloud` 下都有独立子包，例如 Cloud Storage 对应 `com.google.cloud.storage`，BigQuery 对应 `com.google.cloud.bigquery`。以下是 Cloud Storage 的详细示例：

```java
import com.google.cloud.storage.*;
Storage storage = StorageOptions.getDefaultInstance().getService();
Page<Bucket> buckets = storage.list();
for (Bucket bucket : buckets.iterateAll()) {
    System.out.println(bucket.getName());
}
```

此示例列出了所有存储桶，该库还支持上传对象、下载文件和管理存储桶策略等操作。其他服务也适用类似模式，具体方法详见相应 javadoc（如 [Google Cloud Java 参考文档](https://googleapis.dev/java/google-cloud-clients/latest/) 中的 BigQuery 部分）。

#### 高级特性与注意事项
这些库支持高级功能，例如使用 `OperationFuture` 进行长时操作（LRO），并支持配置超时和重试策略。以 AI Platform（v3.24.0）为例，默认设置包括初始重试延迟 5000ms、乘数 1.5、最大重试延迟 45000ms 和总超时 300000ms。同时支持代理配置，HTTPS/gRPC 使用 `https.proxyHost` 和 `https.proxyPort`，gRPC 还可通过 `ProxyDetector` 进行自定义配置。

部分 API 支持 API 密钥认证，可通过 gRPC 或 REST 的 header 手动设置（如 Language service 示例）。测试方面提供了相应工具（详见仓库的 TESTING.md），IntelliJ 和 Eclipse 的 IDE 插件通过库集成增强了开发体验。

#### 支持的平台与限制
这些库兼容多种平台：HTTP 客户端全平台通用，gRPC 客户端支持 x86_64、Mac OS X、Windows 和 Linux。但不支持 Android、树莓派和 App Engine Standard Java 7（Datastore、Storage 和 BigQuery 除外）。支持的环境包括 Windows x86_64、Mac OS X x86_64、Linux x86_64、GCE、GKE、GAE Std J8、GAE Flex 和 Alpine Linux（Java 11+）。

#### 资源与延伸阅读
[Google Cloud Java 客户端库 GitHub 仓库](https://github.com/googleapis/google-cloud-java) 提供代码示例、贡献指南和故障排除资源。[Baeldung](https://www.baeldung.com/java-google-cloud-storage) 等教程提供了实践示例（如使用 Cloud Storage），[Google Cloud for Developers](https://developers.google.com/learn/topics/cloud-java) 的官方文档则涵盖更广泛的应用开发概念。

#### 表格：关键配置详情

| **配置项**               | **详细说明**                                                                                  |
|--------------------------|----------------------------------------------------------------------------------------------|
| Java 版本要求           | 需 Java 8 或更高版本                                                                         |
| 依赖管理                | 使用 BOM 确保版本一致性，例如 Maven 的 `libraries-bom`                                      |
| 身份验证方式            | GCE/GKE/GAE 平台自动处理，本地通过 `GOOGLE_APPLICATION_CREDENTIALS` 或编程方式手动配置       |
| 支持平台                | HTTP 客户端全平台支持，gRPC 支持 x86_64/Mac OS X/Windows/Linux；不支持 Android/树莓派       |
| 服务示例                | Cloud Storage：`com.google.cloud.storage`，支持存储桶列举、对象管理等操作                   |

本完整指南确保开发者掌握在 Java 中有效使用 `com.google.cloud` 的所有必要信息，涵盖环境搭建、身份验证、使用方法和高级特性，并提供权威参考资料供深入探索。

#### 关键引用
- [Google Cloud Java 客户端库 GitHub 仓库（含详细代码与配置）](https://github.com/googleapis/google-cloud-java)
- [Google Cloud Java 开发概述文档](https://cloud.google.com/products/anthos)
- [Baeldung 的 Java Google Cloud Storage 教程（实践示例）](https://www.baeldung.com/java-google-cloud-storage)
