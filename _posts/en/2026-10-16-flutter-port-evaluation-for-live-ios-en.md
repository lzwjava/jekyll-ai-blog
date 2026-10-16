---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flutter Port Evaluation for live-ios
translated: false
type: note
---

Got it — here's my answer in English.

## What kind of app this is

From the README and code, `live-ios` is fundamentally a **consumption-style app**:

- **No in-app broadcasting**: streamers copy RTMP push URLs to OBS (the `ControlForm` only has "copy push URL / key"), and the app itself just plays HLS/MP4 via AVPlayer
- Core features are all "video playback + chat + QR payment + Markdown rendering + lists/forms" plus HTTP API integration (`X-Session` header, uniform `status/result/error` responses)

This is exactly the territory **Flutter is best at** — and the least painful scenario to port.

## Should you use Flutter?

| Your goal | Verdict |
|---|---|
| **iOS only** | ❌ Don't switch. Keep native SwiftUI. The app is already complete with zero dependencies; rewriting adds size and cost, and AVPlayer integration only gets more convoluted |
| **iOS + Android, one codebase** | ✅ Flutter is a great fit |
| **Future: in-app camera broadcast (phone pushes stream directly)** | ⚠️ That's complex; prefer native or a mature live-streaming SDK (Tencent/Aliyun), where Flutter is weakest |
| **Web** | Already covered by H5 (`live-mobile-web`). Don't use Flutter Web — keep the H5 |

If the requirement is "both platforms," Flutter's value is clear — and your project conveniently avoids Flutter's three biggest weaknesses:

1. **Video playback**: `video_player` / `media_kit` internally wrap AVPlayer (iOS) and ExoPlayer (Android), so HLS support is a non-issue — same engine you use today
2. **Chat**: WebSocket (`web_socket_channel`) + a lazy chat `ListView` is a Flutter sweet spot
3. **QR payment**: `qr_flutter` generates the WeChat QR code + HTTP polling of `charges/one` — trivial

Your existing `APIClient / JSONValue / X-Session` layer maps to a ~50-line Dart HTTP client. No backend changes needed at all.

## Trade-offs to watch

- **Binary size**: Flutter adds roughly 20–40MB on iOS (sensitive in China App Store scenarios)
- **The "zero dependency" property disappears**: Flutter itself is the biggest dependency, and plugins are numerous and varied. Long list/performance needs care (use `ListView.builder`, lazy loading)
- **WeChat login / native capability**: your app just pastes a sessionToken, so you don't even need the WeChat SDK — low pressure

## My recommendation

- If the product targets iOS only, or if you treat this as a one-off iOS replica of the web version → **don't switch, keep SwiftUI**
- If you're committed to iOS + Android and accept the dependency and size cost → **yes, go Flutter**, porting the UI semantics of playback, chat, QR pay, and Markdown directly

Happy to scaffold a Flutter version of the current UI (list → live intro → player/chat/pay) so you can validate the feel quickly. Want me to try it?
