---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java Servlet API Guide Essentials
translated: false
type: note
---

Here’s a practical, end-to-end guide to the Java **Servlet** API in the classic **`javax.servlet.*`** namespace (Servlet 2.x–4.x era). I’ll also note what changed after the move to **`jakarta.servlet.*`** so you’re future-proof.

# 1) What is a Servlet?

A **Servlet** is a Java class that runs inside a **Servlet container** (Tomcat, Jetty, WebSphere, WebLogic, etc.) and handles HTTP requests/responses. The container manages:

* Lifecycle (loading, init, service, destroy)
* Multithreading and request routing
* Sessions, security, resources, and configuration

# 2) Core Packages & Key Interfaces (javax.\*)

* `javax.servlet.Servlet`, `ServletConfig`, `ServletContext`
* `javax.servlet.http.HttpServlet`, `HttpServletRequest`, `HttpServletResponse`, `HttpSession`, `Cookie`
* `javax.servlet.Filter`, `FilterChain`, `FilterConfig`
* `javax.servlet.ServletRequestListener` and other listeners
* `javax.servlet.annotation.*` (since 3.0: `@WebServlet`, `@WebFilter`, `@WebListener`, `@MultipartConfig`)
* Since 3.0: **async** (`AsyncContext`), programmatic registration
* Since 3.1: **non-blocking I/O** (`ServletInputStream`/`ServletOutputStream` with `ReadListener`/`WriteListener`)
* Since 4.0: HTTP/2 support (e.g., `PushBuilder`)

> Jakarta switch: starting **Servlet 5.0** (Jakarta EE 9), the packages renamed to `jakarta.servlet.*`. Most APIs are the same; update imports and dependencies when migrating.

# 3) Servlet Lifecycle & Threading Model

* **Load**: Container loads class, creates a single instance per declaration.
* **`init(ServletConfig)`**: Called once. Read init params, cache heavy resources.
* **`service(req, res)`**: Called per request. `HttpServlet` dispatches to `doGet`, `doPost`, etc.
* **`destroy()`**: Called once on shutdown/redeploy.

**Threading**: The container calls `service` concurrently on the same instance.
**Rule**: Avoid mutable instance fields; if you must, use thread-safe structures or proper synchronization. Prefer locals.

# 4) Minimal Servlet (annotations)

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

# 5) `web.xml` vs Annotations

**Annotations (3.0+)** are easiest for simple apps.
**`web.xml`** still useful for ordering, overrides, or legacy containers.

Minimal `web.xml`:

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

# 6) The HTTP Request/Response Essentials

## Reading request data

```java
String q = req.getParameter("q");        // query/form field
Enumeration<String> names = req.getParameterNames();
BufferedReader reader = req.getReader(); // raw body text
ServletInputStream in = req.getInputStream(); // binary body
String header = req.getHeader("X-Token");
```

**Tip**: Always set encoding before reading params:

```java
req.setCharacterEncoding("UTF-8");
```

## Writing responses

```java
resp.setStatus(HttpServletResponse.SC_OK);
resp.setContentType("application/json;charset=UTF-8");
resp.setHeader("Cache-Control", "no-store");
try (PrintWriter out = resp.getWriter()) {
  out.write("{\"ok\":true}");
}
```

# 7) doGet vs doPost vs others

* `doGet`: idempotent reads; use query string.
* `doPost`: create/update with form or JSON body.
* `doPut`/`doDelete`/`doPatch`: RESTful semantics (client must support).
* Always validate inputs and handle content types explicitly.

# 8) Sessions & Cookies

```java
HttpSession session = req.getSession(); // creates if absent
session.setAttribute("userId", 123L);
Long userId = (Long) session.getAttribute("userId");
session.invalidate(); // logout
```

Configure session cookie flags via container or programmatically:

* `HttpOnly` (protect from JS), `Secure` (HTTPS), `SameSite=Lax/Strict`
  Consider stateless tokens for horizontal scaling; else use sticky sessions or external session store.

# 9) Filters (cross-cutting concerns)

Use **Filters** for logging, auth, CORS, compression, encoding, etc.

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

# 10) Listeners (app & request hooks)

Common ones:

* `ServletContextListener`: app startup/shutdown (init pools, warm caches)
* `HttpSessionListener`: create/destroy sessions (metrics, cleanup)
* `ServletRequestListener`: per-request hooks (trace ids)

Example:

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

# 11) Async & Non-Blocking I/O

## Async (Servlet 3.0)

Allows freeing container threads while a backend call runs.

```java
@WebServlet(urlPatterns="/async", asyncSupported=true)
public class AsyncDemo extends HttpServlet {
  protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
    AsyncContext ctx = req.startAsync();
    ctx.start(() -> {
      try {
        // call slow service...
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

## Non-blocking (Servlet 3.1)

Register `ReadListener`/`WriteListener` on the streams for event-driven I/O. Useful for streaming large bodies without blocking threads.

# 12) File Uploads (Multipart)

```java
import javax.servlet.annotation.MultipartConfig;

