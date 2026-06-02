---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source iOS Telegram Client
translated: false
type: note
---

Here's what you're looking at:

**Telegram-iOS** — the official open-source iOS client for Telegram Messenger.

**Repo:** `git@github.com:TelegramMessenger/Telegram-iOS.git`
**Size:** 572 MB on disk
**Version:** 12.7 (requires Xcode 26.2, macOS 26, Bazel 8.4.2)

**Code breakdown:**
- 4,182 Swift files (primary language)
- 901 Objective-C (.m/.mm) files

**Architecture:**

The project is built with **Bazel** via a `build-system/Make/Make.py` wrapper. It's organized into:

| Directory | Purpose |
|-----------|---------|
| `Telegram/` | Main app target, extensions (NotificationContent, Share, Watch, WidgetKitWidget, SiriIntents) |
| `submodules/` | **273 internal libraries** — the bulk of the codebase |
| `third-party/` | Vendored C/C++ deps (ffmpeg, openssl, sqlcipher, libvpx, opus, webrtc, rlottie, libjxl, dav1d, mozjpeg, libyuv) |
| `build-system/` | Bazel rules (rules_apple, rules_swift, rules_xcodeproj) and build configs |

**Key submodules** (273 total) include:
- **TelegramCore** — networking, storage, business logic
- **TelegramUI** — UI components
- **TelegramApi** — MTProto API bindings
- **Postbox** — local database (key-value store over sqlcipher)
- **TelegramCallsUI** / **TgVoipWebrtc** — voice/video calls
- **AccountContext** / **AccountUtils** — multi-account support
- **AsyncDisplayKit** — async node-based UI rendering (Texture fork)
- **Display**, **ComponentFlow** — UI framework layer

**Active refactor** (documented in CLAUDE.md): A 45+ wave effort to migrate `Postbox` direct imports to `TelegramEngine` typealiases — a clean-layering refactor eliminating direct database dependencies from consumer modules.

**Git history** (latest commits): Routine fixes, poll improvements, animation cleanup — looks like an actively maintained fork or clone of the upstream Telegram repo.

**How it builds:**
```sh
python3 build-system/Make/Make.py --overrideXcodeVersion \
  --cacheDir ~/telegram-bazel-cache \
  build \
  --configurationPath build-system/appstore-configuration.json \
  --gitCodesigningRepository git@gitlab.com:peter-iakovlev/fastlanematch.git \
  --gitCodesigningType development --gitCodesigningCurrent --buildNumber=1 --configuration=debug_sim_arm64
```

It's a massive, well-structured codebase — one of the largest open-source iOS projects out there.
