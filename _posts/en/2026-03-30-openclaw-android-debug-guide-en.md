---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Android Development and Debugging Guide
translated: false
type: note
---

**Question:** How does Android Studio work with OpenClaw using ADB, and how can one use it to build, run, and debug an Android app connected to a physical phone?

**Answer:**

## OpenClaw + Android Studio + ADB: Building, Running & Debugging on a Physical Android Phone

OpenClaw is an AI agent platform ("the lobster way 🦞") that connects to Android via ADB. Here's a comprehensive breakdown of how everything fits together.

---

### 🔍 What Is OpenClaw on Android?

OpenClaw's Android app plays the role of a **companion node** — Android does not host the Gateway itself. A Gateway is required and must run on macOS, Linux, or Windows via WSL2. The Android node app connects to the Gateway via mDNS/NSD and WebSocket (default `ws://<host>:18789`).

The Android app status is currently **extremely alpha** and is actively being rebuilt from the ground up.

---

### 📱 Step 1: Enable ADB on Your Android Phone

1. Go to **Settings → About Phone** → tap **Build Number** 7 times to enable Developer Options.
2. Go to **Settings → Developer Options** → enable **USB Debugging**.
3. Connect the phone via USB and **accept the debugging trust prompt** on the phone.

If `adb devices -l` shows `unauthorized`, re-plug the cable and accept the trust prompt again. Then use `adb reverse` so that Android's `localhost:18789` tunnels to your laptop's `localhost:18789`.

```bash
adb reverse tcp:18789 tcp:18789
```

---

### 🏗️ Step 2: Open & Build the Android App in Android Studio

Open the folder `apps/android` in Android Studio. To build and run:

```bash
cd apps/android
./gradlew :app:assembleDebug
./gradlew :app:installDebug
```

You can also run unit tests with:

```bash
./gradlew :app:testDebugUnitTest
```

`gradlew` auto-detects the Android SDK at `~/Library/Android/sdk` (macOS default) if `ANDROID_SDK_ROOT` / `ANDROID_HOME` are unset.

Alternatively, you can build the Play Store debug variant:

```bash
./gradlew :app:assemblePlayDebug
```

---

### ▶️ Step 3: Run the App on the Physical Phone

The app is **native Kotlin + Jetpack Compose**. For UI edits using **Compose**, use **Android Studio Live Edit** on a debug build — this works on physical devices and requires the project's `minSdk=31`.

There are three levels of applying changes:

| Change Type | Method |
|---|---|
| Compose UI edits | **Live Edit** (instant, no reinstall) |
| Non-structural code/resource | **Apply Changes** |
| Structural/native/manifest/Gradle | Full reinstall via `pnpm android:run` |

Canvas web content already supports **live reload** when loaded from Gateway at `__openclaw__/canvas/`.

---

### 🐛 Step 4: Debug with Android Studio

Standard Android Studio debugging tools work fully:

- **Logcat** — view real-time device logs
- **Debugger** — set breakpoints in Kotlin/Java code
- **Layout Inspector** — inspect Compose/View hierarchy live on device
- **Network Inspector** — monitor WebSocket traffic to the OpenClaw Gateway

Since the app uses Kotlin + Jetpack Compose, you can use **Android Studio Hedgehog or newer** for best Compose debugging support (Compose Preview, Live Edit, etc.).

---

### 🔌 Step 5: Connect the App to the OpenClaw Gateway

Open the **Connect** tab in the app. Use **Setup Code** or **Manual** mode to connect. The Android app pairs with the Gateway as a node device.

For the Gateway tunnel via ADB:

```bash
adb reverse tcp:18789 tcp:18789
```

This makes the phone reach your laptop's Gateway at `localhost:18789` as if it were local.

---

### 🤖 Step 6: AI-Driven App Control via ADB (DroidClaw / OpenClaw Agent)

Beyond building your own app, OpenClaw can also **control Android apps via ADB** as an AI agent:

OpenClaw acts as a bridge on the laptop, and the agent executes tasks on your Android device via ADB. The agent uses a **Perception → Reasoning → Action** loop — it dumps the phone's accessibility tree via ADB, parses the XML into interactive UI elements, and grabs a screenshot.

ClawMobile, a related project, runs OpenClaw directly on a mobile device and integrates it with **structured UI automation and deterministic mobile control layers** (ADB, Termux, and Accessibility-based tooling). This enables agents to actively manipulate apps, inspect UI state, and execute reliable, reproducible workflows — without any remote control server.

---

### 🧪 Performance Benchmarking (Bonus)

You can run macrobenchmarks (startup + frame timing) with:

```bash
cd apps/android
./gradlew :benchmark:connectedDebugAndroidTest
```

Reports are written to `apps/android/benchmark/build/reports/androidTests/connected/`.

---

### ⚠️ Important Checklist Before Running/Debugging

Before running tests or debugging:

- The Android app must be connected to the Gateway and show as **paired + connected**.
- The app must stay **unlocked and in the foreground** for the whole session.
- The **Screen tab** must be open and active if canvas/A2UI commands are needed.
- All required **runtime permissions** (camera, mic, location, notifications) must be granted.
- No interactive system dialogs should be pending before test start.

---

**References:**

- [OpenClaw Android README (GitHub)](https://github.com/openclaw/openclaw/blob/main/apps/android/README.md)
- [OpenClaw Android Docs](https://docs.openclaw.ai/platforms/android)
- [DroidClaw Guide (Medium)](https://medium.com/write-a-catalyst/from-openclaw-to-droidclaw-your-friendly-guide-to-android-ai-automation-2b17de9ed67f)
- [ClawMobile GitHub](https://github.com/ClawMobile/ClawMobile)
- [openclaw-android (AidanPark, single-command Android setup)](https://github.com/AidanPark/openclaw-android)
- [Running OpenClaw Locally on Android via Termux](https://sagartamang.com/blog/openclaw-on-android-termux)
