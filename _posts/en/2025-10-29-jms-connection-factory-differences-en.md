---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: JMS Connection Factory Differences
translated: false
type: note
---

In IBM WebSphere Application Server (WAS), both connection factories and queue connection factories are JMS (Java Message Service) resources used to establish connections to a JMS provider for messaging. However, they differ in scope, API compatibility, and usage based on JMS domain models (point-to-point vs. publish/subscribe). Here's a breakdown:

### Key Differences

| Aspect                  | Connection Factory                                                                 | Queue Connection Factory                                                                 |
|-------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Primary Purpose**    | Creates JMS connections to destinations for **both** point-to-point (queues) and publish/subscribe (topics) messaging. Supports the unified "classic" API introduced in JMS 1.1. | Creates JMS connections **exclusively** for point-to-point messaging with queues. Based on the legacy domain-specific API from JMS 1.0. |
| **API Hierarchy**      | Base interface (`javax.jms.ConnectionFactory`). Can dynamically create `Queue` or `Topic` destinations and sessions in the same connection/session. | Subclass of `ConnectionFactory` (`javax.jms.QueueConnectionFactory`). Only creates `QueueConnection` and `QueueSession` objects; cannot handle topics. |
| **Flexibility**        | More flexible for modern applications. Allows mixing queue and topic operations in the same transaction/unit of work (JMS 1.1+). Ideal for code that needs to switch between messaging styles without reconfiguration. | Less flexible; limited to queues. Useful for legacy JMS 1.0 code or strict separation of concerns where only point-to-point is needed. |
| **Configuration in WAS**| Configured under **Resources > JMS > Connection factories** in the admin console. Associated with a JMS provider (e.g., default messaging, WebSphere MQ). | Configured under **Resources > JMS > Queue connection factories**. Tied to queue-specific providers like IBM MQ or default messaging for point-to-point only. |
| **When to Use**        | Preferred for new development or apps using JMS 1.1+. Use when your app might interact with both queues and topics. | Use for backward compatibility with JMS 1.0 domain-specific code, or when explicitly restricting to queues (e.g., in WebSphere MQ setups for performance/security isolation). |
| **Performance/Security**| Generally equivalent, but may require additional setup for cross-domain use. | Can be optimized for queue-only (e.g., bindings transport in MQ for faster throughput, ~30% improvement). |

### Example Usage in Code

- **With Connection Factory** (unified, flexible):

  ```java
  ConnectionFactory factory = (ConnectionFactory) context.lookup("jms/ConnectionFactory");
  Connection conn = factory.createConnection();
  Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);
  // Can create either:
  Queue queue = session.createQueue("myQueue");
  Topic topic = session.createTopic("myTopic");
  ```

- **With Queue Connection Factory** (queue-only):

  ```java
  QueueConnectionFactory qFactory = (QueueConnectionFactory) context.lookup("jms/QueueConnectionFactory");
  QueueConnection qConn = qFactory.createQueueConnection();
  QueueSession qSession = qConn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);
  Queue queue = qSession.createQueue("myQueue");
  // Cannot create topics here.
  ```

In summary, opt for a general connection factory for versatility in contemporary JMS apps on WAS, while queue connection factories are a specialized holdover for queue-centric or legacy scenarios.

[Connection factory collection - IBM](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=settings-connection-factory-collection)
[Queue connection factory collection - IBM](https://www.ibm.com/docs/en/was-nd/8.5.5?topic=settings-queue-connection-factory-collection)
[JMS QueueConnectionFactory vs ConnectionFactory - Stack Overflow](https://stackoverflow.com/questions/30121654/jms-queueconnectionfactory-vs-connectionfactory)
[Queue Connection Factory VS Connection Factory - MQSeries.net](https://mqseries.net/phpBB/viewtopic.php?p=102901)
