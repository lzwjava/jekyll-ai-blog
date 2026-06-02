---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 谷歌云平台重大服务中断
translated: true
type: note
---

### 事件概述
2025年6月12日，Google Cloud Platform（GCP）发生持续约7.5小时的大规模全球服务中断（太平洋夏令时10:51至18:18）。事故根源在于Google服务控制系统新功能中的程序缺陷，该缺陷涉及配额策略检查环节，导致无效的自动化配额更新在全球范围内传播，引发大规模API拒绝响应和任务过载。尤以us-central1（爱荷华州）等高流量区域受影响最为严重。此次中断导致大量GCP服务、Google Workspace产品及依赖GCP基础设施的第三方应用服务受阻，Downdetector平台收到超过140万份用户故障报告。

### 时间线
（所有时间均为太平洋夏令时PDT）

- **10:51**：故障开始，多个GCP和Google Workspace产品的外部API请求出现503错误激增，导致间歇性访问中断
- **11:46**：工程团队确认服务大面积受影响，启动根本原因调查
- **12:09**：启动缓解措施，除us-central1外大部分区域开始恢复
- **12:41**：确认根本原因为无效配额策略数据，实施配额检查绕过方案
- **13:16**：除us-central1和美国多区域外，所有区域基础设施完全恢复
- **14:00**：us-central1出现恢复迹象，预计一小时内完全缓解
- **15:16**：多数GCP产品恢复，但Dataflow、Vertex AI和个性化服务状态页面仍存在残留问题
- **17:06**：Dataflow与个性化服务状态页面问题解决，Vertex AI问题持续，预计解决时间22:00
- **18:27**：Vertex AI在所有区域完全恢复
- **18:18**：事件正式结束，所有服务完全恢复

主要缓解措施耗时约3小时，但由于积压任务和残留错误影响，总中断时长达到7.5小时。

### 根本原因
本次中断由服务控制功能（负责管理API配额与策略）的设计缺陷引发。自动化系统向数据库插入了包含空白或空值字段的无效配额策略，由于全球复制机制（旨在实现近实时一致性），这些损坏数据在数秒内蔓延至全球。当API请求触发配额检查时，导致空指针异常和请求拒绝（503与5xx错误激增）。在us-central1等大型区域，海量失败请求引发严重任务过载，并在依赖服务中产生级联故障。新功能对空白字段等边界情况缺乏充分验证，且系统未设置"故障开放"机制（即在检查失败时允许请求继续执行）。

### 受影响服务
本次中断波及大量Google产品及依赖GCP的外部服务。核心GCP与Google Workspace服务出现不同程度中断，包括API故障和界面访问问题（流媒体与IaaS资源未受影响）。

#### 主要受影响的Google Cloud产品
- **计算与存储**：Google Compute Engine、Cloud Storage、Persistent Disk
- **数据库**：Cloud SQL、Cloud Spanner、Cloud Bigtable、Firestore
- **数据与分析**：BigQuery、Dataflow、Dataproc、Vertex AI（包括在线预测和特征库）
- **网络与安全**：Cloud Load Balancing、Cloud NAT、身份与访问管理（IAM）、Cloud Security Command Center
- **开发者工具**：Cloud Build、Cloud Functions、Cloud Run、Artifact Registry
- **AI/ML**：Vertex AI Search、Speech-to-Text、Document AI、Dialogflow
- **其他**：Apigee、Cloud Monitoring、Cloud Logging、Resource Manager API

#### 主要受影响的Google Workspace产品
- Gmail、Google Drive、Google Docs、Google Meet、Google Calendar、Google Chat

#### 受影响的第三方服务
众多完全或部分依赖GCP的消费级和企业级应用出现服务中断：
- **Spotify**：约46,000用户遭遇流媒体播放和应用访问中断
- **Discord**：语音聊天和服务器连接问题
- **Fitbit**：数据同步和应用功能暂停
- **其他**：OpenAI（ChatGPT）、Shopify、Snapchat、Twitch、Cloudflare（级联DNS问题）、Anthropic、Replit、Microsoft 365（部分功能）、Etsy、Nest

由于GCP支撑着互联网后端基础设施的重要部分，全球性规模放大了本次事件的影响。

### 解决措施
Google工程团队快速定位无效策略，并实施配额检查绕过方案，允许API请求在危机期间无需验证即可执行。该措施使大部分区域在PDT 12:48前恢复。针对us-central1区域，实施了定向过载缓解措施，随后对Dataflow和Vertex AI等受影响服务进行人工积压清理。监控系统于PDT 18:18确认完全恢复。未发生数据丢失，但部分服务出现临时延迟。

### 影响范围
- **规模**：Downdetector收到超140万份报告，凸显全球实时中断影响
- **经济**：企业可能损失数十亿美元生产力，Spotify报告高峰时段用户集中投诉
- **声誉**：凸显云服务集中化风险，业界呼吁完善多云战略

### 经验总结与预防措施
Google发布详细事后分析报告，重点强调韧性建设：
- **架构调整**：模块化改造服务控制系统以实现故障隔离，启用"故障开放"模式
- **数据验证**：全局变更实施增量传播与预验证机制，增强无效输入测试
- **部署保障**：关键更新强制启用功能开关，改进静态分析与错误处理
- **监控通信**：确保中断检测工具独立运行，加速自动客户告警
- **全局优化**：在重试逻辑中引入随机退避机制防止过载级联

这些措施旨在预防类似事件，目前正持续对配额系统进行审计。

[Google Cloud事件报告](https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW)
[ThousandEyes中断分析](https://www.thousandeyes.com/blog/google-cloud-outage-analysis-june-12-2025)
[Ookla Downdetector报告](https://www.ookla.com/articles/google-cloud-outage-june-2025)
[ByteByteGo技术解析](https://blog.bytebytego.com/p/how-the-google-cloud-outage-crashed)
[Medium根本原因解读](https://medium.com/@tahirbalarabe2/%EF%B8%8Fhow-a-single-google-cloud-bug-caused-global-internet-outage-on-june-12-2025-652a83ad9e68)
