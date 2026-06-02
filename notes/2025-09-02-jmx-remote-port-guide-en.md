---
audio: false
generated: true
image: false
lang: en
layout: post
title: JMX Remote Agent Port Guide
translated: false
type: note
---

The **JMX remote agent** is part of the Java Management Extensions (JMX) technology. It allows administrators or monitoring tools to connect to a running Java application from outside the JVM process, typically over TCP/IP. This is commonly used for monitoring, diagnostics, and management of Java applications in production.

Here’s a breakdown:

### 1. What JMX Remote Agent Is

* It exposes JVM internals (memory usage, thread activity, garbage collection, class loading, etc.) as *Managed Beans (MBeans)*.
* It lets you connect remotely (e.g., via **jconsole**, **VisualVM**, or monitoring tools like Prometheus exporters).
* It is usually enabled by JVM startup flags like:

  ```bash
  -Dcom.sun.management.jmxremote
  -Dcom.sun.management.jmxremote.port=9091
  -Dcom.sun.management.jmxremote.authenticate=false
  -Dcom.sun.management.jmxremote.ssl=false
  ```
* Once enabled, the JVM runs an RMI (Remote Method Invocation) connector server bound to the given port.

### 2. About Port 9091

* The number **9091** itself is not special; it’s just a TCP port you configure for JMX connections.
* Often admins pick 9091 (or 9010, 9999, etc.) for convenience and to avoid conflicts with standard ports.
* When listening on `9091`, the JVM will accept remote JMX connections on that port.
* If left unsecured (`authenticate=false, ssl=false`), anyone with network access can control or observe your JVM — which is a major security risk.

### 3. Typical Usage

* Monitoring with **JConsole**:

  ```bash
  jconsole host:9091
  ```
* Integrating with monitoring systems (e.g., Prometheus JMX Exporter).
* Remote management during troubleshooting (e.g., checking heap dumps, threads, GC behavior).

### 4. Security Considerations

* Always protect the JMX port with:

  * Network firewalls (restrict access).
  * Authentication (`password` and `access` files).
  * SSL if needed.
* Otherwise, exposing it on 9091 without security is equivalent to giving remote shell-level control of your JVM.

---

✅ In short: **JMX remote agent on port 9091** means your JVM is exposing a management and monitoring interface over TCP port 9091, which can be used by tools like JConsole or Prometheus, but must be secured.

Do you want me to show you the **exact JVM flags** to enable it with password authentication (instead of unsecured mode)?
