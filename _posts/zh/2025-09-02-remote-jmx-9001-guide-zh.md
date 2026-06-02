---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程JMX端口9001配置指南
translated: true
type: note
---

**JMX 远程代理**是 Java 管理扩展（JMX）的组成部分。它允许您远程监控和管理正在运行的 Java 应用程序。当您启用 JMX 远程管理时，JVM 会启动一个代理，通过 TCP 端口暴露 MBean（托管 Bean）。诸如 **jconsole**、**VisualVM** 或自定义监控软件等工具可以连接到该端口，以检查内存使用情况、线程状态、GC 活动，甚至调用操作。

关于 **9001 端口**：

* 实际端口号取决于应用程序的配置方式。通常您会看到 9001、9090、9091 等端口。
* 如果您发现某个程序正在监听 `9001` 端口，并且它是一个 **JMX 远程代理**，则意味着某个 Java 进程启动时设置了以下系统属性：

  ```bash
  -Dcom.sun.management.jmxremote
  -Dcom.sun.management.jmxremote.port=9001
  -Dcom.sun.management.jmxremote.authenticate=false
  -Dcom.sun.management.jmxremote.ssl=false
  ```

这将在 `9001` 端口上开启 JMX，且无需身份验证/SSL（通常仅用于内部或开发环境，因为如果公开暴露会存在安全风险）。

---

### 如何在 Windows 上检查哪个程序使用了 JMX 端口 9001

1. 打开**命令提示符（以管理员身份运行）**。
2. 运行：

   ```cmd
   netstat -ano | findstr :9001
   ```

   这将显示绑定到该端口的 PID（进程 ID）。
3. 要识别该程序：

   ```cmd
   tasklist /FI "PID eq <PID>"
   ```

   将 `<PID>` 替换为步骤 2 中获取的数字。

---

### 如何停止 / 终止它

* 如果您确认这是一个不需要的 Java 进程，可以使用以下命令终止它：

  ```cmd
   taskkill /PID <PID> /F
   ```

* 但如果它是您的应用程序服务器（如 Tomcat、WebSphere、Spring Boot 应用等）的一部分，最好通过其服务/控制台来停止它，而不是直接终止进程，以确保其正常关闭。

---

👉 您是否还需要我向您展示如何在 Java 应用程序中**禁用 JMX 远程代理**，从而使其完全不开放 9001 端口？
