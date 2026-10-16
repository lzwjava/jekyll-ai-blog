---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flutter RTMP Playback via Packages
translated: false
type: note
---

**Question:** Does Flutter support RTMP streaming playback?

**Answer:**

Flutter does **not** natively support RTMP playback out of the box, but it is well-supported through third-party packages. Here's the breakdown:

---

### ✅ RTMP Playback (Playing an RTMP stream)

The best option is **`media_kit`**, which wraps `libmpv`/FFmpeg under the hood and supports RTMP URLs directly:

```dart
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

MediaKit.ensureInitialized();
final player = Player();
final controller = VideoController(player);

// Play an RTMP stream
player.open(Media('rtmp://your-server/live/stream-key'));
```

`media_kit` is a cross-platform video and audio player for Flutter & Dart, supporting both video and audio playback across platforms.

**Note:** The official `video_player` plugin from Flutter does **not** support RTMP natively — it works best with HLS/DASH/MP4. For playing HLS streams, packages like `video_player` or `media_kit` are recommended, but for RTMP specifically, `media_kit` is the stronger choice.

---

### ✅ RTMP Publishing (Sending/Broadcasting a stream)

For **pushing** a stream to an RTMP server (e.g., from camera):

The `rtmpstreamer` package is a modern Flutter RTMP streaming plugin for Android and Web. On Android it publishes RTMP through PedroSG94 RootEncoder, and on Web it publishes WebRTC through a WHIP endpoint.

```dart
await RtmpStreamer.startStream('rtmp://<host-ip>:1935/live/test');
```

---

### ✅ Tencent Cloud Player SDK (Production-grade)

Tencent's Player SDK provides video playback capabilities for live streaming on Flutter, supporting RTMP live streaming formats, URL playback for online videos, local video playback, HLS/DASH ABR streaming, and live streaming time shifting playback.

---

### Summary Table

| Scenario | Recommended Package | RTMP Support |
|---|---|---|
| Playback (watching RTMP) | `media_kit` | ✅ via libmpv/FFmpeg |
| Playback (Tencent Cloud) | Tencent Player SDK | ✅ |
| Publishing (streaming camera) | `rtmpstreamer` | ✅ Android + Web |
| HLS playback (alternative) | `video_player` | ⚠️ HLS only, not RTMP |

The most common real-world approach for low-latency live streaming is: **ingest via RTMP → transcode server-side → serve as HLS** to the Flutter player, which avoids RTMP playback limitations on some platforms (especially iOS/Web).

---

**References:**
- [media_kit on pub.dev](https://pub.dev/documentation/media_kit/latest/)
- [rtmpstreamer on pub.dev](https://pub.dev/documentation/rtmpstreamer/latest/)
- [Tencent Cloud Player SDK – Flutter](https://www.tencentcloud.com/ko/document/product/266/59808)
- [Stream Video Flutter SDK – Broadcasting](https://getstream.io/video/docs/flutter/advanced/broadcasting.md)
