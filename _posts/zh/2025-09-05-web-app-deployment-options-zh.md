---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Web应用部署方案详解
translated: true
type: note
---

明白了 — 我来为您清晰解释这些选项。

### 选项一：快速开发配置（推荐）

这是开发期间启动项目最简单的方式。
如果您的 `pom.xml` 已包含 Tomcat 或 Jetty 插件，您可以直接运行：

```bash
mvn tomcat7:run
```

或

```bash
mvn jetty:run
```

这将在嵌入式 Tomcat/Jetty 中启动 Web 应用，无需构建 WAR 包或手动部署。如果尚未配置插件，您需要先将其添加到 `pom.xml` 中。

---

### 选项二：构建并部署 WAR 包

这是更“传统”的方式。您需要将应用打包为 WAR 文件：

```bash
mvn clean package
```

这会生成类似 `target/playground-server-1.0.war` 的文件。
随后将该 WAR 文件复制到独立 Tomcat/Jetty 服务器的 `webapps/` 目录，重启服务器后即可通过浏览器访问部署的应用。

---

### 选项三：使用嵌入式服务器（手动配置）

当前您的 `Application.main()` 仅启动 Spring 上下文 — 并未实际启动 Web 服务器。
如果您希望应用自行启动 Tomcat（不依赖外部服务器），需要修改主类，通过编程方式配置并启动嵌入式 Tomcat 实例。

这样您将获得自包含的可运行 JAR，但需要编写额外的配置代码。

---

### 选项四：Spring Boot 迁移

本项目目前**包含部分 Spring Boot 测试配置**，但尚未成为真正的 Spring Boot 应用。因此运行：

```bash
mvn spring-boot:run
```

会执行失败。

如需迁移，您可以：

* 添加正确的 Spring Boot starter 依赖
* 将主类改为 `@SpringBootApplication`
* 之后即可通过 `mvn spring-boot:run` 或 `java -jar target/app.jar` 直接运行

这是最现代化的方案，但需要对代码和 `pom.xml` 进行一些调整。

---

✅ **总结**：

* 若需快速测试 → 选择**选项一**
* 若需部署至现有服务器 → 选择**选项二**
* 若需要不依赖外部 Tomcat 的自包含应用 → 选择**选项三**
* 若希望实现长期现代化简化 → 选择**选项四**

---

需要我为您提供**选项一（Tomcat/Jetty 插件）的 `pom.xml` 配置片段**吗？这样您就可以立即运行 `mvn tomcat7:run` 了。
