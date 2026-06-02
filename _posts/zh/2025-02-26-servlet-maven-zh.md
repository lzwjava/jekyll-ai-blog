---
audio: false
generated: true
lang: zh
layout: post
title: 使用Maven构建Java Servlet应用
translated: true
type: note
---

以下是使用 Maven 构建项目并通过 Liberty Maven 插件部署，在 WebSphere Liberty Profile (WLP) 上创建和部署简单 Java Servlet 应用程序的完整指南。本示例将创建一个基础 Servlet，在访问时返回 "Hello World!"，使用 Maven 将其构建为 WAR 文件并部署到 WLP。我们假设您已设置好启用了 `servlet-4.0` 功能的 WLP，因为这提供了必要的 Servlet 支持。

---

## 分步指南

### 1. 创建 Maven 项目结构
首先设置标准的 Maven Web 应用程序结构。您可以手动创建或使用 Maven 生成。

- **目录结构：**
  ```
  SimpleServletApp/
  ├── pom.xml
  └── src/
      └── main/
          ├── java/
          │   └── com/
          │       └── example/
          │           └── HelloServlet.java
          └── webapp/
              └── WEB-INF/
                  └── web.xml
  ```

- **可选使用 Maven 生成：**
  运行以下命令创建结构，然后根据需要调整：
  ```bash
  mvn archetype:generate -DgroupId=com.example -DartifactId=simple-servlet-app -DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false
  ```
  这将创建一个基本的 Web 应用程序结构，您将在后续步骤中进行修改。

### 2. 编写 Servlet 代码
在 `src/main/java/com/example/` 目录下创建名为 `HelloServlet.java` 的文件，内容如下：

```java
package com.example;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain");
        resp.getWriter().write("Hello World!");
    }
}
```

- **说明：** 此 Servlet 响应 HTTP GET 请求，返回纯文本 "Hello World!"。它使用简单的 `doGet` 方法，并避免使用注解以确保与显式 `web.xml` 配置的兼容性。

### 3. 创建 `web.xml` 部署描述符
在 `src/main/webapp/WEB-INF/` 目录下创建名为 `web.xml` 的文件，内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    <servlet>
        <servlet-name>HelloServlet</servlet-name>
        <servlet-class>com.example.HelloServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>HelloServlet</servlet-name>
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>
```

- **说明：** `web.xml` 文件定义了 `HelloServlet` 类并将其映射到 `/hello` URL 模式。由于我们没有使用 `@WebServlet` 注解，因此这是必需的。

### 4. 配置 Maven `pom.xml`
在 `SimpleServletApp/` 目录下创建或更新 `pom.xml`，内容如下：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>simple-servlet-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>war</packaging>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <!-- Servlet API（由 WLP 提供） -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Maven WAR 插件用于构建 WAR 文件 -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.3.1</version>
                <configuration>
                    <finalName>myapp</finalName>
                </configuration>
            </plugin>
            <!-- Liberty Maven 插件用于部署 -->
            <plugin>
                <groupId>io.openliberty.tools</groupId>
                <artifactId>liberty-maven-plugin</artifactId>
                <version>3.3.4</version>
                <configuration>
                    <installDirectory>/opt/ibm/wlp</installDirectory>
                    <serverName>myServer</serverName>
                    <appsDirectory>dropins</appsDirectory>
                    <looseApplication>false</looseApplication>
                    <stripVersion>true</stripVersion>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

- **说明：**
  - **坐标：** 使用 `groupId`、`artifactId` 和 `version` 定义项目。`packaging` 设置为 `war` 表示这是一个 Web 应用程序。
  - **属性：** 将 Java 8 设置为源版本和目标版本。
  - **依赖项：** 包含 Servlet API，作用域为 `provided`，因为它在运行时由 WLP 提供。
  - **Maven WAR 插件：** 使用 `<finalName>` 将 WAR 文件名配置为 `myapp.war`。
  - **Liberty Maven 插件：** 配置部署到位于 `/opt/ibm/wlp` 的 Liberty 服务器，服务器名称为 `myServer`，部署到 `dropins` 目录。

### 5. 构建项目
在 `SimpleServletApp/` 目录下，使用 Maven 构建 WAR 文件：

```bash
mvn clean package
```

- **结果：** 这将编译 Servlet，将其与 `web.xml` 一起打包到 `target/myapp.war` 中，并准备部署。

### 6. 在 WebSphere Liberty 上部署和运行
确保您的 Liberty 服务器 (`myServer`) 已设置并启用了 `servlet-4.0` 功能。检查您的 `server.xml` 是否包含：
```xml
<featureManager>
    <feature>servlet-4.0</feature>
