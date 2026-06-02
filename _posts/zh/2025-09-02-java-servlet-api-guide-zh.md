---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java Servlet API 核心指南
translated: true
type: note
---

以下是 Java **Servlet** API 的实用端到端指南，涵盖经典 **`javax.servlet.*`** 命名空间（Servlet 2.x–4.x 时代）。我也会说明迁移到 **`jakarta.servlet.*`** 后的变化，助你面向未来。

# 1) 什么是 Servlet？

**Servlet** 是在 **Servlet 容器**（Tomcat、Jetty、WebSphere、WebLogic 等）内部运行的 Java 类，用于处理 HTTP 请求/响应。容器负责管理：

* 生命周期（加载、初始化、服务、销毁）
* 多线程和请求路由
* 会话、安全、资源和配置

# 2) 核心包与关键接口（javax.\*）

* `javax.servlet.Servlet`、`ServletConfig`、`ServletContext`
* `javax.servlet.http.HttpServlet`、`HttpServletRequest`、`HttpServletResponse`、`HttpSession`、`Cookie`
* `javax.servlet.Filter`、`FilterChain`、`FilterConfig`
* `javax.servlet.ServletRequestListener` 及其他监听器
* `javax.servlet.annotation.*`（自 3.0 起：`@WebServlet`、`@WebFilter`、`@WebListener`、`@MultipartConfig`）
* 自 3.0 起：**异步**（`AsyncContext`）、编程式注册
* 自 3.1 起：**非阻塞 I/O**（`ServletInputStream`/`ServletOutputStream` 配合 `ReadListener`/`WriteListener`）
* 自 4.0 起：HTTP/2 支持（如 `PushBuilder`）

> Jakarta 变更：从 **Servlet 5.0**（Jakarta EE 9）开始，包名改为 `jakarta.servlet.*`。大多数 API 保持不变；迁移时需更新导入和依赖项。

# 3) Servlet 生命周期与线程模型

* **加载**：容器加载类，每个声明创建单一实例。
* **`init(ServletConfig)`**：调用一次。读取初始化参数，缓存重型资源。
* **`service(req, res)`**：每个请求调用一次。`HttpServlet` 会分派到 `doGet`、`doPost` 等方法。
* **`destroy()`**：在关闭/重新部署时调用一次。

**线程**：容器在同一实例上并发调用 `service`。
**规则**：避免可变实例字段；如必须使用，请采用线程安全结构或适当同步。优先使用局部变量。

# 4) 最小化 Servlet（注解方式）

```java
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import javax.servlet.ServletException;
import java.io.IOException;

@WebServlet(name = "HelloServlet", urlPatterns = "/hello")
public class HelloServlet extends HttpServlet {
  @Override protected void doGet(HttpServletRequest req, HttpServletResponse resp)
      throws ServletException, IOException {
    resp.setContentType("text/plain;charset=UTF-8");
    resp.getWriter().println("Hello, Servlet!");
  }
}
```

# 5) `web.xml` 与注解对比

**注解（3.0+）** 对简单应用最便捷。
**`web.xml`** 仍适用于排序、覆盖或遗留容器。

最小化 `web.xml`：

```xml
<web-app xmlns="http://java.sun.com/xml/ns/javaee" version="3.0">
  <servlet>
    <servlet-name>HelloServlet</servlet-name>
    <servlet-class>com.example.HelloServlet</servlet-class>
    <init-param>
      <param-name>greeting</param-name>
      <param-value>Hi</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>HelloServlet</servlet-name>
    <url-pattern>/hello</url-pattern>
  </servlet-mapping>
</web-app>
```

# 6) HTTP 请求/响应要点

## 读取请求数据

```java
String q = req.getParameter("q");        // 查询/表单字段
Enumeration<String> names = req.getParameterNames();
BufferedReader reader = req.getReader(); // 原始正文文本
ServletInputStream in = req.getInputStream(); // 二进制正文
String header = req.getHeader("X-Token");
```

**提示**：读取参数前始终设置编码：

```java
req.setCharacterEncoding("UTF-8");
```

## 写入响应

```java
resp.setStatus(HttpServletResponse.SC_OK);
resp.setContentType("application/json;charset=UTF-8");
resp.setHeader("Cache-Control", "no-store");
try (PrintWriter out = resp.getWriter()) {
  out.write("{\"ok\":true}");
}
```

# 7) doGet 与 doPost 及其他方法对比

* `doGet`：幂等读取；使用查询字符串。
* `doPost`：通过表单或 JSON 正文创建/更新。
* `doPut`/`doDelete`/`doPatch`：RESTful 语义（客户端必须支持）。
* 始终显式验证输入并处理内容类型。

