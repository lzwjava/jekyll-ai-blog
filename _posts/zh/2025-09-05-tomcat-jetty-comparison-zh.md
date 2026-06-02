---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tomcat与Jetty对比
translated: true
type: note
---

Tomcat 和 Jetty 都是流行的 **基于 Java 的 Web 服务器和 Servlet 容器**，但它们的定位略有不同且各具优势。以下采用叙述式对比以便阅读：

---

### Tomcat

由 Apache 软件基金会开发的 Tomcat，常被视为运行 Java Web 应用程序的 **默认选择**。

* **定位**：主要作为 Java Servlet 和 JSP 规范的参考实现
* **生态适配**：众多框架（如 Spring MVC）默认采用 Tomcat 作为容器，因此集成方案和文档资源非常丰富
* **性能表现**：在高并发场景下稳定可靠，但在轻量级部署时比 Jetty 存在更多开销
* **适用场景**：需要标准 Servlet/JSP 支持的大型企业级应用和生产系统

---

### Jetty

由 Eclipse 基金会开发的 Jetty 是轻量级且高度可嵌入的解决方案。

* **定位**：致力于成为可嵌入其他应用的轻量高速 HTTP 服务器与 Servlet 容器
* **生态适配**：常见于微服务架构、需要内置 HTTP 引擎的框架及服务器（如 Hadoop、Spark、Solr 以及众多嵌入 Jetty 的 Spring Boot 应用）
* **性能表现**：启动速度极快，内存占用更低，特别适合短连接密集型场景（如 WebSockets）
* **适用场景**：微服务、物联网设备、需要集成 Web 服务器的工具类应用或资源受限环境

---

### 核心差异精髓

* **Tomcat** 更像是“功能完备、开箱即用”的服务器，在需要具备成熟生态的独立应用服务器时表现卓越
* **Jetty** 更接近“组件”而非“产品”，当需要将 HTTP 服务嵌入应用或保持最小资源占用时更具优势

---

👉 开发 **企业级 Web 应用** 时，Tomcat 通常是首选
👉 构建 **轻量级服务或工具类应用** 且服务器仅作为系统组成部分时，Jetty 往往更合适

---

需要进一步了解它们在 **Spring Boot 中的具体对比** 吗？这通常是开发者在嵌入式 Tomcat 与 Jetty 之间做决策的关键场景。
