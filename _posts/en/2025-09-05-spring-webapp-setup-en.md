---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spring Web Application Setup Without Boot
translated: false
type: note
---

Got it. Since you’re using **Java 8** with **Spring 5.2.2** (no Spring Boot here, just core Spring + web), you’ll need to set up a minimal application manually. Below is a simple example showing how to build a web app with one controller.

---

### 1. Add Required Dependencies

You already have `spring-context`, `spring-web`, and `spring-core`. For serving requests, you also need `spring-webmvc`:

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.2.2.RELEASE</version>
</dependency>
```

---

### 2. Create a Controller

```java
package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
public class HelloController {

    @ResponseBody
    @RequestMapping("/hello")
    public String hello() {
        return "Hello, Spring Web!";
    }
}
```

* `@Controller` tells Spring this is a web controller.
* `@RequestMapping("/hello")` maps to `http://localhost:8080/hello`.
* `@ResponseBody` makes it return plain text (not a JSP).

---

### 3. Define Spring Configuration

Since we’re not using Spring Boot, we must wire things manually.

```java
package com.example.demo;

import org.springframework.context.annotation.*;
import org.springframework.web.servlet.config.annotation.*;

@Configuration
@EnableWebMvc
@ComponentScan(basePackages = "com.example.demo")
public class AppConfig implements WebMvcConfigurer {
}
```

This enables Spring MVC and scans your package for controllers.

---

### 4. Set Up `web.xml` (for Tomcat/Servlet container)

If you’re packaging as a WAR:

```xml
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         version="3.1">

    <servlet>
        <servlet-name>dispatcher</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextClass</param-name>
            <param-value>org.springframework.web.context.support.AnnotationConfigWebApplicationContext</param-value>
        </init-param>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>com.example.demo.AppConfig</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

</web-app>
```

This sets up the `DispatcherServlet` and loads your `AppConfig`.

---

### 5. Run the App

* Package as a WAR and deploy to Tomcat (or Jetty).
* Start Tomcat and visit:

  ```
  http://localhost:8080/your-app/hello
  ```

* You should see:

  ```
  Hello, Spring Web!
  ```

---

👉 Question for you: do you want this app to run inside **Tomcat (WAR deployment)**, or would you prefer a **standalone `main()` launcher** (embedded server, like Spring Boot but minimal)? I can show both ways depending on your setup.
