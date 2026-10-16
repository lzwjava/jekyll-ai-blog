---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 保留SRS，跳过直播流API
translated: true
type: note
---

简短回答：**不适合这个应用，现在不行。** Live Stream API 是个好产品，但它的模型与趣直播的工作方式相冲突。我把它和你的代码做了对比：

## 为什么它不适合这里

| 你目前的应用 | Live Stream API |
| --- | --- |
| `live` 行随时创建；主播获得**每场直播的 `rtmpKey`** 并立即用 OBS 推流 | 频道 + 输入端点属于**预置资源**。预置需要几分钟；你得为每场讲座 `POST` 创建频道，等待 `ACTIVE`，然后推流，再停止 |
| 多场同时进行的讲座 | 默认项目配额只允许**少量并发频道** → 在增长之前你需要申请配额提升 |
| Web 桌面端播放 **HTTP-FLV**（`flv.js`），iOS 播放 **RTMP** | 输出**仅 HLS/DASH** — 不支持 FLV、RTMP 播放。你需要修改 `live-web` 客户端，而且原生 iOS 应用会失去它的 `rtmpUrl` |
| `on_publish` 鉴权钩子（拒绝未知流密钥），`on_dvr` → `recorded_video` 行 | **完全没有 webhook。**没有推流鉴权回调，没有 DVR 回调。回放功能必须围绕“live-to-VOD → GCS → 轮询文件”重新构建 |
| 随机的多行 `hlsUrls` 故障转移 | 单一输出路径（GCS + Media CDN） |
| 成本：你的 VM 已存在，SRS 增加约 0 边际成本 | 频道预置/运行期间**按输入小时计费** + GCS 写入 + 传输出口流量 |
| 即时推流 → 观众约 1–3 秒内看到流（FLV） | 基于分段的封装，通常延迟约 6–30 秒 |

所以采用它意味着：用 PHP 编写频道生命周期管理器（每场讲座创建/预置/轮询/停止）、IAM 服务账号、配额申请、Media CDN 配置、移除所有钩子逻辑，并重写两个前端 + iOS 播放。那是一个多天的项目，而且是在*替换*可用的功能，而不是增加功能。

## 以后它在什么情况下*才*有意义

- 你超出了单个 e2-medium VM 的规模，并希望有托管式 ABR 转码（SRS `copy` 只给观众一个码率版本——这是主要的实际功能差距）。
- 你想要 Google 级的可靠性/运维，而不是自托管 SRS。
- 非交互式、高价值的广播（如 webinar），30 秒延迟可以接受。

## 建议

坚持原计划：**在你的 VM 上运行 SRS → 通过 nginx 提供 HTTPS 播放 → 重新指向 `LiveDao` → 验证。** 它复用了你现有的钩子、DVR、FLV/RTMP/HLS 播放器以及每场讲座的流密钥，客户端零改动，而且只需要大约一小时的工作，而不是几天。如果以后确实需要转码的多码率输出，你甚至可以从 SRS 进行 SRT/RTMP 转发到托管服务——但那是 Phase 6 的决定，完全可以逆转，因为前端从 API 读取 URL。

我正在进行到验证 SRS 钩子响应语义的中间阶段（已确认：允许 = body 为 `0`，拒绝 = 任何其他 JSON；钩子以 **JSON** 形式 POST，所以我会让 `LiveHooks` 健壮地从表单或 body 中读取 JSON）。

**继续实施 SRS 吗？**
