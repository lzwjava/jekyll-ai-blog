---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在WebSphere中配置IBM MQ
translated: true
type: note
---

### 在 IBM WebSphere Application Server 中配置消息队列（使用 IBM MQ 作为提供程序）

IBM WebSphere Application Server (WAS) 通过 Java Message Service (JMS) 与 IBM MQ（原 WebSphere MQ）集成来支持消息队列。配置通常通过 **WebSphere Integrated Solutions Console**（管理界面）完成，访问地址为 `https://your-server:9043/ibm/console`（默认安全端口；请根据实际情况调整）。本指南主要针对传统完整配置文件的 WAS（例如 9.0+ 版本），但步骤与 WebSphere Liberty 类似，只需稍作调整。

#### 前提条件

- IBM MQ 必须已安装、正在运行且可访问（例如，队列管理器已启动）。
- WAS 服务器已启动，并且您拥有控制台的管理员访问权限。
- 如果尚未安装，请将 IBM MQ JMS 客户端库（例如 `com.ibm.mq.allclient.jar`）下载并安装到 WAS 的共享库中（位于 **环境 > 共享库**）。
- 确保已配置 WebSphere MQ 消息提供程序（位于 **资源 > JMS > JMS 提供程序**）。如果未配置，请创建一个，并填写详细信息，如主机、端口（默认 1414）和队列管理器名称。

配置完成后，保存更改（顶部的 **保存** 按钮）并重新启动应用服务器以使更改生效。

#### 步骤 1：创建 JMS 队列连接工厂

连接工厂用于建立与 IBM MQ 队列管理器的连接。

1. 登录到 WAS 管理控制台。
2. 在导航窗格中，展开 **资源 > JMS > 队列连接工厂**。
3. 从下拉菜单中选择适当的 **作用域**（例如，单元、节点、服务器），然后单击 **应用**。
4. 单击 **新建**。
5. 选择 **WebSphere MQ 消息提供程序**，然后单击 **确定**。
6. 在下一个屏幕上：
   - **名称**：输入描述性名称（例如 `MyMQQueueConnectionFactory`）。
   - **JNDI 名称**：输入 JNDI 绑定（例如 `jms/MyQueueConnectionFactory`）。
   - 单击 **下一步**。
7. 输入连接详细信息：
   - **队列管理器**：您的 IBM MQ 队列管理器名称（例如 `QM1`）。
   - **主机名**：IBM MQ 服务器的主机名或 IP 地址。
   - **端口**：监听端口（默认：1414）。
   - **传输类型**：CHANNEL（用于客户端模式）或 BINDINGS（用于嵌入式模式）。
   - **通道**：默认通道名称（例如 `SYSTEM.DEF.SVRCONN`）。
   - **用户 ID** 和 **密码**：用于 MQ 身份验证的凭据（如果需要）。
   - 单击 **下一步**。
8. 查看摘要并单击 **完成**。
9. 选择新创建的工厂，转到 **其他属性 > 连接池**（可选），并调整设置，如 **最大连接数**（例如，根据预期负载调整）。
10. 单击 **测试连接** 进行验证。

#### 步骤 2：创建 JMS 队列目标

这定义了用于发送/接收消息的实际队列端点。

1. 在导航窗格中，展开 **资源 > JMS > 队列**。
2. 选择适当的 **作用域**（与连接工厂匹配），然后单击 **应用**。
3. 单击 **新建**。
4. 选择 **WebSphere MQ 消息提供程序**，然后单击 **确定**。
5. 指定属性：
   - **名称**：描述性名称（例如 `MyRequestQueue`）。
   - **JNDI 名称**：JNDI 绑定（例如 `jms/MyRequestQueue`）。
   - **基本队列名称**：IBM MQ 中的确切队列名称（例如 `REQUEST.QUEUE`；必须在 MQ 中存在或创建）。
   - **目标客户端**：JMS（用于 JMS 应用）或 MQ（用于原生 MQ 应用）。
   - **目标目的地模式**：仅一次（默认用于可靠性）。
   - 单击 **确定**。
6. （可选）在 **其他属性** 下，配置持久性、过期时间或优先级设置。
7. 保存配置。

#### 步骤 3：（可选）为消息驱动 Bean (MDB) 创建激活规范

如果使用 MDB 异步消费消息：

1. 在导航窗格中，展开 **资源 > JMS > 激活规范**。
2. 选择 **作用域** 并单击 **新建**。
3. 选择 **WebSphere MQ 消息提供程序**，然后单击 **确定**。
4. 输入：
   - **名称**：例如 `MyQueueActivationSpec`。
   - **JNDI 名称**：例如 `jms/MyQueueActivation`。
   - **目标类型**：队列。
   - **目标 JNDI 名称**：您的队列的 JNDI（例如 `jms/MyRequestQueue`）。
   - **连接工厂 JNDI 名称**：您的连接工厂的 JNDI（例如 `jms/MyQueueConnectionFactory`）。
   - 消息选择器（可选）：用于过滤消息的 JMS 选择器。
5. 在 **其他属性 > 消息监听服务 > 监听端口** 下，如果需要，创建一个端口：
   - **名称**：例如 `MyListenerPort`。
   - **连接工厂 JNDI**：如上所述。
   - **目标 JNDI**：如上所述。
   - **组件**：您的 MDB 的部署描述符。
6. 单击 **确定** 并保存。

#### 步骤 4：验证和测试

- **在控制台中测试**：使用工厂和规范上的 **测试连接**。
- **部署应用**：创建一个简单的 JMS 客户端或 MDB 应用，部署它，并通过 IBM MQ 工具（例如 MQ Explorer）发送/测试消息。
- **监控**：在 **监控和调优 > 性能查看器** 或 **故障排除 > 日志** 下，检查与 JMS 相关的错误。
- 常见问题：
  - 连接失败：验证防火墙、MQ 通道状态（`DISPLAY CHANNEL`）和凭据。
  - JNDI 查找错误：确保绑定正确，并且应用使用了正确的作用域。
  - 持久性：在 WAS 和 MQ 之间对齐持久性设置。

有关命令行替代方案（wsadmin 脚本），请参考 IBM 文档。根据您的版本进行调整（例如，WAS 9.0.5+ 支持 JMS 2.0）。

#### 参考资料

- [在 WebSphere Application Server 中配置 JMS 资源](https://www.ibm.com/docs/en/ibm-mq/9.2.x?topic=resources-configuring-jms-in-websphere-application-server)
- [WebSphere MQ 消息提供程序队列设置](https://www.ibm.com/docs/en/was/8.5.5?topic=settings-websphere-mq-messaging-provider-queue)
- [创建 WebSphere MQ 消息提供程序队列连接工厂](https://help.hcl-software.com/commerce/7.0.0/com.ibm.commerce.integration.doc/tasks/tcvjmsqueuefactory.html)
- [为 WebSphere MQ 配置 JMS 队列目标](http://www.setgetweb.com/p/i5/portal/WAS60/Configure_JMS_queue_destinationfor_WebSphere_MQ.html)
