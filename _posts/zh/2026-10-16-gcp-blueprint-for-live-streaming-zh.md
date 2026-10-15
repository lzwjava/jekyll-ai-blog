---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GCP直播蓝图
translated: true
type: note
---

是的——谷歌云（Google Cloud）对这个场景来说是一个靠谱的选择。它的**Premium Tier全球网络**实际上是亚太地区覆盖最好的之一，而且它有**香港区域**，非常适合你的应用（到中国大陆、东南亚和美国西部的延迟都很理想）。但有几个需要注意的地方，你必须在架构设计时考虑进去：

## GCP用于类似RED的应用时的注意事项

1. **没有中国大陆区域**（AWS/Azure也一样——只有阿里云、腾讯云、华为云有）。中国大陆用户通过香港、东京、新加坡的接入点连接。
2. **谷歌在中国大陆被屏蔽**——所以中国大陆用户无法使用Firebase、Google Fonts、reCAPTCHA、Google Sign-In或`storage.googleapis.com`的CDN URL。谷歌服务只能在**服务器端**使用，或者把静态资源放在你自己的域名下自托管。
3. **没有托管的直播流媒体服务**——你需要自己在Compute Engine上运行SRS（这没问题，你本来就在这样做）。回放的VOD转码可以使用Transcoder API。

## 直播服务器的具体GCP架构方案

| 层级 | 服务 |
| --- | --- |
| API + Web（nginx） | **GKE Autopilot** 或2–3台位于`asia-east2`（香港）的Compute Engine虚拟机——从虚拟机开始，更简单 |
| 全球入口 | **Global HTTP(S) Load Balancer + Cloud CDN**——全球一个anycast IP，边缘节点终结TLS，缓存静态资源和API GET请求 |
| MySQL | **Cloud SQL for MySQL**（香港高可用）——替代你docker化的MySQL 5.7；后续可加只读副本 |
| Redis | **Memorystore for Redis** |
| 回放VOD、图片 | **Cloud Storage**（`multi-region`或香港bucket）+ 前置Cloud CDN——回放以HLS形式通过CDN分发 |
| 直播推流/源站 | **GCE上的SRS**：1台香港虚拟机（源站）+ 可选1台`us-west1`/`europe-west1`虚拟机（就近推流入站，中继到香港）；通过CDN化的HLS播放 |
| 前端（live-mobile-web） | **Cloud Storage静态网站** 或 Cloud Run，放在同一个负载均衡器后面 |

**延迟链路：** 主播推RTMP → 就近的SRS入站节点 → 香港源站 → 转码HLS → Cloud CDN边缘节点 → 观众（2–5秒延迟，且源站不产生跨太平洋流量费用）。

## 成本说明

- 出站流量约$0.08–0.12/GB（与AWS大致相同）；Cloud CDN有免费额度，缓存回源价格比从源站直接出流量更便宜。
- **值得申请Google for Startups**——符合条件的初创企业最高可获得$20万美元的云额度；足够覆盖这套架构一年。
- 如果预算是首要考虑因素，而且你不需要托管服务：一台香港VPS（Hetzner香港 / Vultr香港）+ Cloudflare免费CDN可以以约$10/月的成本完成迁移路线的第1–3步。

## 结论

- **选择GCP的条件：** 你想要托管的数据库/Redis、良好的亚太网络，并且计划扩展API层。以**香港（`asia-east2`）**为主部署区，Cloud CDN全球分发，SRS源站放在香港。
- **选择AWS的条件：** 你想要托管的直播视频服务（MediaLive），或者预计会有企业/合规类客户。
- **两者都不选的条件：** 你只是想低成本地做到"大致全球化"——先用VPS + Cloudflare，等有真实流量后再迁移到GCP。

GCP路线不需要重写你的PHP应用——docker-compose几乎可以1:1映射（Cloud SQL ↔ 你的`database`服务，Memorystore ↔ `redis`），所以迁移主要是基础设施配置层面的工作。

需要我为这条路线起草部署配置吗——比如，为GKE或虚拟机 + Cloud SQL方案编写`cloudbuild.yaml`/Terraform配置，以及多区域SRS推流入站/中继配置？
