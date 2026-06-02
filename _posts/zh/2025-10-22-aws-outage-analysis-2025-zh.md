---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS 2025年10月服务中断事件分析
translated: true
type: note
---

### 2025年10月20日AWS中断事件：详细案例分析

2025年10月20日的AWS中断是一次始于美国东部（弗吉尼亚北部）区域（us-east-1）的重大服务中断事件，该区域是AWS规模最大且最核心的数据中心。事件始于太平洋夏令时间10月19日深夜，持续约16小时，影响超过140项服务，并因该区域的依赖关系产生全球连锁反应。本次事件暴露出DNS解析、服务依赖关系和恢复流程中的脆弱性，波及数百万应用程序、网站和服务的用户。以下内容基于AWS官方事后分析报告及同期监测数据整理。

#### 时间线
中断事件分阶段演进，从问题检测开始逐步升级为级联故障，最终进入分阶段恢复。关键节点（均为太平洋夏令时间）：

| 时间 | 事件 |
|------|-------|
| 11:49 PM (10月19日) | 检测到us-east-1区域多项AWS服务错误率上升和延迟增加 |
| 12:11 AM (10月20日) | AWS公开通报错误率升高；监测网站DownDetector用户报告激增 |
| 12:26 AM | 确定问题根源为us-east-1区域DynamoDB API端点DNS解析失败 |
| 1:26 AM | 确认DynamoDB API（含全局表）出现高错误率 |
| 2:22 AM | 实施初步缓解措施；出现早期恢复迹象 |
| 2:24 AM | DynamoDB DNS问题解决，触发部分服务恢复——但出现EC2启动功能受损和网络负载均衡器健康检查失败 |
| 3:35 AM | DNS完全恢复；多数DynamoDB操作成功，但跨可用区的EC2启动仍受阻 |
| 4:08 AM | 持续处理EC2错误及Lambda轮询SQS事件源映射的延迟 |
| 5:48 AM | 部分可用区EC2启动功能恢复；SQS积压开始清理 |
| 6:42 AM | 跨可用区部署缓解措施；AWS实施新建EC2实例速率限制以稳定系统 |
| 7:14 AM | 多服务持续出现API错误与连接问题；用户侧故障达到峰值（如应用程序中断） |
| 8:04 AM | 调查聚焦于EC2内部网络 |
| 8:43 AM | 确定网络问题根本原因：EC2内部NLB健康监测子系统受损 |
| 9:13 AM | 对NLB健康检查实施额外缓解措施 |
| 9:38 AM | NLB健康检查完全恢复 |
| 10:03 AM – 12:15 PM | EC2启动功能逐步改善；Lambda调用与连接分阶段跨可用区恢复 |
| 1:03 PM – 2:48 PM | 降低节流限制；处理Redshift、Amazon Connect和CloudTrail等服务积压 |
| 3:01 PM | 所有服务恢复正常运行；预计数小时内清除少量积压（如AWS Config、Redshift） |
| 3:53 PM | AWS宣布中断事件解决 |

DownDetector等平台用户报告在太平洋夏令时间早6点达到峰值，事件数超5000起后开始下降。

#### 根本原因
本次中断源于us-east-1区域DynamoDB服务端点的DNS解析故障。作为NoSQL数据库服务，DynamoDB承担着众多AWS功能的关键“控制平面”角色——处理元数据、会话和路由。当DNS无法解析这些端点时，DynamoDB API出现延迟升高和错误激增。

初始问题虽快速解决，但引发连锁反应：
- 因依赖DynamoDB进行元数据存储，EC2实例启动失败
- EC2内部子系统（负责监控NLB健康状态）的潜在缺陷加剧网络连接问题，导致负载均衡和API调用广泛受损
- 恢复工作包含节流措施（如限制EC2启动和Lambda调用）以防过载，但依赖服务的重试机制进一步放大系统压力

AWS确认事件非网络攻击所致，而是基础设施相关故障，可能与有缺陷的DNS数据库更新或备份系统故障有关。由于us-east-1托管着IAM和Lambda等服务的核心控制平面，即使其他区域的资源也受到全球波及。

#### 受影响服务
超过142项AWS服务受影响，主要集中在依赖DynamoDB、EC2或us-east-1端点的服务。核心类别包括：

- **数据库与存储**：DynamoDB（主要）、RDS、Redshift、SQS（积压）
- **计算与编排**：EC2（启动）、Lambda（调用、轮询）、ECS、EKS、Glue
- **网络与负载均衡**：网络负载均衡器（健康检查）、API网关
- **监控与管理**：CloudWatch、CloudTrail、EventBridge、IAM（更新）、AWS Config
- **其他**：Amazon Connect、Athena及DynamoDB全局表等全局功能

并非所有服务完全中断——多数出现部分错误或延迟——但互联性使得微小故障亦会传播。

#### 影响范围
中断导致约1/3互联网依赖型应用瘫痪，全球预估超1亿用户受影响。典型案例：
- **社交与媒体**：Snapchat（登录失败）、Reddit（服务中断）、Twitch（直播问题）
- **游戏**：Roblox（服务器崩溃）、Fortnite（匹配失败）
- **金融支付**：Venmo、劳埃德等银行（交易延迟）、英国税务海关总署（税务服务）
- **零售电商**：亚马逊自营零售站点部分功能；航司值机系统（如达美、美联航延误）
- **其他**：Alexa设备（语音失效）、Twilio（通信故障）

经济损失预估超5亿美元，因用户恐慌引发网络安全扫描量激增300%。事件凸显互联网中心化问题：尽管采用多可用区设计，us-east-1处理约30%的AWS流量，使其成为单一故障点。

#### 解决与经验总结
AWS通过针对性措施解决问题：DNS修复、EC2/NLB子系统补丁及渐进式节流解除。事后建议：
- 重试失败请求
- 清理DNS缓存
- 通过自动扩展组等多可用区/区域分发资源
- 利用服务配额和缓存缓冲重试冲击

更广泛的启示包括：控制平面需更好冗余设计、采用AI驱动异常检测加速故障定位、推行多元化云策略。AWS承诺向客户提供完整根本原因分析，强调此类事件虽罕见，但揭示了超大规模扩展的挑战。

这是自2021年以来AWS在us-east-1区域最严重的服务中断，但借助自动化工具使得恢复速度快于历史同期。

#### 参考资料
- [AWS健康仪表板：2025年10月20日服务状态](https://health.aws.amazon.com/health/status?eventID=arn:aws:health:us-east-1::event/MULTIPLE_SERVICES/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE_BA540_514A652BE1A)
- [AWS中断分析：2025年10月20日](https://www.thousandeyes.com/blog/aws-outage-analysis-october-20-2025)
- [亚马逊大规模AWS中断暴露现代互联网关键弱点](https://finance.yahoo.com/news/amazons-massive-aws-outage-points-to-a-key-weakness-in-the-modern-internet-145418180.html)
- [亚马逊AWS中断原因及主流应用集体瘫痪解析](https://www.aljazeera.com/news/2025/10/21/what-caused-amazons-aws-outage-and-why-did-so-many-major-apps-go-offline)
- [10月20日AWS中断：DynamoDB的DNS故障如何扰乱互联网](https://medium.com/@ansababy/aws-outage-on-october-20-how-a-dns-glitch-in-dynamodb-disrupted-the-internet-40e1f0440a12)
- [更新 - AWS服务恢复正常运行](https://www.aboutamazon.com/news/aws/aws-service-disruptions-outage-update)
- [AWS服务中断——大规模故障实时更新](https://www.tomsguide.com/news/live/amazon-outage-october-2025)