# 8) 会话与 Cookie

```java
HttpSession session = req.getSession(); // 不存在则创建
session.setAttribute("userId", 123L);
Long userId = (Long) session.getAttribute("userId");
session.invalidate(); // 登出
```

通过容器或编程方式配置会话 Cookie 标志：

* `HttpOnly`（防止 JS 访问）、`Secure`（HTTPS）、`SameSite=Lax/Strict`
  考虑使用无状态令牌实现水平扩展；否则使用粘性会话或外部会话存储。

# 9) 过滤器（横切关注点）

使用 **过滤器** 处理日志、认证、CORS、压缩、编码等。

```java
import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import java.io.IOException;

@WebFilter(urlPatterns = "/*")
public class LoggingFilter implements Filter {
  public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    long start = System.nanoTime();
    try {
      chain.doFilter(req, res);
    } finally {
      long ms = (System.nanoTime() - start) / 1_000_000;
      req.getServletContext().log("Handled in " + ms + " ms");
    }
  }
}
```

# 10) 监听器（应用与请求钩子）

常用监听器：

* `ServletContextListener`：应用启动/关闭（初始化连接池、预热缓存）
* `HttpSessionListener`：创建/销毁会话（指标、清理）
* `ServletRequestListener`：每个请求的钩子（跟踪 ID）

示例：

```java
@WebListener
public class AppBoot implements javax.servlet.ServletContextListener {
  public void contextInitialized(javax.servlet.ServletContextEvent sce) {
    sce.getServletContext().log("App starting...");
  }
  public void contextDestroyed(javax.servlet.ServletContextEvent sce) {
    sce.getServletContext().log("App stopping...");
  }
}
```

# 11) 异步与非阻塞 I/O

## 异步（Servlet 3.0）

允许在后端调用运行时释放容器线程。

```java
@WebServlet(urlPatterns="/async", asyncSupported=true)
public class AsyncDemo extends HttpServlet {
  protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
    AsyncContext ctx = req.startAsync();
    ctx.start(() -> {
      try {
        // 调用慢速服务...
        ctx.getResponse().getWriter().println("done");
      } catch (Exception e) {
        ctx.complete();
      } finally {
        ctx.complete();
      }
    });
  }
}
```

## 非阻塞（Servlet 3.1）

在流上注册 `ReadListener`/`WriteListener` 以实现事件驱动 I/O。适用于流式传输大型正文而不阻塞线程。

# 12) 文件上传（多部分）

```java
import javax.servlet.annotation.MultipartConfig;

@MultipartConfig(maxFileSize = 10 * 1024 * 1024)
@WebServlet("/upload")
public class UploadServlet extends HttpServlet {
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException, ServletException {
    Part file = req.getPart("file");
    String filename = file.getSubmittedFileName();
    try (InputStream is = file.getInputStream()) {
      // 保存...
    }
    resp.getWriter().println("Uploaded " + filename);
  }
}
```

确保客户端发送 `Content-Type: multipart/form-data`。

# 13) 分发与模板

* **转发**：服务器端内部分发；原始 URL 保持不变。

  ```java
  req.getRequestDispatcher("/WEB-INF/view.jsp").forward(req, resp);
  ```

* **包含**：包含另一资源的输出。

  ```java
  req.getRequestDispatcher("/fragment").include(req, resp);
  ```

* **重定向**：客户端 302/303/307 到新 URL。

  ```java
  resp.sendRedirect(req.getContextPath() + "/login");
  ```

# 14) 字符编码与国际化

简单的**编码过滤器**可防止乱码：

```java
@WebFilter("/*")
public class Utf8Filter implements Filter {
  public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    req.setCharacterEncoding("UTF-8");
    res.setCharacterEncoding("UTF-8");
    chain.doFilter(req, res);
  }
}
```

使用 `HttpServletRequest#getLocale()` 获取 `Locale` 并结合资源包实现国际化。

# 15) 安全基础

* **传输**：始终使用 HTTPS；设置 `Secure` Cookie。
* **认证**：容器管理（FORM/BASIC/DIGEST），或使用带有 JWT/会话的自定义过滤器。
* **CSRF**：生成每会话令牌；在状态变更请求上验证。
* **XSS**：对输出进行 HTML 转义；设置 `Content-Security-Policy`。
* **点击劫持**：`X-Frame-Options: DENY` 或 CSP `frame-ancestors 'none'`。
* **CORS**：在过滤器中添加头部：

  ```java
  resp.setHeader("Access-Control-Allow-Origin", "https://example.com");
  resp.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE");
  resp.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  ```

