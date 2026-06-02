---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: Spring Boot HTTP 请求日志记录过滤器
translated: true
type: note
---

以下是在 Spring（例如 Spring Boot 或 Spring MVC）中实现自定义 Servlet 过滤器以记录传入 HTTP 请求结构化数据的示例。该过滤器将捕获并记录：

- **HTTP 方法**：例如 GET、POST。
- **查询参数**：以映射形式提取。
- **请求体**：适用于 POST/PUT 等方法（注意：请求体是流，因此我们包装请求以便读取，同时不影响下游处理）。

日志输出将采用结构化 JSON 格式。我们将使用：
- **SLF4J** 进行日志记录（Spring 中常用）。
- **Jackson** 将数据序列化为 JSON（Spring Boot 默认包含）。
- 自定义 `HttpServletRequestWrapper` 以安全读取请求体。

该过滤器可全局注册以拦截所有请求。

### 步骤 1：依赖项
如果使用 Spring Boot，请确保在 `pom.xml`（Maven）或 `build.gradle`（Gradle）中包含以下内容：
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <!-- Jackson 已包含，但为清晰起见显式声明 -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
    </dependency>
</dependencies>
```

### 步骤 2：自定义请求包装器
该包装器允许多次读取请求体（通过将其缓存为字符串）。

```java
package com.example.filter;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.ReadListener;
import jakarta.servlet.ServletInputStream;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletRequestWrapper;
import org.springframework.util.StreamUtils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

public class ContentCachingRequestWrapper extends HttpServletRequestWrapper {
    private final byte[] cachedBody;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public ContentCachingRequestWrapper(HttpServletRequest request) throws IOException {
        super(request);
        InputStream requestInputStream = request.getInputStream();
        this.cachedBody = StreamUtils.copyToByteArray(requestInputStream);
    }

    @Override
    public ServletInputStream getInputStream() throws IOException {
        return new CachedServletInputStream(this.cachedBody);
    }

    @Override
    public BufferedReader getReader() throws IOException {
        byte[] requestBodyBytes = getRequestBody();
        return new BufferedReader(new InputStreamReader(new ByteArrayInputStream(requestBodyBytes),
                StandardCharsets.UTF_8));
    }

    public String getRequestBodyAsString() {
        if (cachedBody.length > 0) {
            return new String(cachedBody, StandardCharsets.UTF_8);
        }
        return "";
    }

    public byte[] getRequestBody() {
        return cachedBody;
    }

    // 辅助方法：将查询参数提取为映射
    public Map<String, String[]> getQueryParams() {
        Map<String, String[]> params = new LinkedHashMap<>();
        // 添加查询字符串参数
        String queryString = getQueryString();
        if (queryString != null) {
            // 简单解析；复杂情况可使用 Apache Commons 等库
            String[] pairs = queryString.split("&");
            for (String pair : pairs) {
                String[] keyValue = pair.split("=", 2);
                if (keyValue.length == 2) {
                    params.put(keyValue[0], new String[]{keyValue[1]});
                } else {
                    params.put(keyValue[0], new String[]{});
                }
            }
        }
        // 与参数映射合并
        params.putAll(getParameterMap());
        return params;
    }

    private static class CachedServletInputStream extends ServletInputStream {
        private final ByteArrayInputStream cachedBodyInputStream;

        public CachedServletInputStream(byte[] cachedBody) {
            this.cachedBodyInputStream = new ByteArrayInputStream(cachedBody);
        }

        @Override
        public boolean isFinished() {
            return cachedBodyInputStream.available() == 0;
        }

        @Override
        public boolean isReady() {
            return true;
        }

        @Override
        public void setReadListener(ReadListener readListener) {
            throw new UnsupportedOperationException();
        }

        @Override
        public int read() throws IOException {
            return cachedBodyInputStream.read();
        }
    }
}
```

### 步骤 3：自定义过滤器
该过滤器使用 SLF4J 将结构化数据记录为 JSON，适用于所有请求。

```java
package com.example.filter;

import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.util.StreamUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Component
public class LoggingFilter extends OncePerRequestFilter {

    private static final Logger logger = LoggerFactory.getLogger(LoggingFilter.class);
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        // 仅对具有请求体的方法（如 POST、PUT）包装请求
        ContentCachingRequestWrapper wrappedRequest = null;
        String body = "";
        if ("GET".equalsIgnoreCase(request.getMethod()) == false) {
            wrappedRequest = new ContentCachingRequestWrapper(request);
            body = wrappedRequest.getRequestBodyAsString();
        } else {
            wrappedRequest = new ContentCachingRequestWrapper(request);
        }

        // 构建结构化数据映射
        Map<String, Object> logData = new HashMap<>();
        logData.put("httpMethod", request.getMethod());
        logData.put("requestUri", request.getRequestURI());
        logData.put("queryParams", wrappedRequest.getQueryParams());
        logData.put("requestBody", body); // 仅对 POST 类方法非空

        // 记录为 JSON
        String jsonLog = objectMapper.writeValueAsString(logData);
        logger.info("传入请求: {}", jsonLog);

        // 继续处理包装后的请求
        filterChain.doFilter(wrappedRequest != null ? wrappedRequest : request, response);
    }
}
```

### 步骤 4：注册过滤器（在 Spring Boot 中自动注册）
在 Spring Boot 中，过滤器上的 `@Component` 注解会自动注册它。如果使用纯 Spring MVC（非 Boot），可以手动注册：

```java
// 在 @Configuration 类中
@Bean
public FilterRegistrationBean<LoggingFilter> loggingFilter() {
    FilterRegistrationBean<LoggingFilter> registrationBean = new FilterRegistrationBean<>();
    registrationBean.setFilter(new LoggingFilter());
    registrationBean.addUrlPatterns("/*"); // 应用于所有 URL
    registrationBean.setOrder(1);
    return registrationBean;
}
```

### 日志输出示例
当收到类似 `POST /api/users` 的请求，请求体为 `{"name": "John"}`，查询参数为 `?id=123` 时，日志将如下所示（假设日志记录器配置为 JSON 输出，例如通过 Logback 的 JSON 附加器）：

```json
{
  "httpMethod": "POST",
  "requestUri": "/api/users",
  "queryParams": {
    "id": ["123"]
  },
  "requestBody": "{\"name\": \"John\"}"
}
```

- **日志记录器配置**：要获取完整的 JSON 日志，请在 Logback（在 `logback-spring.xml` 或 `application.properties` 中）配置 JSON 编码器，例如 `net.logstash.logback.encoder.LogstashEncoder`。例如，在 `application.yml` 中：
  ```yaml
  logging:
    pattern:
      console: "%msg%n"  # 或使用 JSON 附加器进行结构化输出
  ```

### 注意事项
- **请求体读取限制**：我们仅读取非 GET 方法的请求体。对于 GET 方法，请求体为空。这避免了处理大请求体或多次读取的问题。
- **安全性**：注意记录敏感数据（如请求体/查询中的密码）。可能需要屏蔽某些字段。
- **性能**：缓存请求体会占用内存；对于非常大的请求体，请考虑限制（例如仅读取前 N 字节）。
- **测试**：将此添加到 Spring Boot 应用程序中，并通过 curl 发送 POST 请求：`curl -X POST http://localhost:8080/api/users?id=123 -d '{"name":"John"}' -H "Content-Type: application/json"`。
- **替代方案**：对于更高级的日志记录，请考虑使用 Spring Boot Actuator 或带有结构化日志记录的库，如 `spring-boot-starter-logging`。

这是一个生产就绪的起点。根据需要自定义！如果需要更多详细信息，请告知。
