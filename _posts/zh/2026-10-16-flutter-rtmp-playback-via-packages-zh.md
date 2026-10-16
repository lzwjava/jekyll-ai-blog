---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过软件包实现Flutter RTMP播放
translated: true
type: note
---

**问题**：Flutter 支持 RTMP 流式播放吗？

**回答**：

Flutter 并不原生支持开箱即用的 RTMP 播放，但通过第三方包可以得到很好的支持。以下是详细说明：

---

### ✅ RTMP 播放（播放 RTMP 流）

最佳选择是 **`media_kit`**，它在底层封装了 `libmpv`/FFmpeg，并直接支持 RTMP URL：

```dart
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';

MediaKit.ensureInitialized();
final player = Player();
final controller = VideoController(player);

// Play an RTMP stream
player.open(Media('rtmp://your-server/live/stream-key'));
```

`media_kit` 是适用于 Flutter 和 Dart 的跨平台视频与音频播放器，支持跨平台的视频和音频播放。

**注意：** Flutter 官方的 `video_player` 插件并不原生支持 RTMP —— 它最适合 HLS/DASH/MP4。对于 HLS 流播放，推荐使用 `video_player` 或 `media_kit` 等包；但针对 RTMP 而言，`media_kit` 是更强的选择。

---

### ✅ RTMP 推流（发送/广播流）

用于**推送**流到 RTMP 服务器（例如，来自摄像头）：

`rtmpstreamer` 包是一个适用于 Android 和 Web 的现代 Flutter RTMP 流式传输插件。在 Android 上，它通过 PedroSG94 RootEncoder 发布 RTMP；在 Web 上，它通过 WHIP 端点发布 WebRTC。

```dart
await RtmpStreamer.startStream('rtmp://<host-ip>:1935/live/test');
```

---

### ✅ Tencent Cloud Player SDK（生产级）

Tencent 的 Player SDK 在 Flutter 上提供直播视频播放能力，支持 RTMP 直播格式、在线视频 URL 播放、本地视频播放、HLS/DASH 自适应码率流，以及直播时移播放。

---

### 汇总表

| 场景 | 推荐包 | RTMP 支持 |
| --- | --- | --- |
| 播放（观看 RTMP） | `media_kit` | ✅ 通过 libmpv/FFmpeg |
| 播放（Tencent Cloud） | Tencent Player SDK | ✅ |
| 推流（摄像头直播） | `rtmpstreamer` | ✅ Android + Web |
| HLS 播放（替代方案） | `video_player` | ⚠️ 仅支持 HLS，不支持 RTMP |

低延迟直播最常见的现实方案是：**通过 RTMP 推流 → 服务端转码 → 以 HLS 分发** 给 Flutter 播放器，这样可以避免某些平台（尤其是 iOS/Web）上的 RTMP 播放限制。

---

**参考：**

- [pub.dev 上的 media_kit](https://pub.dev/documentation/media_kit/latest/)
- [pub.dev 上的 rtmpstreamer](https://pub.dev/documentation/rtmpstreamer/latest/)
- [Tencent Cloud Player SDK – Flutter](https://www.tencentcloud.com/ko/document/product/266/59808)
- [Stream Video Flutter SDK – Broadcasting](https://getstream.io/video/docs/flutter/advanced/broadcasting.md)
