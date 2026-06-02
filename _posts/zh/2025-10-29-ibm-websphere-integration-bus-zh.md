---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: IBM WebSphere 服务集成总线
translated: true
type: note
---

### IBM WebSphere Application Server 中的服务集成总线

在 IBM WebSphere Application Server（WAS）环境中，“集成总线”通常指的是**服务集成总线（SIB 或 SIBus）**，这是 WAS 内置的消息传递基础设施。它支持应用程序之间可靠、异步的通信，特别适用于基于消息的架构或面向服务的架构（SOA）。

#### 目的

SIB 在 WAS 环境中充当虚拟消息骨干。它允许运行在不同服务器或集群上的应用程序交换消息，而无需直接的点对点连接，从而促进松耦合、可扩展性和容错能力。主要用例包括：

- 支持用于队列和发布/订阅模式的 Java 消息服务（JMS）。
- 在 SOA 设置中集成企业服务。
- 在分布式系统中处理消息路由、转换和持久化。

与独立的企业服务总线（如 IBM Integration Bus，前身为 WebSphere Message Broker）不同，SIB 原生嵌入在 WAS 中，无需单独安装——通过配置即可启用。

#### 关键组件与架构

- **总线成员**：这些是加入总线的 WAS 单元中的应用程序服务器或服务器集群。每个成员托管部分消息传递基础设施。
- **消息引擎（ME）**：处理消息的核心运行时组件。每个 ME 在 WAS 进程（例如，在总线成员上）中运行，负责发送、接收和存储消息。ME 动态连接以形成高可用性的中介网络。
- **SIB 服务**：每个 WAS 应用服务器上的默认服务，默认情况下处于禁用状态。启用该服务将激活消息传递功能。
- **目的地**：队列或主题，用于发布或消费消息，可通过 WAS 管理控制台进行配置。
- **数据存储**：为了持久化，ME 使用基于文件的存储（单服务器使用本地存储，集群使用共享文件系统）或数据库，以确保消息的持久性。

该架构基于单元：在 WAS 网络部署设置中，多个总线成员跨节点协作，使用 SOAP/HTTP 或 JMS 等协议实现互操作性。

#### 设置与使用方法

1. **创建**：通过 WAS 集成解决方案控制台（管理控制台），导航至 *服务集成 > 总线 > 新建*。定义总线名称，添加成员（服务器/集群），并配置 ME（例如，高可用性策略）。
2. **配置**：启用 SIB JMS 提供程序，创建目的地（队列/主题），并将其映射到 JNDI 名称以供应用程序访问。
3. **使用**：应用程序部署消息驱动 Bean（MDB）或使用 JMS API 与总线交互。例如，发送方应用程序将消息放入队列，总线将其路由到其他成员上的接收方。

SIB 支持 JMS 1.1/2.0 等标准，并与外部系统（例如，通过 WebSphere MQ 桥接）集成。在生产环境中，需考虑性能调优，例如使用共享数据存储实现故障转移。

**注意**：如果您指的是 *IBM Integration Bus*（IIB），这是一个用于更广泛 ESB 需求的独立产品，可以连接到 WAS/SIB，但本身并不“在” WAS 中。

[服务集成总线 - IBM 文档](https://www.ibm.com/docs/en/was/9.0.5?topic=integration-service-buses)
[服务集成总线消息传递提供程序 - IBM 文档](https://www.ibm.com/docs/en/was-liberty/nd?topic=providers-service-integration-bus-messaging-provider)
[服务集成总线入门指南](https://www.freekb.net/Article?id=1975)
