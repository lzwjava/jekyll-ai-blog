---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: IBM MQ WebSphere应用服务器配置
translated: true
type: note
---

### 前置条件

在 IBM WebSphere Application Server (WAS) 中配置 IBM MQ（前身为 WebSphere MQ）之前，请确保满足以下条件：

- IBM MQ 已安装在专用服务器上（若为本地绑定模式，可与 WAS 安装在同一服务器）。
- 已在 IBM MQ 中创建队列管理器（例如使用 `crtmqm QMNAME` 命令）。
- 已在队列管理器中创建所需队列（例如使用 MQ Explorer 或 `runmqsc` 命令）。
- IBM MQ 客户端库（如 `com.ibm.mq.allclient.jar`、`com.ibm.mqjms.jar`）可用。若 WAS 与 MQ 分属不同服务器，请在 WAS 所在机器安装 IBM MQ 客户端。
- 将 WAS 进程用户添加至 `mqm` 组以获取权限。
- 在类 Unix 系统上，对于非 root 用户，请使用 `setmqaut` 命令授予权限。

### 逐步配置指南

配置过程涉及在 WAS 管理控制台中设置 JMS 提供程序、连接工厂和目的地。本指南假设通过 TCP/IP 建立分布式（客户端）模式连接；若为本地绑定模式请相应调整。

1. **访问 WAS 管理控制台**：
   - 启动 WAS 服务器。
   - 打开浏览器并访问 `https://localhost:9043/ibm/console`（请替换为实际主机地址/端口）。
   - 使用管理员凭据登录。

2. **配置 IBM MQ JMS 提供程序**：
   - 进入 **资源 > JMS > 提供程序**。
   - 点击 **新建**。
   - 选择 **WebSphere MQ 消息传递提供程序**。
   - 填写详细信息：
     - **名称**：例如 `MQProvider`。
     - **描述**：选填。
     - **类路径**：MQ JAR 文件路径（例如 `/opt/mqm/java/lib/*` 或复制至 `<WAS_HOME>/lib/ext`）。
     - **本地库路径**：绑定模式必需（MQ 库路径，例如 `/opt/mqm/lib64`）。
     - **外部初始上下文工厂名称**：`com.ibm.mq.jms.context.WMQInitialContextFactory`（适用于客户端模式）。
     - **外部上下文提供程序 URL**：例如 `host:1414/CHANNEL`（host 为 MQ 服务器 IP，1414 为默认端口，CHANNEL 例如 `SYSTEM.DEF.SVRCONN`）。
   - 保存配置。

3. **创建队列连接工厂**：
   - 进入 **资源 > JMS > 队列连接工厂**（作用域选择服务器或单元）。
   - 点击 **新建**。
   - 选择步骤 2 创建的提供程序。
   - 填写：
     - **名称**：例如 `MQQueueCF`。
     - **JNDI 名称**：例如 `jms/MQQueueCF`。
     - **队列管理器**：您的 MQ 队列管理器名称（例如 `QM1`）。
     - **主机**：MQ 服务器主机名或 IP。
     - **端口**：1414（默认）。
     - **通道**：例如 `SYSTEM.DEF.SVRCONN`。
     - **传输类型**：`CLIENT`（适用于 TCP/IP）或 `BINDINGS`（本地）。
     - **安全凭据**：如需认证请填写用户 ID 和密码。
   - 可选高级属性：设置连接池大小（例如根据负载调整最大连接数）。
   - 保存。

4. **创建队列目的地**：
   - 进入 **资源 > JMS > 队列**。
   - 点击 **新建**。
   - 选择提供程序。
   - 为每个队列配置：
     - **名称**：例如 `MyQueue`。
     - **JNDI 名称**：例如 `jms/MyQueue`。
     - **队列名称**：MQ 中的确切队列名（例如 `MY.LOCAL.QUEUE`）。
     - **队列管理器**：同上文设置。
     - **目标客户端类型**：`MQ` 或 `JMS`。
   - 保存。若使用发布/订阅模式，请重复此步骤创建主题。

5. **（可选）为绑定模式配置 WebSphere MQ 服务器**：
   - 若使用本地绑定，请进入 **服务器 > 服务器类型 > WebSphere MQ 服务器**。
   - 点击 **新建**。
   - 设置 **名称**、**队列管理器名称**。
   - 指定 **MQ 安装路径**。
   - 保存并重启服务器。

6. **配置 JCA 资源适配器（适用于 MDB）**：
   - 进入 **资源 > 资源适配器 > J2C 连接工厂**。
   - 若使用内置 MQ RA，请确保已部署（WAS 包含 `wmq.jmsra.rar`）。
   - 设置属性如最大连接数（例如根据负载设置 10-50）。

7. **测试配置**：
   - 部署示例 JMS 应用程序或使用 WAS JMS 示例。
   - 检查日志中的错误（例如端口 1414 连接被拒绝）。
   - 在 MQ 中验证：使用 MQ Explorer 监控队列深度和通道状态。

8. **安全与高级设置**：
   - 启用 SSL：在 WAS 和 MQ 中配置密钥库（通道需设置 `SSLCIPH`）。
   - 设置认证：使用 MQ 用户组或备用用户 ID。
   - 对于集群：跨节点同步配置。

### 故障排除提示

- **ClassNotFoundException**：确保 MQ JAR 文件在类路径中。
- **连接失败**：检查端口 1414 的防火墙设置、通道状态（在 runmqsc 中使用 `DISPLAY CHSTATUS(*)`）。
- **绑定模式问题**：验证本地库和用户是否在 `mqm` 组中。
- 修改配置后重启 WAS。

有关版本特定详情（例如 WAS 9.x 与 MQ 9.x），请参考 IBM 官方文档。

[结合使用 WebSphere Application Server 与 IBM MQ](https://www.ibm.com/docs/en/ibm-mq/9.2.x?topic=together-using-websphere-application-server-mq)
[配置 WebSphere Application Server 以使用 IBM MQ](https://help.hcl-software.com/commerce/9.0.0/integration/tasks/tcvconfigure_was_for_mq.html)
[创建 WebSphere MQ 服务器定义](https://www.ibm.com/docs/SSAW57_8.5.5/com.ibm.websphere.nd.multiplatform.doc/ae/tjfp0004_.html)