@MultipartConfig(maxFileSize = 10 * 1024 * 1024)
@WebServlet("/upload")
public class UploadServlet extends HttpServlet {
  protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException, ServletException {
    Part file = req.getPart("file");
    String filename = file.getSubmittedFileName();
    try (InputStream is = file.getInputStream()) {
      // save...
    }
    resp.getWriter().println("Uploaded " + filename);
  }
}
```

Make sure the client sends `Content-Type: multipart/form-data`.

# 13) Dispatching & Templating

* **Forward**: server-side internal dispatch; original URL remains.

  ```java
  req.getRequestDispatcher("/WEB-INF/view.jsp").forward(req, resp);
  ```
* **Include**: include output of another resource.

  ```java
  req.getRequestDispatcher("/fragment").include(req, resp);
  ```
* **Redirect**: client 302/303/307 to new URL.

  ```java
  resp.sendRedirect(req.getContextPath() + "/login");
  ```

# 14) Character Encoding & i18n

A tiny **encoding filter** prevents mojibake:

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

Use `Locale` from `HttpServletRequest#getLocale()` and resource bundles for i18n.

# 15) Security Basics

* **Transport**: always HTTPS; set `Secure` cookies.
* **Auth**: container-managed (FORM/BASIC/DIGEST), or custom filter with JWT/session.
* **CSRF**: generate per-session token; validate on state-changing requests.
* **XSS**: HTML-escape outputs; set `Content-Security-Policy`.
* **Clickjacking**: `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'`.
* **CORS**: add headers in a filter:

  ```java
  resp.setHeader("Access-Control-Allow-Origin", "https://example.com");
  resp.setHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE");
  resp.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  ```

# 16) Error Handling

* Map error pages in `web.xml` or via framework:

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

* In code, set status codes and render a consistent JSON error schema for APIs.

# 17) Logging & Observability

* Use `ServletContext#log`, or better: SLF4J + Logback/Log4j2.
* Add a request-ID (UUID) in a filter; include in logs and response headers.
* Expose health endpoints; integrate with Prometheus via a filter/servlet.

# 18) Packaging & Deployment

**WAR layout**:

```
myapp/
  WEB-INF/
    web.xml
    classes/            # compiled .class files
    lib/                # third-party jars
  index.html
  static/...
```

Build with Maven/Gradle, produce a **WAR**, deploy to the container’s `webapps` (Tomcat) or via admin console. For embedded style, use **Jetty** or **Tomcat embedded** with a `main()` bootstrapping the server.

# 19) Testing Servlets

* **Unit**: mock `HttpServletRequest/Response`.

  * Spring’s `org.springframework.mock.web.*` is convenient even without Spring.
  * Or Mockito your own stubs.
* **Integration**: start embedded Jetty/Tomcat and hit endpoints with HTTP client (REST Assured/HttpClient).
* **End-to-End**: browser automation (Selenium/WebDriver) for full flows.

# 20) Performance Tips

* Reuse expensive resources (DB pools via `DataSource`); clean up in `destroy()`.
* Set caching headers for static content; offload static assets to a reverse proxy/CDN.
* Use GZIP compression (container setting or a filter).
* Avoid blocking I/O for long operations; consider async or queueing.
* Profile allocations and GC; keep responses streaming for large payloads.

# 21) Common Pitfalls

* **Instance fields** not thread-safe → race conditions.
* Forgetting `req.setCharacterEncoding("UTF-8")` before reading params.
* Reading the body twice without buffering.
* Swallowing exceptions without setting `5xx` status.
* Mixing `getWriter()` and `getOutputStream()` in the same response.

# 22) From `javax.servlet.*` to `jakarta.servlet.*`

If/when you upgrade to Jakarta EE 9+:

* Change imports `javax.servlet.*` → `jakarta.servlet.*`.
* Use a container that supports Jakarta (Tomcat 10+, Jetty 11+).
* Rebuild; most code changes are import renames.
* Libraries must also be Jakarta-compatible (watch transitive dependencies).

# 23) Minimal REST-style Example

```java
@WebServlet(name="UsersApi", urlPatterns="/api/users/*")
public class UsersApi extends HttpServlet {
  @Override protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
    resp.setContentType("application/json;charset=UTF-8");
    String id = pathParam(req, 1); // e.g. /api/users/42
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

# 24) Build Dependencies (classic `javax.servlet`)

**Provided** scope in Maven because the container supplies the API at runtime:

```xml
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>4.0.1</version>
  <scope>provided</scope>
</dependency>
```

For **Jakarta**:

```xml
<dependency>
  <groupId>jakarta.servlet</groupId>
  <artifactId>jakarta.servlet-api</artifactId>
  <version>6.0.0</version>
  <scope>provided</scope>
</dependency>
```

---

If you tell me your target container (Tomcat/Jetty/Liberty), Java version, and whether you want synchronous, async, or non-blocking I/O, I can sketch a production-ready skeleton tailored to your stack (logging, CORS, security headers, and a clean Maven/Gradle layout) — no tables, just tight code and steps.
