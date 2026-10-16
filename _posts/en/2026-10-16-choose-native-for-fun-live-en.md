---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choose Native for Fun Live
translated: false
type: note
---

Question: **How should you choose between SwiftUI and Flutter for Fun Live’s `live-ios` app?**

Answer: **For Fun Live specifically, I would choose native Swift + Kotlin rather than Flutter if you are rebuilding it today.**

The key reason is that **AI changes the economics of maintaining two native codebases**.

### My choice

| | SwiftUI + Kotlin/Jetpack Compose | Flutter |
|---|---|---|
| iOS | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Android | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Native video/audio | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| WeChat/payment/native SDKs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| UI consistency | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Code sharing | ❌ | ⭐⭐⭐⭐⭐ |
| AI-assisted development | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Long-term platform compatibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Your particular app | **Best** | Good |

The important change is this:

> **You no longer need to optimize primarily for human developer hours. Optimize for product quality + AI leverage.**

You can have Claude/Codex/etc. generate a lot of the Android implementation from the Swift implementation. The duplicated code isn't necessarily duplicated *human effort* anymore.

For example:

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

### Why I would lean native for Fun Live

Your app isn't really a "cross-platform UI problem."

It's fundamentally:

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

The hardest/most valuable component is **video consumption**, and native APIs are already excellent.

Your iOS implementation can be very small:

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

Android is equally straightforward:

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

And your real reusable layer should be **the protocol**, not necessarily the UI framework:

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

That's a much healthier architecture for a product like Fun Live.

### But there is one situation where I'd choose Flutter

If your actual goal is:

> **"I want to rebuild Fun Live extremely quickly with one person, validate the product, and don't care much about native polish initially."**

Then:

**Flutter wins.**

You could probably get:

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

working very quickly.

And because you already have the backend/API, Flutter is unusually suitable for this particular app.

But I wouldn't choose Flutter merely because "iOS + Android = cross-platform."

### The bigger strategic decision

For Fun Live, I think the more important question is:

```text
Do we optimize for
        ↓
        ↓
fastest MVP
        OR
        ↓
long-lived global developer platform?
```

If Fun Live is becoming the **China ↔ global developer knowledge/community platform** you've been discussing, I would build the mobile clients as first-class native apps:

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

That gives you maximum freedom later for **camera streaming, push notifications, background playback, downloads, AirPlay/Cast, native sharing, App Clips/Android equivalents, payments, and platform-specific features**.

So my ranking for *your* situation is:

**1. SwiftUI + Jetpack Compose — best long-term**
**2. Flutter — best if speed/one-codebase dominates**
**3. React Native — I wouldn't pick it for this app**

And I would **not rewrite the existing iOS app just to use Flutter**. Keep the current Swift app as the reference implementation, then build Android natively if/when Android demand justifies it.

I can also map your existing `live-ios` architecture into a **shared API/domain model + SwiftUI + Compose structure**, which would give you a concrete migration plan without rewriting the backend.
