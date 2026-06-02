---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: WebSphere的JMS与JNDI API
translated: true
type: note
---

### Java中JMS所需的包与API

要使用您引用的JMS代码片段（用于在IBM WebSphere应用服务器中查找并连接JMS连接工厂），您需要导入相关的Java包。这些是Java EE/Jakarta EE生态系统中的标准API：

- **JNDI（Java命名和目录接口）**：用于`InitialContext`查找。
  - 包：`javax.naming`（或新版Jakarta EE中的`jakarta.naming`）
  - 关键类：`InitialContext`——这是JNDI操作的起点。它提供了通过JNDI名称（如`"jms/MyConnectionFactory"`）查找资源（如JMS工厂或队列）的上下文环境。在WAS等容器中，它会自动连接至服务器的命名服务。

- **JMS（Java消息服务）API**：用于创建连接、会话、发送器/接收器和消息。
  - 包：`javax.jms`（JMS 1.1/2.0）或现代EE中的`jakarta.jms`（Jakarta JMS 3.0+）
  - 关键接口：`QueueConnectionFactory`、`QueueConnection`、`QueueSession`、`QueueSender`、`Queue`、`TextMessage`等

Java类文件顶部的导入示例：

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

**什么是`InitialContext`？**
这是JNDI API中的一个类，作为命名服务的入口点。在代码中：

```java
InitialContext ctx = new InitialContext();  // 创建绑定至应用服务器JNDI环境的默认上下文
QueueConnectionFactory qcf = (QueueConnectionFactory) ctx.lookup("jms/MyConnectionFactory");  // 通过JNDI名称查找预配置的工厂
```

对于运行在WAS*内部*的应用程序，构造函数无需任何属性，因为容器会注入环境（例如通过`java.naming.factory.initial`）。若在WAS*外部*运行独立客户端，则需传递包含提供程序URL等属性的`Hashtable`。

### Maven依赖配置（pom.xml）

如果Java应用部署在WAS内部运行（例如作为Web应用、EJB或企业级Bean）：

- **无需额外依赖**。WAS作为Java EE运行时环境，已内置提供JMS和JNDI API。编译时直接引用即可（构建/部署时它们已在类路径中）。
- 在`pom.xml`中，可通过`<scope>provided</scope>`显式声明这些依赖，避免将其打包到WAR/EAR中（保持轻量化）：

  ```xml
  <dependencies>
      <dependency>
          <groupId>javax.jms</groupId>  <!-- 新版本可使用jakarta.jms -->
          <artifactId>javax.jms-api</artifactId>
          <version>2.0.1</version>  <!-- JMS 2.0，兼容WAS 8.5+ -->
          <scope>provided</scope>
      </dependency>
      <dependency>
          <groupId>javax.naming</groupId>
          <artifactId>javax.naming-api</artifactId>
          <version>1.0</version>  <!-- JNDI 1.0标准 -->
          <scope>provided</scope>
      </dependency>
  </dependencies>
  ```

如果应用是独立客户端（在WAS外部运行，例如连接服务器的瘦客户端）：

- 需要通过IIOP获得完整JMS支持时，需使用**WebSphere应用客户端**库。从IBM下载"IBM WebSphere Application Server traditional"客户端包，然后将其添加至类路径。
- 在`pom.xml`中包含：

  ```xml
  <dependency>
      <groupId>com.ibm.ws</groupId>
      <artifactId>was-jms-client</artifactId>  <!-- 近似依赖项；若可用请使用IBM Maven仓库 -->
      <version>9.0.5</version>  <!-- 请与您的WAS版本匹配 -->
  </dependency>
  ```

  或使用完整的瘦客户端JAR包（例如`com.ibm.ws.orb_8.5.5.jar`、`com.ibm.ws.jndi_*.jar`）。具体配置请查阅IBM文档。

对于Jakarta EE迁移（2020年后），建议切换至`jakarta.*`包，但WAS 9.x默认仍使用`javax.*`——如需启用Jakarta，请通过功能包进行配置。

[IBM WebSphere JMS API文档](https://www.ibm.com/docs/en/was/9.0.5?topic=resources-jms-api)
[Java EE JNDI教程](https://docs.oracle.com/javase/tutorial/jndi/)
