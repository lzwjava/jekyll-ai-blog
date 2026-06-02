---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: IBM WebSphere Request Routing Explained
translated: false
type: note
---

Let me explain how IBM WebSphere Application Server (WAS) handles incoming requests and routing:

## Request Flow in IBM WAS

When a request comes to IBM WAS, here's the typical flow:

**1. Web Server Layer (Optional)**
- Request first hits IBM HTTP Server (IHS) or another web server
- Web server plugin routes to appropriate WAS instance

**2. Web Container Entry Point**
The request enters WAS through the **Web Container**, which is part of the main servlet engine. The key package structure is:

```
com.ibm.ws.webcontainer.*
```

**3. Request Processing Chain**

The routing happens through several components:

**Transport Channel Framework**
- `com.ibm.ws.channel.*` - handles network communication
- HTTP transport channels receive the request

**Web Container Processing**
```
com.ibm.ws.webcontainer.servlet.ServletWrapper
com.ibm.ws.webcontainer.filter.WebAppFilterManager
```

**4. Filter Chain Execution**

Filters work exactly like standard Java Servlet filters but managed by WAS:

- **Defined in web.xml** of your application
- Filters are chained in the order specified
- Each filter can inspect/modify request and response
- Uses standard `javax.servlet.Filter` interface

```xml
<filter>
    <filter-name>MyFilter</filter-name>
    <filter-class>com.example.MyFilter</filter-class>
</filter>

<filter-mapping>
    <filter-name>MyFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

**Filter execution order:**
1. WAS loads filter configurations at application startup
2. WebAppFilterManager creates filter chain
3. On each request: Request → Filter1 → Filter2 → ... → Servlet

## Main Packages in IBM WAS

**Core packages:**
- `com.ibm.ws.webcontainer.*` - Web container implementation
- `com.ibm.ws.runtime.*` - Runtime services
- `com.ibm.websphere.servlet.*` - WAS-specific servlet extensions
- `com.ibm.ws.channel.*` - Transport layer
- `com.ibm.ejs.*` - EJB container services
- `com.ibm.ws.naming.*` - JNDI implementation

## Routing Mechanism

**Virtual Host Routing:**
- Configured in WAS admin console
- Maps `hostname:port` combinations to applications
- Configuration: `VirtualHost → Host Aliases → Applications`

**Context Root Routing:**
- Each application has a context root (e.g., `/myapp`)
- WAS maintains a registry of deployed applications
- URI mapping: `http://server:port/contextRoot/servletPath`

**Servlet Mapping:**
- Defined in web.xml or annotations
- Pattern matching (exact, path, extension, default)

## Application Startup Sequence

When application starts:
1. **ClassLoader initialization** - App gets its own classloader
2. **web.xml parsing** - Filters, servlets, listeners loaded
3. **ServletContextListeners fire** - `contextInitialized()`
4. **Filters instantiated** - `init()` method called
5. **Load-on-startup servlets** - Initialize eager servlets
6. **Application marked STARTED** - Ready to accept requests

The routing registry is updated, and the application is now available at its context root.

Does this clarify how WAS handles request routing and filtering?
