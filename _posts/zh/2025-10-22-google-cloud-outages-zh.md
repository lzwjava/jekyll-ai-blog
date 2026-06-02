---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 谷歌云平台重大服务中断事件
translated: true
type: note
---

### Google Cloud Platform (GCP) 重大故障史

自早期发展以来，Google Cloud Platform 经历了多次重大故障，通常由软件缺陷、硬件故障、环境因素或容量问题引起。下表汇总了部分最引人注目的事件，这些事件因其规模、持续时间或广泛影响而被选出。这些记录截至 2025 年中期。

| 日期 | 原因 | 影响 |
|------|--------|--------|
| 2020 年 12 月 14 日 | 中央用户 ID 管理系统容量意外缩减，影响基于 OAuth 的身份验证。 | 全球中断约 90 分钟；全球数百万用户的 Gmail、YouTube、Google Drive、GCP 服务及 Pokémon GO 等应用访问受阻。 |
| 2022 年 7 月 | 伦敦超过 40°C 的极端热浪导致 europe-west2-a 区域冷却系统故障。 | 区域中断约 24 小时；影响 Cloud Storage、BigQuery、Compute Engine、GKE 等服务，迫使故障转移至其他区域。 |
| 2022 年 8 月 8 日 | 爱荷华州康瑟尔布拉夫斯数据中心发生电气事故引发火灾（与并发的搜索/地图问题无关）。 | 局部火灾响应；Cloud Logging 服务全球延迟持续数天，影响 GCP 用户的监控和调试。 |
| 2023 年 4 月 28 日 | 巴黎数据中心进水和火灾，引发 europe-west9-a 区域多集群故障。 | 欧洲、亚洲、美洲广泛中断；VPC、负载均衡、BigQuery 及网络服务受影响数小时至数天。 |
| 2024 年 8 月 7-8 日 | 在 Vertex AI 的 API 启用期间，Cloud TPU 服务激活失败。 | 全球中断约 14 小时；阻塞所有主要区域的 Vertex AI 机器学习模型上传和训练。 |
| 2024 年 10 月 23 日 | europe-west3-c 区域（法兰克福）电力故障和电弧，导致冷却基础设施性能下降。 | 区域中断半天（约 8 小时）；基础设施部分关闭，流量转移至其他区域。 |
| 2025 年 1 月 7-8 日 | 互联问题包括 Apigee 中的 SAML 身份验证失败、Vertex Gemini API 中的 HTTP 错误以及 Pub/Sub 中的发布阻塞。 | 超过 18 小时的多小时中断；影响跨区域的 API 管理、AI 推理和实时消息传递。 |
| 2025 年 6 月 12 日 | 新 Service Control 功能（配额策略检查）中的错误导致 us-central1 等大区域任务过载。 | 全球中断约 7 小时；导致 Spotify、Discord、Fitbit 及许多依赖 GCP 的服务瘫痪，报告数量超过 140 万。 |

这些事件凸显了 GCP 的发展阵痛，从 2000 年代末的早期 App Engine 问题到近期的系统性故障。Google 通常会发布事后分析和补救计划，例如将组件模块化以“故障开放”。有关最新状态，请查看 [Google Cloud Service Health](https://status.cloud.google.com/)。

[Google Cloud 和数据中心故障史](https://www.datacenterknowledge.com/outages/a-history-of-google-cloud-and-data-center-outages)
[Google 服务中断 - 维基百科](https://en.wikipedia.org/wiki/Google_services_outages)
[Google Cloud 故障历史 | StatusGator](https://statusgator.com/blog/google-cloud-outage-history/)
[2025 年至今十大云中断事件 - CRN](https://www.crn.com/news/cloud/2025/the-10-biggest-cloud-outages-of-2025-so-far)
[Google Cloud 故障分析：2025 年 6 月 12 日 - ThousandEyes](https://www.thousandeyes.com/blog/google-cloud-outage-analysis-june-12-2025)
