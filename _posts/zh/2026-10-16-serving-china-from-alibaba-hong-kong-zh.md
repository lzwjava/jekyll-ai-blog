---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从阿里巴巴香港服务中国
translated: true
type: note
---

Alibaba Cloud with a **Hong Kong origin (`cn-hongkong`)** is arguably an even better fit than GCP for your app — because your user base and payment/SMS integrations are China-centric, and Alibaba's cross-border network to mainland China is the best in the business. This is the classic "serve mainland users without ICP" architecture.

## Where Alibaba Cloud wins vs GCP

| 方面 | 阿里云香港 | GCP香港 |
| --- | --- | --- |
| 中国大陆延迟 | 业界领先 — 阿里云骨干网 + 可选 **CN2 GIA / Global Accelerator** 线路到大陆 | 尚可，但跨境对等互联依赖公共传输质量 |
| 托管直播 | **Apsara Video Live（阿里云视频直播）** — 托管式推流/转码/CDN，可以淘汰SRS | 无 — 需自建SRS |
| 支付/短信 | 一流的支付宝、微信支付、国内短信/OTP | 支付宝需自行集成；短信仍需国内服务商 |
| 计费/账单 | 人民币发票、国内支持 | 美元、国际支持 |
| 大陆CDN节点 | 有 — **但需ICP备案**（见下文） | 完全没有大陆节点 |
| 全球覆盖（美欧边缘） | 较小，亚洲以外较弱 | 强得多 |

## Concrete blueprint — Alibaba HK origin

| 层级 | 服务 |
| --- | --- |
| API + Web（nginx/PHP） | `cn-hongkong` 的 **ECS**（如需扩容可用 **ACK** 容器集群） |
| 全球入口 | 香港的 **ALB** + 可选 **Global Accelerator（GA）** — GA 通过阿里云国内线路为大陆用户提供稳定、快速的入口IP，对跨境访问提升显著 |
| MySQL | **RDS for MySQL** 高可用版（替代 Docker 化的 MySQL 5.7） |
| Redis | **Tair / ApsaraDB for Redis** |
| 回放视频/图片 | 香港 **OSS** 存储桶 + **Alibaba CDN** |
| 直播 | 选择 **Apsara Video Live**（托管式：推流域名 → 转码 → 播放域名经CDN分发，完全不用SRS）**或** 在ECS上保留SRS作为源站 + Alibaba CDN进行HLS分发 |
| 前端静态资源 | OSS静态托管 + CDN |
| 短信/OTP | **Alibaba Cloud SMS**（国内+国际模板）— 可部分替代Supabase短信通道服务大陆用户 |

**流程：** 主播推RTMP到最近的接入点（Apsara Live也有海外接入节点）→ 香港源站 → HLS → CDN边缘 → 观众。

## The compliance gotchas (important, different from GCP)

1. **香港托管：无需ICP备案。** 网站/API/回放存储桶从香港提供服务无需ICP。这正是选择香港源站的意义。
2. **但大陆CDN节点需要ICP。** 如果为你的域名启用阿里云CDN *大陆境内* 节点，必须有ICP。无ICP时，将CDN限制为 **海外/香港/台湾节点** — 大陆观众从香港边缘节点获取内容（依然快速，但不如国内PoP节点快）。
3. **跨境数据（PIPL）。** 将大陆用户（+86手机号、支付信息）的个人信息存储在香港 = 跨境数据传输。需要用户同意 + 法律依据（标准合同备案）。中国大陆用户个人数据仅保留在香港区域，不要随意复制。
4. **直播许可证。** 如果大陆用户既开播又观看，**《网络表演经营许可证》**/相关许可证适用于*面向*大陆用户的服务，无论服务器在哪里。针对大陆用户变现的平台会面临实际执法 — 如果收费（你确实收费：付费课程+打赏），需考虑这一点。

## Verdict

- **如果应用核心市场是中国+亚洲（+一般全球用户）：选择阿里云，香港源站。** 单厂商集成栈（ECS + RDS + OSS + Apsara Live + GA）一致性强，支付宝/短信接入简单，无需ICP即可获得最佳大陆延迟。这是国内应用发布"国际版"的标准做法。
- **在前面加一层Cloudflare**（API域名开橙色云），如果也想获得廉价的美欧边缘缓存 — 混用没问题：Cloudflare缓存你的静态资源和HLS，源站留在香港。
- **只有当**你的主要市场在美欧、中国只是次要市场时才选GCP/AWS — 这种情况下阿里云的大陆优势对你并不重要。

成本说明：香港区域定价比阿里云大陆区域高约30–50%；GA和CN2跨境流量是成本大头 — 先用纯香港ECS + 仅海外CDN起步（小规模架构约$30–60/月），只有确认大陆延迟确实成问题时再增加GA。

需要我编写具体的迁移配置吗 — docker-compose → 阿里云香港（ECS启动脚本 + RDS/OSS环境变量）、SRS（或Apsara Live）推流/播放域名配置，以及限制为海外节点的阿里云CDN配置？
