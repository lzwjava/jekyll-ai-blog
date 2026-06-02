---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Spring Boot HTTP Request Logging Filter
translated: false
type: note
---

Below is an example of how to implement a custom Servlet Filter in Spring (e.g., Spring Boot or Spring MVC) to log structured data from incoming HTTP requests. This filter will capture and log:

- **HTTP Method**: e.g., GET, POST.
- **Query Parameters**: Extracted as a map.
- **Request Body**: For methods like POST/PUT (note: the body is a stream, so we wrap the request to read it without consuming it for downstream processing).

The log output will be in structured JSON format. We'll use:
- **SLF4J** for logging (common in Spring).
- **Jackson** to serialize the data to JSON (Spring Boot includes it by default).
- A custom `HttpServletRequestWrapper` to safely read the body.

This filter can be registered globally to intercept all requests.

### Step 1: Dependencies
If using Spring Boot, ensure these are in your `pom.xml` (Maven) or `build.gradle` (Gradle):
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <!-- Jackson is included, but explicitly for clarity -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
    </dependency>
</dependencies>
```

### Step 2: Custom Request Wrapper
This wrapper allows reading the request body multiple times (by caching it as a string).

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

    // Helper to extract query params as a map
    public Map<String, String[]> getQueryParams() {
        Map<String, String[]> params = new LinkedHashMap<>();
        // Add query string params
        String queryString = getQueryString();
        if (queryString != null) {
            // Simple parsing; for complex cases, use libraries like Apache Commons
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
        // Merge with parameter map
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

### Step 3: The Custom Filter
This filter logs the structured data as JSON using SLF4J. It's applied to all requests.

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

        // Wrap the request only for methods that have a body (e.g., POST, PUT)
        ContentCachingRequestWrapper wrappedRequest = null;
        String body = "";
        if ("GET".equalsIgnoreCase(request.getMethod()) == false) {
            wrappedRequest = new ContentCachingRequestWrapper(request);
            body = wrappedRequest.getRequestBodyAsString();
        } else {
            wrappedRequest = new ContentCachingRequestWrapper(request);
        }

        // Build structured data map
        Map<String, Object> logData = new HashMap<>();
        logData.put("httpMethod", request.getMethod());
        logData.put("requestUri", request.getRequestURI());
        logData.put("queryParams", wrappedRequest.getQueryParams());
        logData.put("requestBody", body); // Only non-empty for POST-like methods

        // Log as JSON
        String jsonLog = objectMapper.writeValueAsString(logData);
        logger.info("Incoming Request: {}", jsonLog);

        // Proceed with the wrapped request
        filterChain.doFilter(wrappedRequest != null ? wrappedRequest : request, response);
    }
}
```

### Step 4: Register the Filter (Automatic in Spring Boot)
In Spring Boot, the `@Component` annotation on the filter automatically registers it. If you're using plain Spring MVC (not Boot), you can register it manually:

```java
// In a @Configuration class
@Bean
public FilterRegistrationBean<LoggingFilter> loggingFilter() {
    FilterRegistrationBean<LoggingFilter> registrationBean = new FilterRegistrationBean<>();
    registrationBean.setFilter(new LoggingFilter());
    registrationBean.addUrlPatterns("/*"); // Apply to all URLs
    registrationBean.setOrder(1);
    return registrationBean;
}
```

### Example Log Output
When a request like `POST /api/users` with body `{"name": "John"}` and query `?id=123` comes in, the log will look like this (assuming your logger is configured for JSON output, e.g., via Logback with JSON appender):

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

- **Logger Configuration**: To get full JSON logs, configure Logback (in `logback-spring.xml` or `application.properties`) with a JSON encoder like `net.logstash.logback.encoder.LogstashEncoder`. For example, in `application.yml`:
  ```yaml
  logging:
    pattern:
      console: "%msg%n"  # Or use a JSON appender for structured output
  ```

### Notes
- **Body Reading Limitation**: We only read the body for non-GET methods. For GET, it's empty. This avoids issues with large bodies or multiple reads.
- **Security**: Be cautious logging sensitive data (e.g., passwords in body/query). You might want to mask fields.
- **Performance**: Caching the body uses memory; for very large bodies, consider limits (e.g., read only first N bytes).
- **Testing**: Add this to a Spring Boot app and send a POST request via curl: `curl -X POST http://localhost:8080/api/users?id=123 -d '{"name":"John"}' -H "Content-Type: application/json"`.
- **Alternatives**: For more advanced logging, consider Spring Boot Actuator or libraries like `spring-boot-starter-logging` with structured logging.

This is a production-ready starting point. Customize as needed! If you need more details, let me know.
