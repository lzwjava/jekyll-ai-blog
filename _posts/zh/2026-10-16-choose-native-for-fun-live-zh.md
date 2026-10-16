---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 趣直播
translated: true
type: note
---

**你应当如何在 SwiftUI 和 Flutter 之间为趣直播的 `live-ios` 应用做选择？**

**具体到趣直播，如果今天重建，我会选择原生 Swift + Kotlin，而不是 Flutter。**

关键原因是：**AI 改变了维护两套原生代码库的成本结构。**

### 我的选择

|  | SwiftUI + Kotlin/Jetpack Compose | Flutter |
|---|---|---|
| iOS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Android | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 原生视频/音频 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 微信/支付/原生 SDK | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| UI 一致性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 代码共享 | ❌ | ⭐⭐⭐⭐⭐ |
| AI 辅助开发 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 长期平台兼容性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 你的特定应用 | **最佳** | 良好 |

重要的变化是：

> **你不再需要主要为了人类开发者的工时而优化。请为产品质量 + AI 杠杆效应而优化。**

你可以让 Claude/Codex 等从 Swift 实现生成大量 Android 实现。重复的代码不再意味着重复的*人力*。

例如：

```text
                    Fun Live
                       │
              ┌────────┴────────┐
              │                 │
           Backend           API model
              │                 │
       ┌──────┴──────┐    ┌─────┴─────┐
       │             │    │           │
    SwiftUI       Compose  Swift     Kotlin
       │             │    │           │
    AVPlayer      ExoPlayer│           │
       │             │    │           │
       └─────────────┴────┴───────────┘
                       │
                Same product semantics
```

你的应用其实不是一个“跨平台 UI 问题”。

它本质上是由以下部分组成的：

```text
HLS/MP4
  +
AVPlayer / ExoPlayer
  +
WebSocket chat
  +
QR payment
  +
Markdown
  +
native platform UI
```

最困难/最有价值的部分是**视频消费**，而原生 API 已经非常出色。

你的 iOS 实现可以非常精简：

```swift
struct LiveRoomView: View {
    let room: LiveRoom

    var body: some View {
        ScrollView {
            VideoPlayer(player: AVPlayer(url: room.playURL))
            ChatView(roomID: room.id)
            DonationView(roomID: room.id)
        }
    }
}
```

Android 也同样直接：

```kotlin
@Composable
fun LiveRoom(room: LiveRoom) {
    Column {
        Player(url = room.playUrl)
        Chat(room.id)
        Donation(room.id)
    }
}
```

你真正可复用的抽象层应该是**协议（protocol）**，而不一定是 UI 框架。

```text
                    API
                     │
          ┌──────────┴──────────┐
          │                     │
     Swift models          Kotlin models
          │                     │
     LiveRoom               LiveRoom
     User                   User
     Message                Message
     Charge                 Charge
          │                     │
       SwiftUI              Compose
```

对于趣直播这样的产品，这是一个健康得多的架构。

### 但有一种情况我会选择 Flutter

如果你真正的目标是：

> **“我想以一个人极快地重建趣直播，验证产品，并且初期不太在意原生打磨。”**

那么：

**Flutter 会胜出。**

你可能很快就能实现：

```text
login
  ↓
live list
  ↓
live room
  ├── HLS player
  ├── chat
  ├── markdown
  └── QR payment
```

并且很快跑通。

而且因为你已经有后端/API，Flutter 对于这个特定应用特别合适。

但我不会仅仅因为“iOS + Android = 跨平台”就选择 Flutter。

### 更大的战略决策

对于趣直播，我认为更重要的问题是：

```text
Do we optimize for
        ↓
        ↓
fastest MVP
        OR
        ↓
long-lived global developer platform?
```

如果趣直播正在成为你一直在讨论的**中国 ↔ 全球开发者知识/社区平台**，那么我会将移动客户端构建为一流的原生应用：

```text
                 Fun Live
                    │
        ┌───────────┼───────────┐
        │           │           │
       Web        iOS       Android
        │           │           │
       H5         Swift       Kotlin
        │           │           │
        └───────────┴───────────┘
                    │
             unified backend
                    │
          ┌─────────┴─────────┐
          │                   │
       Chinese            Global
       creators            creators
          │                   │
          └──── AI translation┘
```

这会让你日后在**摄像头推流、推送通知、后台播放、下载、AirPlay/Cast、原生分享、App Clips/Android 对应功能、支付以及平台特定功能**方面拥有最大的自由。

所以，针对*你的*情况，我的排序是：

**1. SwiftUI + Jetpack Compose — 长期最佳**
**2. Flutter — 如果速度/单一代码库占主导则为最佳**
**3. React Native — 我不会为这个应用选择它**

而且我**不会仅仅为了使用 Flutter 而重写现有的 iOS 应用**。保留当前的 Swift 应用作为参考实现，然后在 Android 需求证明合理时（如果真有需求）再原生构建 Android。

我还可以将你现有的 `live-ios` 架构映射为**共享 API/领域模型 + SwiftUI + Compose 结构**，这能让你在不重写后端的情况下获得一个具体的迁移计划。