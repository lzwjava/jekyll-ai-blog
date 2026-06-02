---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote JMX Port 9001 Guide
translated: false
type: note
---

A **JMX remote agent** is part of Java Management Extensions (JMX). It allows you to monitor and manage a running Java application remotely. When you enable JMX remote management, the JVM starts an agent that exposes MBeans (Managed Beans) over a TCP port. Tools like **jconsole**, **VisualVM**, or custom monitoring software can connect to that port to inspect memory usage, thread states, GC activity, and even invoke operations.

About the **9001 port**:

* The actual port number depends on how the application is configured. Commonly you’ll see 9001, 9090, 9091, etc.
* If you see something listening on `9001` and it’s a **JMX remote agent**, it means some Java process started with system properties like:

  ```bash
  -Dcom.sun.management.jmxremote
  -Dcom.sun.management.jmxremote.port=9001
  -Dcom.sun.management.jmxremote.authenticate=false
  -Dcom.sun.management.jmxremote.ssl=false
  ```

This opens JMX on port `9001` without authentication/SSL (often only for internal or dev use, since it’s insecure if exposed publicly).

---

### How to check which program uses JMX port 9001 on Windows

1. Open **Command Prompt (as Administrator)**.
2. Run:

   ```cmd
   netstat -ano | findstr :9001
   ```

   This shows the PID (Process ID) bound to that port.
3. To identify the program:

   ```cmd
   tasklist /FI "PID eq <PID>"
   ```

   Replace `<PID>` with the number from step 2.

---

### How to stop / kill it

* If you confirm it’s a Java process you don’t want, kill it with:

  ```cmd
  taskkill /PID <PID> /F
  ```

* But if it’s part of your application server (Tomcat, WebSphere, Spring Boot app, etc.), better to stop it via its service/console instead of killing the process, so it shuts down cleanly.

---

👉 Do you want me to also show you how to **disable JMX remote agent** in a Java application so it doesn’t open port 9001 at all?
