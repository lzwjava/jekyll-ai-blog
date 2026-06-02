---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Java请求日志记录封装器
translated: true
type: note
---

在 Java Web 应用程序中，当你需要装饰或修改标准 `HttpServletRequest` 的行为而不触及 Servlet 容器的实现时，通常会使用 **`HttpServletRequestWrapper`**。

### `HttpServletRequestWrapper` 的工作原理

* 它是原始 `HttpServletRequest` 的**装饰器**
* 你可以继承 `HttpServletRequestWrapper` 并重写诸如 `getInputStream()`、`getReader()` 或 `getParameter()` 等方法
* 这在需要**读取或缓存请求体**（默认只能读取一次）或修改/查询请求参数时非常有用

### 为何需要它来实现日志记录

* 默认情况下，Servlet 请求体（`InputStream`）只能被消费一次。如果在过滤器中直接记录它，控制器后续将无法读取
* 包装机制允许你**缓存请求体**，从而支持多次读取：一次用于日志记录，一次用于下游处理
* 可通过访问 `request.getParameterMap()` 或 `request.getQueryString()` 记录 URL 参数

---

### 示例：记录请求体和 URL 参数

以下是一个使用自定义包装器的过滤器：

```java
public class CachedBodyHttpServletRequest extends HttpServletRequestWrapper {
    private byte[] cachedBody;

    public CachedBodyHttpServletRequest(HttpServletRequest request) throws IOException {
        super(request);
        InputStream requestInputStream = request.getInputStream();
        this.cachedBody = requestInputStream.readAllBytes();
    }

    @Override
    public ServletInputStream getInputStream() {
        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(this.cachedBody);
        return new ServletInputStream() {
            @Override
            public int read() {
                return byteArrayInputStream.read();
            }
            @Override
            public boolean isFinished() {
                return byteArrayInputStream.available() == 0;
            }
            @Override
            public boolean isReady() {
                return true;
            }
            @Override
            public void setReadListener(ReadListener readListener) {}
        };
    }

    @Override
    public BufferedReader getReader() {
        return new BufferedReader(new InputStreamReader(this.getInputStream()));
    }

    public String getBody() {
        return new String(this.cachedBody, StandardCharsets.UTF_8);
    }
}
```

在过滤器中的使用示例：

```java
@WebFilter("/*")
public class LoggingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        CachedBodyHttpServletRequest wrappedRequest = new CachedBodyHttpServletRequest((HttpServletRequest) request);

        // 记录 URL
        String url = wrappedRequest.getRequestURL().toString();
        String query = wrappedRequest.getQueryString();

        // 记录参数
        Map<String, String[]> params = wrappedRequest.getParameterMap();

        // 记录请求体
        String body = wrappedRequest.getBody();

        System.out.println("请求 URL: " + url + (query != null ? "?" + query : ""));
        System.out.println("参数: " + params);
        System.out.println("请求体: " + body);

        // 继续过滤器链
        chain.doFilter(wrappedRequest, response);
    }
}
```

---

### 关键要点

* **`HttpServletRequestWrapper`** 允许安全地多次读取请求体
* 对于 URL 参数：使用 `getParameterMap()` 或 `getQueryString()` 即可满足需求
* 注意处理**大体积请求体**（可能需要流式处理或设置大小限制）
* 在生产环境中，应使用日志框架（SLF4J + Logback/Log4J2）替代 `System.out`

---

需要我继续展示 **Spring Boot 风格的解决方案**吗（使用 `OncePerRequestFilter` 和 `ContentCachingRequestWrapper`）？这种实现方式会更加简洁。
