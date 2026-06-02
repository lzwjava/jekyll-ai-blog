---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS重大中断事件回顾
translated: true
type: note
---

### AWS历史上的重大中断事件

自2006年以来，亚马逊云服务（AWS）支撑着互联网的大部分运行，但如同任何大型基础设施一样，它偶尔也会面临服务中断。相对于其庞大的运营规模，中断事件并不频繁，但重大故障会产生连锁反应，波及从社交媒体到金融平台等依赖服务。下表汇总了历史上影响范围较大或冲击力较强的关键中断事件，这些事件均选自影响多服务或知名客户的记录在案案例。

| 日期              | 受影响服务/区域           | 原因                          | 影响 |
|-------------------|---------------------------|--------------------------------|--------|
| 2008年2月15日 | S3、EC2（全球）         | 未明确的技术故障 | 导致多个网站图片存储和托管服务中断，标志着AWS早期重大故障之一 |
| 2011年4月21日    | 多服务（美东-1区域） | 数据中心长时间故障 | 致使Reddit、Quora等知名网站宕机数小时，凸显早期可靠性问题 |
| 2017年2月28日 | EC2、S3、RDS等多服务（美东-1区域） | 人为失误：调试期间输错指令 | 持续数小时的中断影响Slack、Docker、Exora等平台，预估损失达数亿美元；AWS云管理控制台同时瘫痪 |
| 2021年12月7日  | EC2、RDS、Lambda等控制平面服务（美东-1区域） | 故障转移期间控制平面软件缺陷引发级联故障 | 近年历时最长的中断（8小时以上）；影响Netflix、Disney+、Capital One及政府网站；12月15日发生第二次较小规模中断影响类似服务 |
| 2023年6月13日     | EC2及相关服务（多区域） | 未明确的区域性问题 | 大规模宕机波及美联社、波士顿环球报等新闻机构及纽约大都会运输署等交通系统，持续数小时 |
| 2025年10月20日  | DynamoDB端点、EC2启动及多服务（美东-1区域，产生全球涟漪效应） | DynamoDB服务端点DNS解析失败 | 持续整日的中断（始于太平洋时间10月19日深夜，10月20日下午解决）；影响Snapchat、Reddit、Roblox、Fortnite、劳埃德银行集团、英国税务海关总署等；导致约三分之一依赖互联网的应用程序访问受阻，影响数百万用户；AWS为恢复服务限流部分操作 |

这些事件通常源于人为失误、网络问题或环境因素，AWS已通过多区域部署等冗余措施提升韧性。2025年中断事件再次凸显过度依赖AWS最繁忙区域——美东-1区域的持续风险。

延伸阅读：

- [AWS云与数据中心中断历史纵览](https://www.datacenterknowledge.com/outages/a-history-of-aws-cloud-and-data-center-outages)
- [史上最大AWS中断：2021年12月7日事件全解析](https://aws.plainenglish.io/the-biggest-aws-outage-in-history-the-december-7-2021-us-east-1-meltdown-and-lessons-learned-2efab5a02de5)
- [AWS中断事件原因探析](https://www.bbc.com/news/articles/cev1en9077ro)
- [AWS关于2025年10月中断事件的最新说明](https://www.aboutamazon.com/news/aws/aws-service-disruptions-outage-update)
