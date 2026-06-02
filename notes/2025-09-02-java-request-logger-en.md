---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java Request Wrapper for Logging
translated: false
type: note
---

In Java web applications, you typically use a **`HttpServletRequestWrapper`** when you want to decorate or modify the behavior of the standard `HttpServletRequest` without touching the servlet container’s implementation.

### How `HttpServletRequestWrapper` works

* It’s a **decorator** around the original `HttpServletRequest`.
* You subclass `HttpServletRequestWrapper` and override methods such as `getInputStream()`, `getReader()`, or `getParameter()`.
* This is useful when you want to **read or cache the request body** (which by default can only be read once) or modify/query request parameters.

### Why you need it for logging

* By default, the servlet request body (`InputStream`) can be consumed only once. If you log it directly in a filter, the controller won’t be able to read it afterward.
* Wrapping allows you to **cache the body** so it can be read multiple times: once for logging, once for downstream processing.
* URL parameters can be logged by accessing `request.getParameterMap()` or `request.getQueryString()`.

---

### Example: Logging body and URL params

Here’s a filter using a custom wrapper:

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

Then use it in a filter:

```java
@WebFilter("/*")
public class LoggingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        CachedBodyHttpServletRequest wrappedRequest = new CachedBodyHttpServletRequest((HttpServletRequest) request);

        // Log URL
        String url = wrappedRequest.getRequestURL().toString();
        String query = wrappedRequest.getQueryString();

        // Log params
        Map<String, String[]> params = wrappedRequest.getParameterMap();

        // Log body
        String body = wrappedRequest.getBody();

        System.out.println("Request URL: " + url + (query != null ? "?" + query : ""));
        System.out.println("Parameters: " + params);
        System.out.println("Body: " + body);

        // Continue filter chain
        chain.doFilter(wrappedRequest, response);
    }
}
```

---

### Key Points

* **`HttpServletRequestWrapper`** lets you safely read the body multiple times.
* For URL parameters: `getParameterMap()` or `getQueryString()` is enough.
* Be cautious with **large bodies** (you may want streaming or size limits).
* In production, use a logging framework (SLF4J + Logback/Log4J2) instead of `System.out`.

---

Do you want me to also show you a **Spring Boot–style solution** (using `OncePerRequestFilter` and `ContentCachingRequestWrapper`), since that’s much simpler?
