---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: "Request Filter Comparison: WebSphere vs Spring Boot"
translated: false
type: note
---

### Overview

Both IBM WebSphere Application Server (WAS, traditional or Liberty) and Spring Boot support the concept of a **request processing chain** based on the standard Java Servlet API's `javax.servlet.Filter` and `FilterChain`. This is where incoming HTTP requests pass through a series of filters before reaching servlets (or controllers/handlers), and responses can be modified on the way back.

- Filters allow pre-processing (e.g., authentication, logging, compression) and post-processing of requests/responses.
- The core mechanism — implementing `Filter`, calling `chain.doFilter(request, response)` to proceed — is **identical** because both run in a Servlet container (WAS has its own full Java EE web container; Spring Boot embeds Tomcat/Jetty/Undertow by default).

There is no fundamental difference in how a basic "request chain filter" works. However, the way you configure, order, and integrate filters differs significantly due to the architecture of each platform.

### Key Comparison

| Aspect                  | IBM WebSphere Application Server (Traditional/Liberty) | Spring Boot |
|-------------------------|---------------------------------------------------------|-------------|
| **Underlying Mechanism** | Standard Servlet filters (`javax.servlet.Filter`). WAS also has proprietary extensions like `ChainedRequest`/`ChainedResponse` for internal request forwarding/chaining in some scenarios (e.g., portal or custom IBM APIs). | Standard Servlet filters. Spring Boot auto-registers any `@Component` Filter bean or you explicitly register via `FilterRegistrationBean`. |
| **Configuration**       | Primarily via `web.xml` (declarative) or programmatic registration. For global filters (across all apps): complex — requires shared libraries, custom listeners, or IBM-specific extensions (no simple server-wide web.xml like Tomcat). | Convention-over-configuration: Annotate with `@Component` + `@Order` for automatic registration, or use `FilterRegistrationBean` for fine control (URL patterns, dispatcher types). Very developer-friendly. |
| **Ordering**            | Defined in `web.xml` order or via `@Order` if programmatic. Global ordering is tricky. | Easy with `@Order(n)` (lower = earlier) or `Ordered` interface. Spring Boot manages the chain automatically. |
| **Security Filter Chain** | Uses standard Servlet filters or IBM-specific security (e.g., TAI, JEE roles). No built-in security chain like Spring Security. | Spring Security provides a powerful `SecurityFilterChain` (via `FilterChainProxy`) with 15+ ordered filters (CSRF, authentication, session management, etc.). Highly customizable with multiple chains per path. |
| **Ease of Adding Custom Filters** | More verbose, especially for global/cross-app filters. Often requires admin console tweaks or shared libs. | Extremely simple — just a `@Component` bean or config class. Auto-integrated into the embedded container. |
| **Deployment Model**    | Traditional full Java EE server. Apps deployed as WAR/EAR. Supports heavy enterprise features (clustering, transactions, JMS). | Embedded container (standalone executable JAR by default). Can deploy as WAR to external servers (including WAS). Lightweight/microservices-oriented. |
| **Performance/Overhead**| Higher overhead (full app server). Transport chains, web container channels add layers. | Lower overhead (embedded lightweight container). Faster startup, less resource use. |
| **When Filters Run**     | In WAS web container inbound chain. Can have server-level transport filters (e.g., IP filtering on TCP channels). | In the embedded container's filter chain. Spring Boot adds its own filters (error handling, character encoding, etc.). |
| **Common Use Cases**    | Enterprise monoliths, portals, legacy Java EE apps needing global security/logging. | Modern microservices, REST APIs, rapid development with Spring Security. |

### Practical Examples

**Standard Custom Filter (same code works in both):**

```java
@Component  // Spring Boot only; in WAS declare in web.xml
@Order(1)
public class LoggingFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        System.out.println("Request: " + ((HttpServletRequest) req).getRequestURI());
        chain.doFilter(req, res);  // Critical: passes to next filter/servlet
    }
    // init/destroy...
}
```

**In Spring Boot (auto-registered):**
Just the class above + `@Component`.

**In WAS:**
Add to `web.xml`:

```xml
<filter>
    <filter-name>LoggingFilter</filter-name>
    <filter-class>com.example.LoggingFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>LoggingFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

### When to Choose Which

- **Use WAS filters** if you are in a legacy IBM environment, need full Java EE features, or must apply filters globally across many apps without code changes.
- **Use Spring Boot filters** (especially with Spring Security) for new/greenfield projects, microservices, fast iteration, or when you want multiple security chains and easy ordering.

In summary, the **request chain filter concept is the same** (Servlet spec), but **Spring Boot makes it far simpler and more powerful** for most modern use cases, while WAS is more enterprise-heavy and configuration-intensive.

[IBM WAS Servlet Filtering Documentation](https://www.ibm.com/docs/en/was/9.0.5?topic=extensions-servlet-filtering)
[Spring Boot Custom Filters](https://www.baeldung.com/spring-boot-add-filter)
[Spring Security Filter Chain](https://docs.spring.io/spring-security/reference/servlet/architecture.html)
