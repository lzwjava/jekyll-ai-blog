---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spring Session, JSESSIONID, and Server Detection
translated: false
type: note
---

Let’s break this into two parts: how **Spring Session/JSESSIONID** works, and how to tell whether Spring is running on **Tomcat or Netty**.

---

## 1. How Spring Session and `JSESSIONID` Work

* **JSESSIONID** is the standard HTTP session identifier used by servlet containers (Tomcat, Jetty, Undertow, etc.).
* When a client makes the first request that requires a session, the container (or Spring Session if you use it) generates a random session ID, stores session data on the server, and sends the ID back to the client in a `Set-Cookie` header.
* The client includes this `JSESSIONID` cookie on subsequent requests, allowing the server to find the correct session.
* By default, the session data is stored **in the servlet container’s memory**. For example:

  * Tomcat stores sessions in memory (unless you configure persistence).
  * If you use **Spring Session**, session storage can be externalized (Redis, JDBC, Hazelcast, etc.), while still using the `JSESSIONID` cookie to identify users.
* Spring Security and other Spring features rely on this session mechanism for authentication and state management.

---

## 2. How to Know Whether Spring Uses Tomcat or Netty

Spring Boot can run with different embedded servers:

* **Tomcat** (default for Spring Boot starter-web)
* **Jetty** (if you swap dependencies)
* **Undertow** (alternative servlet container)
* **Netty** (used by Spring WebFlux, not servlet-based)

### Ways to Check:

1. **Look at your dependencies**

   * If your `pom.xml` or `build.gradle` includes `spring-boot-starter-web`, it uses **Tomcat** by default.
   * If it includes `spring-boot-starter-webflux`, it uses **Netty** by default.

2. **Check startup logs**

   * When the app starts, Spring Boot logs the embedded server.
   * Example (Tomcat):

     ```
     Tomcat started on port(s): 8080 (http)
     ```
   * Example (Netty):

     ```
     Netty started on port(s): 8080
     ```

3. **Check runtime classes**

   * In code or via actuator, check what server classes are loaded.
   * Tomcat classes start with `org.apache.catalina.`
   * Netty classes start with `io.netty.`

---

✅ **Summary**:

* `JSESSIONID` is just the cookie pointing to a server-side session, managed by Tomcat (default) or by Spring Session (Redis/DB).
* You can tell whether Spring uses **Tomcat or Netty** by checking dependencies, startup logs, or runtime classes.

---

Do you want me to also explain **how session handling differs between Spring MVC (Tomcat) and Spring WebFlux (Netty)**? That’s where the distinction matters most.
