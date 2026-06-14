---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ThingsBoard物联网平台介绍
translated: true
type: note
---

**问题：** 什么是 ThingsBoard（thingsboard.io）？请给出全面介绍。

**回答：**

## ThingsBoard — 全面介绍

### 是什么

ThingsBoard 是一个开源物联网平台，用于设备管理、数据采集、处理和可视化。你可以把它看作是位于物理硬件（传感器、执行器、边缘设备）与应用层之间的“后端 + 仪表盘”层。无需从头构建发布/订阅基础设施、时序存储或仪表盘——ThingsBoard 帮你完成这一切。

它已被博世、英特尔、Engie、T-Mobile、Schwarz Group 等企业在生产环境中使用。

---

### 核心架构

ThingsBoard 围绕四个支柱构建：

**1. 设备连接（传输层）**

设备通过以下方式连接：
- **MQTT**（主要方式——大多数物联网设备）
- **CoAP**（低功耗受限设备）
- **HTTP/HTTPS**（REST 风格遥测数据上报）
- **LwM2M**（OMA 标准，用于受限设备）
- **AMQP、Kafka**（用于企业集成）

每个设备通过令牌、X.509 证书或基本认证进行身份验证。网关产品允许你将传统协议（Modbus、BACnet、OPC-UA、CAN 总线）桥接到 ThingsBoard 世界。

**2. 数据模型（实体）**

ThingsBoard 拥有丰富的实体模型：

```
租户（Tenant）
  └── 客户（Customer）
        └── 设备（Device）/ 资产（Asset）
              ├── 属性（Attributes）（服务器端、客户端、共享）
              ├── 遥测（Telemetry）（时序键值对）
              ├── 告警（Alarms）
              └── 关系（Relations）（实体之间的边）
```

- **遥测**：时序数据（例如 `{"temperature": 23.4}`）
- **属性**：静态或半静态元数据（设备配置、位置）
- **关系**：构建数字孪生图——建筑有楼层，楼层有房间，房间有设备

**3. 规则引擎（处理层）**

这是大脑。你定义数据处理规则链。转换和标准化设备数据。根据传入的遥测事件、属性更新、设备不活动和用户操作触发告警。

规则链是在拖拽编辑器中构建的 DAG。节点类型包括：

```
[消息类型开关] → [过滤器: temperature > 80] → [创建告警]
                                                   → [发送邮件]
                                                   → [REST API 调用]
                                                   → [保存到数据库]
```

规则节点涵盖：JS/MVEL 转换、Kafka/RabbitMQ/SQS 生产者、HTTP/REST 调用、告警创建、属性丰富、去重等。

**4. 可视化（仪表盘层）**

超过 600 个可定制的小部件，让你能够为大多数物联网用例构建端到端的自定义仪表盘。小部件库包括时序图表、仪表盘、地图（Leaflet/Google Maps/OpenStreet）、表格、SCADA 符号、HTML/JS 自定义小部件以及控制小部件（用于 RPC 的滑块、按钮）。

仪表盘支持多租户——你可以向特定客户公开一个只读仪表盘，且仅包含其设备范围。

---

### 产品阵容

| 产品 | 说明 |
|---|---|
| **社区版（CE）** | 开源，Apache 2.0 许可，自托管 |
| **专业版（PE）** | 新增：高级集成、白标、边缘计算、调度器、组/角色 |
| **ThingsBoard Cloud** | 托管 SaaS（PE 功能，由他们托管） |
| **ThingsBoard Edge** | 在边缘本地运行，与云端 TB 实例同步 |
| **IoT Gateway** | 将传统协议连接到 ThingsBoard 的代理 |
| **TBMQ** | 独立的可扩展 MQTT 代理（基于 Kafka） |
| **Trendz Analytics** | 基于机器学习的分析与预测插件 |

---

### 可扩展性模型

ThingsBoard 支持微服务架构。随着集群模式下 ThingsBoard 服务器的增加，支持的服务器端请求和设备数量线性增长。无需停机、服务器重启或应用错误。

底层（PE/微服务模式）：
- **Kafka** 作为服务间的消息总线
- **Cassandra** 或 **PostgreSQL+TimescaleDB** 用于时序存储
- **Redis** 用于缓存/会话
- 服务：`tb-core`、`tb-rule-engine`、`tb-transport`（MQTT/HTTP/CoAP）、`tb-web-ui`——每个可独立扩展

