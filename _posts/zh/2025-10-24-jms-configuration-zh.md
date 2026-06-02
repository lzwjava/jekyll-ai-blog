---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在WebSphere中配置JMS资源
translated: true
type: note
---

### 前置条件
- 确保您拥有 IBM WebSphere Application Server (WAS) 集成解决方案控制台（管理控制台）的管理员访问权限。
- 服务器应处于运行状态，且需确定资源的作用域（例如：单元、节点、服务器）。
- 本指南重点介绍默认消息传递提供程序（使用服务集成总线 SIBus），即 WAS 内置的 JMS 提供程序。若使用 WebSphere MQ，则需额外配置 MQ 提供程序。
- 若系统提示，请在重大更改后重启服务器。

### 步骤 1：创建服务集成总线
服务集成总线充当 JMS 资源的消息传递主干。

1. 登录 WebSphere 集成解决方案控制台。
2. 导航至 **服务集成 > 总线**。
3. 点击 **新建**。
4. 输入唯一的总线名称（例如 `MyJMSBus`）。
5. 除非需要，请取消勾选 **总线安全性** 选项。
6. 点击 **下一步**，然后点击 **完成** 创建总线。

### 步骤 2：将服务器添加为总线成员
这使服务器能够在总线上托管消息传递引擎。

1. 选择您创建的总线（例如 `MyJMSBus`）。
2. 在 **其他属性** 下，点击 **总线成员**。
3. 点击 **添加**。
4. 在 **添加新总线成员** 向导中：
   - 选择 **消息传递引擎** 作为总线成员类型。
   - 从列表中选择您的服务器（例如 `server1`）。
   - 对于消息存储，选择 **文件存储**（非集群环境的默认选项）或用于数据库持久化的 **数据存储**，并根据需要配置属性。
5. 点击 **下一步**，然后点击 **完成**。
6. 重启 WebSphere Application Server 以激活总线成员。

### 步骤 3：创建 JMS 连接工厂
连接工厂用于将 JMS 客户端连接到提供程序。

1. 导航至 **资源 > JMS > 连接工厂**。
2. 选择适当的作用域（例如 `server1` 的服务器作用域）并点击 **新建**。
3. 选择 **默认消息传递提供程序** 并点击 **确定**。
4. 输入详细信息：
   - **名称**：例如 `MyJMSConnectionFactory`。
   - **JNDI 名称**：例如 `jms/MyConnectionFactory`。
   - **总线名称**：从下拉菜单中选择 `MyJMSBus`。
   - 保留其他默认设置（例如提供程序端点设为自动检测）。
5. 点击 **应用**，然后 **保存** 至主配置。

### 步骤 4：创建 JMS 队列
此操作用于定义点对点消息传递的队列目标。

1. 导航至 **资源 > JMS > 队列**。
2. 选择适当的作用域并点击 **新建**。
3. 选择 **默认消息传递提供程序** 并点击 **确定**。
4. 输入详细信息：
   - **名称**：例如 `MyJMSQueue`。
   - **JNDI 名称**：例如 `jms/MyQueue`。
   - **总线名称**：选择 `MyJMSBus`。
   - **队列名称**：选择 **创建服务集成总线目标**，输入唯一标识符（例如 `MyQueueDestination`），并选择之前创建的总线成员。
   - **基本队列名称**：例如 `$MyJMSBus:MyQueueDestination`（自动生成）。
5. 根据需要配置其他属性（例如传递模式、过期时间）。
6. 点击 **应用**，然后 **保存** 至主配置。

### 步骤 5：（可选）为消息驱动 Bean (MDB) 创建激活规范
若使用 MDB 从队列消费消息，需配置激活规范。

1. 导航至 **资源 > JMS > 激活规范**。
2. 选择适当的作用域并点击 **新建**。
3. 选择 **默认消息传递提供程序** 并点击 **确定**。
4. 输入详细信息：
   - **名称**：例如 `MyActivationSpec`。
   - **JNDI 名称**：例如 `jms/activation/MyActivationSpec`。
   - **总线名称**：选择 `MyJMSBus`。
   - **目标类型**：队列。
   - **目标**：输入队列的 JNDI 名称（例如 `jms/MyQueue`）。
5. 点击 **应用**，然后 **保存** 至主配置。

### 验证与测试
- 保存后，若处于集群环境中，请同步节点。
- 重启服务器。
- 使用 JMS 客户端应用程序通过 JNDI 名称测试消息发送/接收。
- 通过 **服务集成 > 总线 > [您的总线] > 总线成员 > [您的成员] > 消息传递引擎** 进行监控。

关于高级配置（例如安全性、集群），请参阅 IBM 文档。

[配置 IBM WebSphere Application Server 以运行 Decision Server](https://docs.redhat.com/en/documentation/red_hat_decision_manager/7.4/html/installing_and_configuring_decision_server_on_ibm_websphere_application_server/was-configure-proc)
[使用默认消息传递提供程序管理消息传递](https://www.ibm.com/docs/en/was/9.0.5?topic=resources-managing-messaging-default-messaging-provider)
