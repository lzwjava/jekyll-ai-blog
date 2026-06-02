---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: WebSphere应用服务器中的JMS
translated: true
type: note
---

### IBM WebSphere Application Server (WAS) 中的 JMS 工作原理

JMS（Java 消息服务）是一种标准 API，用于以解耦、异步的方式在 Java 应用程序之间发送和接收消息。在 WAS 中，JMS 通过**默认消息传递提供程序**实现，该提供程序使用**服务集成总线（SIBus）**作为其底层消息传递引擎。SIBus 是一个内置的可扩展总线，无需外部软件即可处理消息路由、排队和传递。

#### 关键组件与流程
1. **服务集成总线（SIBus）**：这是核心基础设施。它类似于一个虚拟网络，消息引擎（每个服务器或集群一个）在其中处理消息。您需要创建一个总线，将服务器添加为成员，并在其上定义目标（队列或主题）。

2. **连接工厂**：充当入口点。您的 Java 应用程序通过 JNDI（例如 `jms/MyConnectionFactory`）查找此工厂，以创建到 SIBus 的 JMS 连接。

3. **目标（队列/主题）**：队列用于点对点消息传递（一个发送者，一个接收者）。一旦创建并绑定到总线，它们就会持久存储消息（使用文件存储或数据库，可配置）。

4. **消息流过程**：
   - **发送**：应用程序通过连接工厂创建 JMS 会话，通过 JNDI 获取队列引用，并发送消息（例如 `TextMessage`）。SIBus 将其路由到目标消息引擎，由引擎将其加入队列。
   - **接收**：消费者（例如另一个应用程序或消息驱动 Bean）以类似方式连接，并轮询或监听消息。SIBus 可靠地传递消息，处理重试、确认和事务。
   - SIBus 支持集群以实现高可用性、负载均衡，并支持外部总线链接以与其他系统集成。

WAS 管理生命周期：启动/停止引擎、监控队列，并根据您的配置（例如持久化与非持久化消息）确保持久性。

#### 创建 JMS 队列是否能让 Java 应用程序发送/接收消息？
是的，完全正确。完成设置（如前所述：总线、成员、连接工厂、队列）后，您的 Java 应用程序可以：
- 使用标准 JMS API（`javax.jms.*`）发送/接收消息。
- 在应用服务器上下文中通过 JNDI 查找资源。
- 发送消息的示例代码片段：
  ```java
  InitialContext ctx = new InitialContext();
  QueueConnectionFactory qcf = (QueueConnectionFactory) ctx.lookup("jms/MyConnectionFactory");
  Queue queue = (Queue) ctx.lookup("jms/MyQueue");
  QueueConnection conn = qcf.createQueueConnection();
  QueueSession session = conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
  QueueSender sender = session.createSender(queue);
  TextMessage msg = session.createTextMessage("Hello JMS!");
  sender.send(msg);
  // 关闭资源...
  ```
接收消息类似，使用 `QueueReceiver` 或 MDB。无需为总线编写自定义代码——这一切都已抽象化。

#### WAS 是否能正确处理队列？
绝对可以。SIBus 负责：
- **持久性**：消息在重启后仍保留（文件/数据库存储）。
- **可靠性**：保证传递，失败时使用死信队列。
- **可扩展性**：处理高吞吐量、集群。
- **监控**：在管理控制台中查看统计信息（例如消息计数、积压）。
如果出现问题（例如队列已满），可以查看日志和警报。它已为企业使用做好生产准备。

#### 是否需要像 Kafka 这样的额外插件？
不需要，完全不需要类似 Kafka 的组件——SIBus 完全集成在 WAS 中（除了 WAS 本身之外，无需单独安装或许可）。Kafka 是一个不同的分布式流平台；SIBus 是专为 JMS 设计的，对 WAS 应用程序更简单。如果您需要类似 Kafka 的功能（例如流），可以通过外部总线链接集成，但对于标准的 JMS 队列，请坚持使用默认提供程序。

如需深入了解，请查阅 IBM 文档：[使用默认消息传递提供程序管理消息传递](https://www.ibm.com/docs/en/was/9.0.5?topic=resources-managing-messaging-default-messaging-provider) 和 [JMS 应用程序如何连接到总线上的消息引擎](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=messaging-how-jms-applications-connect-engine-bus)。
