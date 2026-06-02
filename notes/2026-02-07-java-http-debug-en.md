---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Java HTTP Debugging Options
translated: false
type: note
---

In Java, there isn't a direct equivalent to Node.js's `NODE_DEBUG` environment variable, but there are several ways to enable debugging output for HTTP/HTTPS connections:

## 1. **System Properties (Most Common)**

```bash
# Enable all SSL/TLS debugging
java -Djavax.net.debug=all MyApp

# Enable only SSL handshake debugging
java -Djavax.net.debug=ssl:handshake MyApp

# Enable HTTP protocol debugging
java -Djava.net.debug=true MyApp
```

## 2. **HTTP Client Logging (Java 11+)**

For the modern `java.net.http.HttpClient`, you can enable logging:

```bash
java -Djdk.httpclient.HttpClient.log=all MyApp
```

Or programmatically:
```java
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .build();
```

Then configure logging in your logging framework (like java.util.logging).

## 3. **Apache HttpClient (if using that library)**

Add to your `log4j.properties` or `logback.xml`:
```properties
log4j.logger.org.apache.http=DEBUG
log4j.logger.org.apache.http.wire=DEBUG
```

## 4. **Common javax.net.debug Options**

```bash
# All debugging
-Djavax.net.debug=all

# SSL/TLS only
-Djavax.net.debug=ssl

# SSL handshake and session
-Djavax.net.debug=ssl:handshake:session

# Key manager
-Djavax.net.debug=ssl:keymanager

# Trust manager
-Djavax.net.debug=ssl:trustmanager
```

The closest equivalent to `NODE_DEBUG=http,https` would be:
```bash
java -Djavax.net.debug=all -Djdk.httpclient.HttpClient.log=all MyApp
```

This gives you detailed information about SSL/TLS connections and HTTP client operations, similar to what Node.js provides.
