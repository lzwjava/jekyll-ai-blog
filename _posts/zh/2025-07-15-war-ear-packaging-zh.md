---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WAR与EAR打包指南
translated: true
type: note
---

以下是 Maven **WAR** 与 **EAR** 打包方式的实用对比（无表格版），以及在实际项目中如何选择使用。

# 每种打包方式的用途

* **WAR (`packaging: war`)** – 单个 Web 应用程序：Servlet/Jakarta REST、JSP/JSF、Spring MVC/Boot（以 WAR 形式）等。可部署到 Servlet 容器（Tomcat/Jetty）或完整应用服务器的 Web 层。
* **EAR (`packaging: ear`)** – 多个模块的集合，作为一个整体部署到完整的 Java EE/Jakarta EE 应用服务器（WildFly/JBoss EAP、WebLogic、WebSphere）。通常包含一个或多个 WAR、EJB JAR 以及共享库，构成一个部署单元。

# 典型选择场景

* 选择 **WAR**：如果你只有一个 Web 应用或 Spring Boot 应用，且不需要 EJB 或多模块服务器功能。
* 选择 **EAR**：如果你需要将多个模块一起部署（例如 EJB + 多个 WAR + 共享库），需要跨模块使用应用服务器服务（XA、集中式安全域、JMS、分布式事务），或者组织规定必须使用 EAR。

# 打包内容物

* **WAR** 内容：`/WEB-INF/classes`、`/WEB-INF/lib`、可选的 `web.xml`（或注解）、静态资源。在大多数服务器中，每个 WAR 有独立的类加载器。
* **EAR** 内容：`*.war`、`*.jar`（EJB/工具类）、`META-INF/application.xml`（或注解/精简配置），以及可选的 `lib/` 目录用于模块间共享的库。提供 EAR 级别的类加载器，对所有模块可见。

# 依赖与类加载考量

* **WAR**：将 Servlet/Jakarta EE API 声明为 `provided`；其他依赖放入 `/WEB-INF/lib`。隔离更简单，版本冲突较少。
* **EAR**：将公共库放入 EAR 的 `lib/` 目录（通过 `maven-ear-plugin`），所有模块共享同一版本。注意模块库与服务器提供 API 之间的冲突；对齐版本并在适当时使用 `provided`。

# 需使用的 Maven 插件

* **WAR 项目**：`maven-war-plugin`
* **EAR 聚合项目**：`maven-ear-plugin`
* **EJB 模块（如有）**：`maven-ejb-plugin`
* 父级/聚合项目通常使用 `packaging: pom` 来关联模块。

# 最小化示例

单 Web 应用（WAR）：

```xml
<!-- pom.xml -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>my-web</artifactId><version>1.0.0</version>
  <packaging>war</packaging>

  <dependencies>
    <!-- 服务器 API 使用 provided -->
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-web-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
    <!-- 你的应用依赖 -->
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-war-plugin</artifactId>
        <version>3.4.0</version>
        <!-- 可选：配置 webResources、warName、过滤等 -->
      </plugin>
    </plugins>
  </build>
</project>
```

包含 WAR 和 EJB 的多模块 EAR：

```xml
<!-- parent/pom.xml -->
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId><artifactId>my-app</artifactId><version>1.0.0</version>
  <packaging>pom</packaging>
  <modules>
    <module>ejb-module</module>
    <module>web-module</module>
    <module>ear-assembly</module>
  </modules>
</project>
```

```xml
<!-- ejb-module/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>ejb-module</artifactId>
  <packaging>ejb</packaging>
  <dependencies>
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
  </dependencies>
</project>
```

```xml
<!-- web-module/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>web-module</artifactId>
  <packaging>war</packaging>
  <dependencies>
    <dependency>
      <groupId>jakarta.platform</groupId><artifactId>jakarta.jakartaee-web-api</artifactId>
      <version>10.0.0</version><scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>com.example</groupId><artifactId>ejb-module</artifactId><version>1.0.0</version>
      <type>ejb</type> <!-- 允许 @EJB 注入 -->
    </dependency>
  </dependencies>
</project>
```

```xml
<!-- ear-assembly/pom.xml -->
<project>
  <parent>…</parent>
  <artifactId>ear-assembly</artifactId>
  <packaging>ear</packaging>

  <dependencies>
    <dependency>
      <groupId>com.example</groupId><artifactId>web-module</artifactId><version>1.0.0</version>
      <type>war</type>
    </dependency>
    <dependency>
      <groupId>com.example</groupId><artifactId>ejb-module</artifactId><version>1.0.0</version>
      <type>ejb</type>
    </dependency>
    <!-- 放入 EAR/lib 供所有模块共享的库 -->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId><artifactId>jackson-databind</artifactId>
      <version>2.17.2</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-ear-plugin</artifactId>
        <version>3.4.0</version>
        <configuration>
          <defaultLibBundleDir>lib</defaultLibBundleDir>
          <modules>
            <webModule>
              <groupId>com.example</groupId>
              <artifactId>web-module</artifactId>
              <contextRoot>/myapp</contextRoot>
            </webModule>
            <ejbModule>
              <groupId>com.example</groupId>
              <artifactId>ejb-module</artifactId>
            </ejbModule>
          </modules>
          <!-- 可选：生成 application.xml，或提供自定义文件 -->
          <generateApplicationXml>true</generateApplicationXml>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

构建结果：

* `mvn -pl web-module -am clean package` → 生成 `web-module-1.0.0.war`
* `mvn -pl ear-assembly -am clean package` → 生成 `ear-assembly-1.0.0.ear`，内含 WAR、EJB 和 `lib/` 目录。

# 关键操作差异

* **部署目标**

  * WAR：Servlet 容器或应用服务器 Web 层。
  * EAR：完整应用服务器；以原子操作部署所有模块。
* **事务与消息**

  * 单独使用 WAR 时，只能利用容器暴露的功能；复杂的 XA/JMS 配置通常位于 EAR 内的 EJB 中。
* **版本管理与发布**

  * WAR：单个应用的重建和重新部署简单。
  * EAR：协调多个模块的版本；一个部署单元确保一致性。
* **启动时间与本地开发**

  * WAR：反馈快速，运行时更轻量。
  * EAR：较重；IDE/服务器集成有帮助，但开发周期较慢。
* **现代 Spring Boot 注意事项**

  * Boot 首选可执行 **JAR**；若部署到外部容器，也支持 WAR。
  * Boot **不** 针对 EAR；如果必须使用应用服务器，将 Boot 应用部署为 WAR，并避免使用 EAR，除非平台要求。

# 常见陷阱与技巧

* 对服务器 API 使用 `provided`，避免打包它们。
* 对于 EAR，将共享库放入 `defaultLibBundleDir`，防止在每个 WAR/EJB 内重复复制。
* 跨模块对齐 Jakarta EE 版本；版本不匹配会导致类加载错误。
* 在 WebLogic/WebSphere 上，注意类加载策略（父级优先 vs 父级最后）；有时需要供应商特定的描述符。
* 如果不需要 EJB/XA，简单的 WAR（或 Boot JAR）更简单且通常更具可移植性。

如果你告诉我你的应用服务器（Tomcat vs WildFly/WebLogic 等）以及是否有 EJB 或多个 Web 应用，我可以为你绘制所需的准确 POM 和部署描述符。
