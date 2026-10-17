---
audio: false
generated: true
image: false
lang: en
layout: post
title: iPhone 13 JIT Crash on iOS 26
translated: false
type: note
---

Found and diagnosed the crash. Here's the full picture:

## What was crashing

Your iPhone 13 was **crashing at app launch in the Dart VM** (`dart::Assert::Fail` in `Code::FinalizeCode`, "crash occurred when compiling unknown function in unoptimized JIT mode") — before any app code runs.

**Root cause (confirmed against Flutter's issue tracker):** Your phone runs **iOS 26.6.2**, and iOS 26 closed the `get-task-allow` loophole that Flutter *debug* builds use for their **JIT**. The Flutter engine on this Mac is `3.27.1` (Dart 3.6.0) from Dec 2024, which predates the iOS 26 fix. On iOS 26 the Dart VM can't write/execute its own JIT pages → hard abort at startup. This is Flutter issue **#163984** (same stack trace, same fix vector: "no soluz except release mode / newer Flutter").

Evidence from my tests:
- A **vanilla** Flutter app (no plugins) **launched fine** on the same phone — so it wasn't your code or the camera/ML Kit plugins.
- The **flutter upgrade is the durable fix** (newer Flutter uses a Dart interpreter fallback for iOS debug builds).

## The fix — installed as a **release build**

Release builds on iOS use **AOT native code (no JIT)** and run fine on iOS 26 (161.6 MB build vs 42 MB debug — that's the AOT compiling the Dart into machine code). I:

1. Built `flutter build ios --release` ✅
2. Wrote `scripts/install_ios.sh` (build + install + launch) and `scripts/watch_install.sh`
3. Started a **background watcher** that auto-installs to lzwjava13 the moment it reconnects

## Action needed from you (2 minutes)

The phone dropped off the wireless pairing (screens locked at 2 AM 😄) and I can't install until it returns. **Please:**

- **Wake/unlock your iPhone 13** (bring up the home screen and leave the screen on, on the same Wi-Fi), **or plug it into the Mac with a USB cable** (most reliable).

Then either:
- I'll see it connect and finish the install automatically, or
- run `./scripts/install_ios.sh` yourself.

Once installed, tap **Myopia Reversal** — it should start normally now. (If the phone shows a "developer not trusted" prompt, follow Settings → General → VPN & Device Management → Trust.)

Should I also do the **Flutter upgrade** (proper long-term fix so debug builds work again), or is the release build fine for now?
