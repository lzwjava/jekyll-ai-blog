---
audio: false
generated: true
image: false
lang: en
layout: post
title: LiveIos SwiftUI Port Complete
translated: false
type: note
---

Done. I built **LiveIos** — a complete Swift/SwiftUI native port of `live-mobile-web` in `/Users/lzwjava/projects/live-ios`. It builds with **zero warnings** and runs in the iOS Simulator without crashes.

## What was created

**~3,500 lines across 27 files**, zero third-party dependencies, Xcode project (objectVersion 77, folder-synced):

| Area | Files | Matches Web |
|---|---|---|
| 直播列表 | `LiveListView` | 最新/热门直播 tabs, status tags, 参与人数, price (ListView) |
| 直播介绍 | `LiveIntroView` | cover, 主播信息, 参与/邀请榜, 主播简介, 详情, 须知, 更多直播, 报名/付费 (IntroView) |
| 直播间 | `LiveRoomView` + `ChatView` | AVPlayer **HLS/MP4** live+回放, 倒计时, 公告/聊天 tabs, 关注, 切换线路, 打赏 (LiveView) |
| 其他 | UsersView / UserRoomView / ProfileView / MyLivesView / SettingsView | 观众列表, 用户直播间, 个人中心, 我的直播, 服务器配置 |
| 基础设施 | `APIClient`, `API`, `AuthStore`, `ImageStore`, `MarkdownRenderer`, `Formatters`, `ChatService` | api.js 对齐: `status/result/error`, 表单 POST, `X-Session` 头, util.js 时间/文案/金额 |

## Key decisions

- **原后端已死** — `api.quzhiboapp.com` 现在是 NXDOMAIN（我实测过）。App 的 API 地址可在「设置 → 服务器」随时改指新的 `live-server` 部署（接口路径/格式/登录头与 Web 版完全一致），网络失败时给出友好错误和重试。
- **支付** — 付费报名/打赏通过 `wechat_qrcode` channel 生成二维码，本地 `CIQRCodeGenerator` 渲染，轮询 `charges/one` 确认到账（同 QrcodePayForm）。
- **聊天** — 原版依赖 LeanCloud 实时通讯（WS+protobuf，云端已失效）。我抽取了 `ChatService` 协议 + 演示实现，UI/业务完整，接入新即时通讯只需实现该协议。
- **登录** — Web 是微信 OAuth；原生端改为粘贴 sessionToken 登录。

## Run it

```bash
xcodebuild -project LiveIos.xcodeproj -scheme LiveIos \
  -destination 'platform=iOS Simulator,name=iPhone 17' build
```

It's already installed and running in the booted "iPhone 17" simulator (PID 51600).