</featureManager>
```

使用 Liberty Maven 插件部署并运行应用程序：

```bash
mvn liberty:run
```

- **过程：**
  - 在前台启动 Liberty 服务器（如果尚未运行）。
  - 自动将 `myapp.war` 部署到 `dropins` 目录。
  - 保持服务器运行直到手动停止。

- **验证部署：** 查找类似以下的日志消息：
  ```
  [AUDIT   ] CWWKT0016I: Web application available (default_host): http://localhost:9080/myapp/
  ```
  日志通常位于 `/opt/ibm/wlp/usr/servers/myServer/logs/console.log`。

### 7. 访问应用程序
打开浏览器并导航到：

```
http://localhost:9080/myapp/hello
```

- **预期输出：**
  ```
  Hello World!
  ```

- **URL 解析：**
  - `9080`：WLP 的默认 HTTP 端口。
  - `/myapp`：来自 WAR 文件名 (`myapp.war`) 的上下文根。
  - `/hello`：来自 `web.xml` 的 URL 模式。

### 8. 停止服务器
由于 `mvn liberty:run` 在前台运行服务器，请在终端中按 `Ctrl+C` 停止它。

---

## 注意事项
- **前提条件：**
  - Maven 必须在您的系统上安装并配置好。
  - Liberty 必须安装在 `/opt/ibm/wlp`，并且服务器实例 `myServer` 必须存在。如果您的设置不同（例如 `/usr/local/wlp` 或 `defaultServer`），请在 `pom.xml` 中调整 `installDirectory` 和 `serverName`。
  - `server.xml` 中必须启用 `servlet-4.0` 功能。

- **替代部署方式：**
  - 要分别构建和部署：
    ```bash
    mvn clean package
    mvn liberty:deploy
    ```
    如果需要，手动启动服务器：
    ```bash
    /opt/ibm/wlp/bin/server start myServer
    ```

- **端口配置：** 如果您的 Liberty 服务器使用不同的 HTTP 端口，请检查 `server.xml` 中的 `<httpEndpoint>` 并相应调整 URL。

- **上下文根：** 在 `pom.xml` 中重命名 `<finalName>`（例如 `<finalName>app</finalName>`）以将上下文根更改为 `/app`。

- **故障排除：**
  - 如果部署失败，请验证 `pom.xml` 中的 `installDirectory` 和 `serverName`。
  - 检查 `/opt/ibm/wlp/usr/servers/myServer/logs/messages.log` 中的错误日志。
  - 确保使用 Java 8 或更高版本，与 `maven.compiler` 设置匹配。

---

## 总结
本指南演示了如何：
1. 设置一个包含简单 Servlet (`HelloServlet.java`) 和 `web.xml` 的 Maven 项目。
2. 使用 Servlet API、Maven WAR 插件和 Liberty Maven 插件配置 `pom.xml`。
3. 使用 `mvn clean package` 将应用程序构建为 `myapp.war`。
4. 使用 `mvn liberty:run` 在 WLP 上部署和运行它。
5. 在 `http://localhost:9080/myapp/hello` 访问 "Hello World!"。

这提供了一种基于 Maven 的简化方法，用于在 WebSphere Liberty Profile 上开发和部署 Servlet 应用程序。

---
