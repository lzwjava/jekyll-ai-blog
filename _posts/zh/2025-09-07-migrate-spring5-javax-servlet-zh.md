---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: Spring 5 WAR项目迁移至javax.servlet
translated: true
type: note
---

你离成功很近了。由于这个项目是 Spring 5（javax.* 时代）且采用 WAR 包，最简洁的方案是：**使用 `javax.servlet-api` 4.x**，添加最简化的 `web.xml`、Java 配置和一个小型控制器。

### 0) 修复 Servlet API（重要）

Spring 5.2.x 使用 `javax.servlet.*`，但你的 POM 引入了 **`jakarta.servlet-api:5.0.0`**。需替换为 `javax`：

```xml
<!-- 将 jakarta 依赖替换为此项 -->
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>4.0.1</version>
  <scope>provided</scope>
</dependency>
```

（保留 Jetty 9.4 —— 它兼容 Servlet 3.1/4.0 且支持 javax。）

### 1) `web.xml`（因你设置了 `failOnMissingWebXml=true`）

创建 `src/main/webapp/WEB-INF/web.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

  <!-- 根 Spring 上下文（后续添加服务层/仓储层时使用） -->
  <listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
  </listener>
  <context-param>
    <param-name>contextClass</param-name>
    <param-value>org.springframework.web.context.support.AnnotationConfigWebApplicationContext</param-value>
  </context-param>
  <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>com.lzw.config.RootConfig</param-value>
  </context-param>

  <!-- MVC 调度器 Servlet -->
  <servlet>
    <servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
      <param-name>contextClass</param-name>
      <param-value>org.springframework.web.context.support.AnnotationConfigWebApplicationContext</param-value>
    </init-param>
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>com.lzw.config.WebConfig</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>

  <servlet-mapping>
    <servlet-name>dispatcher</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>

</web-app>
```

### 2) Java 配置

创建两个配置类。

`src/main/java/com/lzw/config/RootConfig.java`：

```java
package com.lzw.config;

import org.springframework.context.annotation.Configuration;

@Configuration
public class RootConfig {
    // 后续若有服务层/仓储层，可在此添加 @Bean 定义
}
```

`src/main/java/com/lzw/config/WebConfig.java`：

```java
package com.lzw.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.lzw.web")
public class WebConfig {
    // 纯 REST 应用可留空。后续如需视图解析/静态资源处理再补充配置
}
```

### 3) 示例控制器

`src/main/java/com/lzw/web/HelloController.java`：

```java
package com.lzw.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring MVC!";
    }
}
```

### 4) 目录结构检查

* `src/main/webapp/WEB-INF/web.xml`
* `src/main/java/com/lzw/config/{RootConfig,WebConfig}.java`
* `src/main/java/com/lzw/web/HelloController.java`

### 5) 运行项目

由于 POM 中已配置 Jetty：

```bash
mvn clean package
mvn jetty:run
```

访问：`http://localhost:8080/hello` → 应显示 `Hello, Spring MVC!`。

---

#### 注意事项与常见问题

* 若**必须**使用 `jakarta.servlet-api:5.x`，需升级至 Spring 6 / Spring Boot 3+（Jakarta 命名空间）并更换新版 Servlet 容器。当前技术栈（Spring 5.2.2）请**使用 `javax.servlet-api:4.0.1`**。
* 因在 `maven-war-plugin` 中设置了 `failOnMissingWebXml=true`，即使 Spring 3.1+ 可无 `web.xml` 运行，此处仍需该文件。
* 后续若需视图支持（JSP/Thymeleaf），请在 `WebConfig` 中添加视图解析器；纯 JSON 应用使用上述 `@RestController` 方案即可。
