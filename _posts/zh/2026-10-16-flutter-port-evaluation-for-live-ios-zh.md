---
audio: false
generated: true
image: false
lang: zh
layout: post
title: live-ios 的 Flutter 移植评估
translated: true
type: note
---

好的——以下是我的回答。

## 这个应用属于什么类型

从 README 和代码来看，`live-ios` 本质上是一个**消费型应用**：

- **没有应用内推流**：主播将 RTMP 推流地址复制到 OBS（`ControlForm` 只有“复制推流地址/密钥”），应用本身只是通过 AVPlayer 播放 HLS/MP4
- 核心功能都是“视频播放 + 聊天 + 二维码支付 + Markdown 渲染 + 列表/表单”，外加 HTTP API 集成（`X-Session` 请求头、统一的 `status/result/error` 响应）

这正是 **Flutter 最擅长** 的领域——也是移植最省心的场景。

## 应该用 Flutter 吗？

| 你的目标 | 结论 |
| --- | --- |
| **仅 iOS** | ❌ 不要换。保留原生 SwiftUI。应用已经完整且零依赖；重写会带来体积和成本，AVPlayer 集成只会更复杂 |
| **iOS + Android，一套代码** | ✅ Flutter 非常适合 |
| **未来：应用内摄像头直播（手机直接推流）** | ⚠️ 这很复杂；建议用原生或成熟直播 SDK（腾讯/阿里云），而这是 Flutter 最薄弱的环节 |
| **Web** | 已由 H5 覆盖（`live-mobile-web`）。不要用 Flutter Web——保留 H5 |

如果需求是“双端”，Flutter 的价值很明显——而且你的项目恰好避开了 Flutter 的三大短板：

1. **视频播放**：`video_player` / `media_kit` 内部封装了 AVPlayer（iOS）和 ExoPlayer（Android），HLS 支持完全不是问题——和你现在用的引擎一样
2. **聊天**：WebSocket（`web_socket_channel`）+ 懒加载聊天列表 `ListView` 正是 Flutter 的强项
3. **二维码支付**：`qr_flutter` 生成微信收款码 + HTTP 轮询 `charges/one`——很简单

你现有的 `APIClient / JSONValue / X-Session` 层只需映射为一个约 50 行的 Dart HTTP 客户端，后端完全不用改。

## 需要注意的取舍

- **包体积**：Flutter 在 iOS 上会增加约 20–40MB（在中国 App Store 场景下比较敏感）
- **“零依赖”的特性消失**：Flutter 本身就是最大的依赖，插件数量多且良莠不齐。长列表/性能需要小心处理（使用 `ListView.builder`、懒加载）
- **微信登录 / 原生能力**：你的应用只是粘贴 sessionToken，所以连微信 SDK 都不需要——压力不大

## 我的建议

- 如果产品只面向 iOS，或者你只是把这当作 Web 版的一次性 iOS 复刻 → **不要换，保留 SwiftUI**
- 如果你确定要做 iOS + Android，并且接受依赖和体积成本 → **是的，用 Flutter**，把播放、聊天、二维码支付和 Markdown 的 UI 语义直接移植过去

我可以先搭一个当前 UI 的 Flutter 原型（列表 → 直播简介 → 播放器/聊天/支付），让你快速验证体验。要我试试吗？