# 16) 错误处理

* 在 `web.xml` 或通过框架映射错误页面：

```xml
<error-page>
  <error-code>404</error-code>
  <location>/WEB-INF/errors/404.jsp</location>
</error-page>
<error-page>
  <exception-type>java.lang.Throwable</exception-type>
  <location>/WEB-INF/errors/500.jsp</location>
</error-page>
```

* 在代码中，设置状态码并为 API 呈现一致的 JSON 错误模式。

# 17) 日志与可观测性

* 使用 `ServletContext#log`，或更好：SLF4J + Logback/Log4j2。
* 在过滤器中添加请求 ID（UUID）；包含在日志和响应头部中。
* 暴露健康端点；通过过滤器/Servlet 集成 Prometheus。

# 18) 打包与部署

**WAR 布局**：

```
myapp/
  WEB-INF/
    web.xml
    classes/            # 编译后的 .class 文件
    lib/                # 第三方 jar
  index.html
  static/...
```

使用 Maven/Gradle 构建，生成 **WAR**，部署到容器的 `webapps`（Tomcat）或通过管理控制台部署。对于嵌入式方式，使用 **Jetty** 或 **Tomcat 嵌入式** 并通过 `main()` 引导服务器。

# 19) 测试 Servlet

* **单元测试**：模拟 `HttpServletRequest/Response`。

  * 即使不使用 Spring，Spring 的 `org.springframework.mock.web.*` 也很方便。
  * 或使用 Mockito 创建自己的存根。
* **集成测试**：启动嵌入式 Jetty/Tomcat 并使用 HTTP 客户端（REST Assured/HttpClient）访问端点。
* **端到端测试**：使用浏览器自动化（Selenium/WebDriver）进行完整流程测试。

# 20) 性能提示

* 重用昂贵资源（通过 `DataSource` 的数据库连接池）；在 `destroy()` 中清理。
* 为静态内容设置缓存头部；将静态资源卸载到反向代理/CDN。
* 使用 GZIP 压缩（容器设置或过滤器）。
* 避免对长时间操作使用阻塞 I/O；考虑异步或队列。
* 分析内存分配和 GC；对大负载保持响应流式传输。

# 21) 常见陷阱

* **实例字段** 非线程安全 → 竞态条件。
* 在读取参数前忘记 `req.setCharacterEncoding("UTF-8")`。
* 无缓冲情况下两次读取正文。
* 未设置 `5xx` 状态就吞掉异常。
* 在同一响应中混用 `getWriter()` 和 `getOutputStream()`。

# 22) 从 `javax.servlet.*` 迁移到 `jakarta.servlet.*`

如果升级到 Jakarta EE 9+：

* 更改导入 `javax.servlet.*` → `jakarta.servlet.*`。
* 使用支持 Jakarta 的容器（Tomcat 10+、Jetty 11+）。
* 重新构建；大多数代码变更仅为导入重命名。
* 库也必须兼容 Jakarta（注意传递依赖项）。

# 23) 最小化 REST 风格示例

```java
@WebServlet(name="UsersApi", urlPatterns="/api/users/*")
public class UsersApi extends HttpServlet {
  @Override protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    resp.setContentType("application/json;charset=UTF-8");
    String id = pathParam(req, 1); // 例如 /api/users/42
    if (id == null) {
      resp.getWriter().write("[{\"id\":1,\"name\":\"A\"}]");
    } else {
      resp.getWriter().write("{\"id\":"+id+",\"name\":\"A\"}");
    }
  }
  private String pathParam(HttpServletRequest req, int idx) {
    String path = req.getPathInfo();        // "/42"
    if (path == null) return null;
    String[] parts = path.split("/");
    return parts.length > idx ? parts[idx] : null;
  }
}
```

# 24) 构建依赖（经典 `javax.servlet`）

Maven 中使用 **Provided** 范围，因为容器在运行时提供 API：

```xml
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>4.0.1</version>
  <scope>provided</scope>
</dependency>
```

对于 **Jakarta**：

```xml
<dependency>
  <groupId>jakarta.servlet</groupId>
  <artifactId>jakarta.servlet-api</artifactId>
  <version>6.0.0</version>
  <scope>provided</scope>
</dependency>
```

---

如果你告诉我目标容器（Tomcat/Jetty/Liberty）、Java 版本，以及你需要同步、异步还是非阻塞 I/O，我可以为你量身定制一个生产就绪的骨架（包含日志、CORS、安全头部和清晰的 Maven/Gradle 布局）——无需表格，只有紧凑的代码和步骤。
