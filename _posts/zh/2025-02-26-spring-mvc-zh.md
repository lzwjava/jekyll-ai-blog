---
audio: false
generated: true
lang: zh
layout: post
title: Spring MVC
translated: true
type: note
---

要在不使用 **Spring Boot** 的情况下使用 **Spring MVC**，你需要手动配置 Spring 框架，因为 Spring Boot 通常会自动化大部分设置。以下是通过基于 XML 的配置创建一个简单 Spring MVC Web 应用程序的逐步指南。本示例将搭建一个基础应用程序，包含一个在 JSP 页面上显示“欢迎”信息的控制器。

---

## 逐步指南

### 1. 设置项目结构
创建一个标准的 Web 应用程序结构。你可以使用 IntelliJ 或 Eclipse 等 IDE，或手动创建文件夹。结构应如下所示：

```
SimpleSpringMVCApp/
├── src/
│   └── main/
│       └── java/
│           └── com/
│               └── example/
│                   └── controllers/
│                       └── HomeController.java
│       └── webapp/
│           └── WEB-INF/
│               ├── web.xml
│               ├── spring-mvc-config.xml
│               └── views/
│                   └── home.jsp
└── pom.xml  (如果使用 Maven)
```

- **`src/main/java`**：包含你的 Java 源代码（例如控制器）。
- **`src/main/webapp/WEB-INF`**：包含配置文件（`web.xml`、`spring-mvc-config.xml`）和 JSP 视图。

### 2. 添加依赖项
如果使用 Maven，请在 `pom.xml` 中包含所需的依赖项。对于简单的 Spring MVC 应用程序，你需要 Spring Web MVC 库和 Servlet API（由容器提供）。

创建或编辑 `pom.xml`，内容如下：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>SimpleSpringMVCApp</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>war</packaging>

    <dependencies>
        <!-- Spring Web MVC -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>5.3.10</version>
        </dependency>
        <!-- Servlet API (provided by the container) -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.3.1</version>
            </plugin>
        </plugins>
    </build>
</project>
```

- **注意事项**：
  - `<packaging>war</packaging>`：确保项目打包为 WAR 文件，以便部署到 Servlet 容器。
  - 如果不使用 Maven，请手动下载 Spring MVC JAR 和 Servlet API JAR，并将其添加到项目的类路径中。

### 3. 在 `web.xml` 中配置 DispatcherServlet
`web.xml` 文件是 Web 应用程序的部署描述符。它配置 `DispatcherServlet`（Spring MVC 的前端控制器）以处理传入请求。

创建 `src/main/webapp/WEB-INF/web.xml`，内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <!-- Define the DispatcherServlet -->
    <servlet>
        <servlet-name>spring-mvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>/WEB-INF/spring-mvc-config.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <!-- Map the DispatcherServlet to handle all requests -->
    <servlet-mapping>
        <servlet-name>spring-mvc</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

- **解释**：
  - `<servlet-class>`：指定 `DispatcherServlet`，用于将请求路由到控制器。
  - `<init-param>`：指向 Spring 配置文件（`spring-mvc-config.xml`）。
  - `<url-pattern>/</url-pattern>`：将 Servlet 映射到处理所有应用程序请求。

### 4. 创建 Spring 配置文件
创建 `src/main/webapp/WEB-INF/spring-mvc-config.xml` 以定义 Spring MVC Bean，例如控制器和视图解析器。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
           http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
           http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
           http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc.xsd">

    <!-- Enable component scanning for controllers -->
    <context:component-scan base-package="com.example.controllers" />

    <!-- Enable annotation-driven MVC -->
    <mvc:annotation-driven />

    <!-- Configure view resolver for JSP files -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="prefix" value="/WEB-INF/views/" />
        <property name="suffix" value=".jsp" />
    </bean>
</beans>
```

- **解释**：
  - `<context:component-scan>`：扫描 `com.example.controllers` 包中的注解组件（例如 `@Controller`）。
  - `<mvc:annotation-driven>`：启用基于注解的 MVC 功能（例如 `@GetMapping`）。
  - `InternalResourceViewResolver`：将视图名称映射到 `/WEB-INF/views/` 目录下的 JSP 文件，并添加 `.jsp` 后缀。

### 5. 创建简单控制器
创建一个控制器来处理 HTTP 请求。在 `src/main/java/com/example/controllers/` 中添加 `HomeController.java`：

```java
package com.example.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "home";
    }
}
```

- **解释**：
  - `@Controller`：将该类标记为 Spring MVC 控制器。
  - `@GetMapping("/")`：将 GET 请求映射到根 URL（`/`）的 `home()` 方法。
  - `return "home"`：返回视图名称 `"home"`，解析为 `/WEB-INF/views/home.jsp`。

### 6. 创建 JSP 视图
创建一个简单的 JSP 文件以显示输出。在 `src/main/webapp/WEB-INF/views/` 中添加 `home.jsp`：

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Home</title>
</head>
<body>
    <h1>Welcome to Spring MVC without Spring Boot</h1>
</body>
</html>
```

### 7. 构建和打包应用程序
如果使用 Maven，从项目根目录运行以下命令以构建 WAR 文件：

```bash
mvn clean package
```

这将在 `target` 目录中生成 `SimpleSpringMVCApp-1.0-SNAPSHOT.war`。

- **注意**：如果不使用 Maven，请编译 Java 文件并手动将项目打包为 WAR 文件，同时保持文件夹结构。

### 8. 部署应用程序
将 WAR 文件部署到 Servlet 容器（如 Apache Tomcat）：
- 将 `SimpleSpringMVCApp-1.0-SNAPSHOT.war` 复制到 Tomcat 安装目录的 `webapps` 目录中。
- 启动 Tomcat（例如，从 Tomcat 的 `bin` 目录运行 `startup.sh` 或 `startup.bat`）。

### 9. 访问应用程序
打开浏览器并导航到：

```
http://localhost:8080/SimpleSpringMVCApp-1.0-SNAPSHOT/
```

你将看到：
```
Welcome to Spring MVC without Spring Boot
```

- **注意**：上下文路径（`/SimpleSpringMVCApp-1.0-SNAPSHOT`）取决于 WAR 文件名。如果将 WAR 文件重命名为 `myapp.war`，则 URL 变为 `http://localhost:8080/myapp/`。

---

## 总结
要使用 **Spring MVC 而不使用 Spring Boot**：
1. **设置 Web 项目**，采用标准结构。
2. **添加依赖项**，包括 Spring MVC 和 Servlet API。
3. **在 `web.xml` 中配置 DispatcherServlet**。
4. **在 XML 文件中定义 Spring 配置**（例如 `spring-mvc-config.xml`）。
5. **创建控制器**以处理请求。
6. **添加 JSP 视图**以显示响应。
7. **构建并部署** WAR 文件到 Servlet 容器。

这种方法让你可以完全控制配置，是学习 Spring MVC 基础知识的绝佳方式！
