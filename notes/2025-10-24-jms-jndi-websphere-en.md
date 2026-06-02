---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: JMS and JNDI APIs for WebSphere
translated: false
type: note
---

### Required Packages and APIs for JMS in Java

To use the JMS code snippet you referenced (for looking up and connecting to a JMS Connection Factory in IBM WebSphere Application Server), you'll need to import the relevant Java packages. These are standard APIs from the Java EE/Jakarta EE ecosystem:

- **JNDI (Java Naming and Directory Interface)**: For the `InitialContext` lookup.
  - Package: `javax.naming` (or `jakarta.naming` in newer Jakarta EE versions).
  - Key class: `InitialContext` – This is the starting point for JNDI operations. It provides a context for looking up resources (like JMS factories or queues) by their JNDI names (e.g., `"jms/MyConnectionFactory"`). In a container like WAS, it automatically connects to the server's naming service.

- **JMS (Java Message Service) API**: For creating connections, sessions, senders/receivers, and messages.
  - Package: `javax.jms` (JMS 1.1/2.0) or `jakarta.jms` (Jakarta JMS 3.0+ in modern EE).
  - Key interfaces: `QueueConnectionFactory`, `QueueConnection`, `QueueSession`, `QueueSender`, `Queue`, `TextMessage`, etc.

Example imports at the top of your Java class:

```java
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.jms.QueueConnectionFactory;
import javax.jms.QueueConnection;
import javax.jms.QueueSession;
import javax.jms.Queue;
import javax.jms.QueueSender;
import javax.jms.TextMessage;
import javax.jms.JMSException;
```

**What is `InitialContext`?**
It's a class in the JNDI API that acts as an entry point to a naming service. In your code:

```java
InitialContext ctx = new InitialContext();  // Creates a default context tied to the app server's JNDI environment
QueueConnectionFactory qcf = (QueueConnectionFactory) ctx.lookup("jms/MyConnectionFactory");  // Looks up the pre-configured factory by its JNDI name
```

No properties are needed in the constructor for apps running *inside* WAS, as the container injects the environment (e.g., via `java.naming.factory.initial`). If running a standalone client *outside* WAS, you'd pass a `Hashtable` with properties like the provider URL.

### Maven Dependencies (pom.xml)

If your Java app is **deployed and running inside WAS** (e.g., as a web app, EJB, or enterprise bean):

- **No extra dependencies needed**. WAS provides the JMS and JNDI APIs out-of-the-box as part of its Java EE runtime. Just compile against them (they're on the classpath during build/deploy).
- In `pom.xml`, you can explicitly declare them with `<scope>provided</scope>` to avoid bundling them in your WAR/EAR (keeps it lightweight):

  ```xml
  <dependencies>
      <dependency>
          <groupId>javax.jms</groupId>  <!-- Or jakarta.jms for newer versions -->
          <artifactId>javax.jms-api</artifactId>
          <version>2.0.1</version>  <!-- JMS 2.0, compatible with WAS 8.5+ -->
          <scope>provided</scope>
      </dependency>
      <dependency>
          <groupId>javax.naming</groupId>
          <artifactId>javax.naming-api</artifactId>
          <version>1.0</version>  <!-- JNDI 1.0, standard -->
          <scope>provided</scope>
      </dependency>
  </dependencies>
  ```

If your app is a **standalone client** (running outside WAS, e.g., a thin client connecting to the server):

- You'll need the **WebSphere Application Client** libraries for full JMS support over IIOP. Download the "IBM WebSphere Application Server traditional" client package from IBM, then add it to your classpath.
- In `pom.xml`, include:

  ```xml
  <dependency>
      <groupId>com.ibm.ws</groupId>
      <artifactId>was-jms-client</artifactId>  <!-- Approximate; use IBM's Maven repo if available -->
      <version>9.0.5</version>  <!-- Match your WAS version -->
  </dependency>
  ```

  Or use the full thin client JARs (e.g., `com.ibm.ws.orb_8.5.5.jar`, `com.ibm.ws.jndi_*.jar`). Check IBM docs for the exact setup.

For Jakarta EE migration (post-2020), switch to `jakarta.*` packages, but WAS 9.x still uses `javax.*` by default—enable Jakarta via feature packs if needed.

[IBM WebSphere JMS API Documentation](https://www.ibm.com/docs/en/was/9.0.5?topic=resources-jms-api)
[Java EE JNDI Tutorial](https://docs.oracle.com/javase/tutorial/jndi/)
