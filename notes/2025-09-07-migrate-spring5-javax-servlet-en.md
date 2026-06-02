---
audio: false
date: 2025-09-07
generated: true
image: false
lang: en
layout: post
title: Migrating Spring 5 WAR to javax.servlet
translated: false
type: note
---

You’re almost there. Because this project is Spring 5 (javax.\* era) and a WAR, the cleanest way is: **use `javax.servlet-api` 4.x**, add a minimal `web.xml`, a Java config, and a tiny controller.

### 0) Fix the servlet API (important)

Spring 5.2.x uses `javax.servlet.*`, but your POM pulls **`jakarta.servlet-api:5.0.0`**. Swap it to `javax`:

```xml
<!-- replace the jakarta dependency with this -->
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>4.0.1</version>
  <scope>provided</scope>
</dependency>
```

(Keep Jetty 9.4 — it’s Servlet 3.1/4.0 friendly with javax.)

### 1) `web.xml` (since you set `failOnMissingWebXml=true`)

Create `src/main/webapp/WEB-INF/web.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                             http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

  <!-- Root Spring context (services/repos if you add them later) -->
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

  <!-- DispatcherServlet for MVC -->
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

### 2) Java config

Create two config classes.

`src/main/java/com/lzw/config/RootConfig.java`:

```java
package com.lzw.config;

import org.springframework.context.annotation.Configuration;

@Configuration
public class RootConfig {
    // Add @Bean definitions for services/repositories if/when you have them.
}
```

`src/main/java/com/lzw/config/WebConfig.java`:

```java
package com.lzw.config;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.lzw.web")
public class WebConfig {
    // Keep empty for REST-only. Add view resolvers/static resource handlers later if needed.
}
```

### 3) Hello controller

`src/main/java/com/lzw/web/HelloController.java`:

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

### 4) Directory layout sanity check

* `src/main/webapp/WEB-INF/web.xml`
* `src/main/java/com/lzw/config/{RootConfig,WebConfig}.java`
* `src/main/java/com/lzw/web/HelloController.java`

### 5) Run it

Since you already have Jetty in the POM:

```bash
mvn clean package
mvn jetty:run
```

Open: `http://localhost:8080/hello` → should print `Hello, Spring MVC!`.

---

#### Notes & pitfalls

* If you **must** keep `jakarta.servlet-api:5.x`, you’d need Spring 6 / Spring Boot 3+ (Jakarta namespace) and a newer servlet container. For your current stack (Spring 5.2.2), **use `javax.servlet-api:4.0.1`**.
* Because you set `maven-war-plugin` with `failOnMissingWebXml=true`, `web.xml` is required even though Spring 3.1+ can run without it.
* For views (JSP/Thymeleaf) later, add a view resolver in `WebConfig`; for pure JSON, the `@RestController` approach above is enough.