在 CE 单节点模式下，它作为单体应用在单个 JVM 上运行，这对于小型部署来说完全足够。

---

### 多租户

ThingsBoard 开箱即用地支持多租户安装。单个租户可以有多个租户管理员以及数百万台设备和客户。

这使得它成为一个平台中的平台——一家公司可以在 ThingsBoard 之上构建白标物联网产品，其每个企业客户获得一个租户，并且每个企业客户可以拥有子客户。

---

### 部署用例

- 智能能源 / 计量（电力、水、气）
- 车队追踪（GPS 遥测、地理围栏）
- 智慧农业（土壤湿度、灌溉控制）
- 环境监测（空气质量指数、温湿度）
- SCADA（工业过程控制——石油/天然气、电网）
- 智能建筑 / 办公室（HVAC、占用情况）
- 医疗保健（辅助生活传感器监测）

---

### 技术栈

- **后端**：Java（Spring Boot）、Netty（用于高吞吐量 MQTT）、Akka/actors（规则引擎）
- **前端**：Angular
- **存储**：PostgreSQL（属性/实体），Cassandra 或 TimescaleDB（遥测）
- **消息传递**：Kafka（集群模式），进程内队列（单节点）
- **部署**：Docker、Kubernetes Helm charts、AWS/GCP/Azure 市场镜像

---

### 快速开始（Docker，单节点 CE）

```bash
# 拉取并运行 ThingsBoard CE
docker run -it -p 9090:9090 -p 1883:1883 -p 7070:7070 -p 5683-5688:5683-5688/udp \
  --name mytb --restart always \
  thingsboard/tb-postgres

# 默认凭据：
# 租户：tenant@thingsboard.org / tenant
# 管理员：sysadmin@thingsboard.org / sysadmin
```

然后通过 MQTT 发布遥测数据：
```bash
# 将 <ACCESS_TOKEN> 替换为你的设备令牌
mosquitto_pub -h localhost -p 1883 \
  -t "v1/devices/me/telemetry" \
  -u "<ACCESS_TOKEN>" \
  -m '{"temperature": 25.3, "humidity": 60}'
```

或者通过 HTTP：
```bash
curl -v -X POST http://localhost:8080/api/v1/<ACCESS_TOKEN>/telemetry \
  --header 'Content-Type: application/json' \
  --data-raw '{"temperature": 25.3}'
```

---

### 在物联网栈中的位置

```
[物理设备 / 传感器]
        │  MQTT / CoAP / HTTP / BACnet / Modbus
        ▼
[ThingsBoard IoT 网关]  ← 桥接传统协议
        │
        ▼
[ThingsBoard 平台]
  ├── 传输层（MQTT 代理、HTTP 适配器）
  ├── 规则引擎（基于 Kafka 的处理）
  ├── 设备注册表 + 数字孪生
  ├── 时序数据库（Cassandra/TimescaleDB）
  └── 仪表盘 / REST API / WebSocket
        │
        ▼
[你的应用 / 移动端 / 第三方：Grafana、Kafka 消费者、Webhooks]
```

---

### 与你工作的相关性

鉴于你的人工智能 + 后端工程背景：

- **规则引擎 + 人工智能**：规则引擎可以调用外部 REST API，因此你可以将设备遥测数据 → 基于 LLM 的异常检测 → 告警连接起来。他们刚刚推出的（2026 年 6 月）“AI Solution Creator”可以在 10 分钟内生成可运行的物联网原型——值得关注。
- **TBMQ**：他们的独立 MQTT 代理基于 Kafka，从分布式系统角度来看很有趣——与 Pulsar 的设计选择类似。
- **ThingsBoard Edge**：如果你对边缘机器学习（在靠近传感器的地方运行推理）感兴趣，Edge + 你的模型是一种真实的生产模式。
- **REST/WebSocket API**：完全可编程控制——你可以完全通过 Python/CLI 代理来驱动它。

参考链接：

- [ThingsBoard 官网](https://thingsboard.io)
- [ThingsBoard 文档](https://thingsboard.io/docs/)
- [ThingsBoard GitHub（CE）](https://github.com/thingsboard/thingsboard)
- [架构 / 微服务](https://thingsboard.io/docs/pe/reference/architecture/microservices/)
- [规则引擎文档](https://thingsboard.io/docs/pe/user-guide/rule-engine/)