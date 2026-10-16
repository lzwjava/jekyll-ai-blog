---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flutter Builds Web and Desktop Apps
translated: false
type: note
---

**Question:** Can Flutter also build web or desktop versions of an app?

**Answer:**

**Yes!** Flutter is a true **6-platform framework** — one codebase can target all of these:

---

### 📱 Mobile

- Android
- iOS

### 🌐 Web

- Runs in any modern browser
- Two rendering modes:
  - **HTML renderer** — lighter, better SEO, standard DOM
  - **CanvasKit (WebAssembly)** — pixel-perfect, same look as mobile, heavier

### 🖥️ Desktop (Native Apps)

Flutter provides support for compiling a **native Windows, macOS, or Linux** desktop app. Flutter's desktop support also extends to plugins — you can install existing plugins that support these platforms, or create your own.

To enable desktop targets:

```bash
flutter config --enable-windows-desktop
flutter config --enable-macos-desktop
flutter config --enable-linux-desktop
```

To add desktop to an existing project:

```bash
flutter create --platforms=windows,macos,linux .
```

---

### The "Write Once, Run Everywhere" Reality

The Flutter team's goal was to build this in a way that there would be **one Flutter codebase** with no need to fork the framework or the applications to support different platforms.

Businesses can optimize resource allocation, accelerate time-to-market, and maintain high-quality standards across mobile, web, and desktop platforms — with a single team able to handle multiple platforms.

---

### ⚠️ Caveats to Know

| Platform | Maturity | Notes |
| --- | --- | --- |
| Android / iOS | ⭐⭐⭐⭐⭐ | Production-proven |
| Web | ⭐⭐⭐⭐ | Good for SPAs/dashboards; SEO tricky with CanvasKit |
| Windows | ⭐⭐⭐⭐ | Stable |
| macOS | ⭐⭐⭐⭐ | Stable |
| Linux | ⭐⭐⭐ | Stable but less tested in production |

This is exactly why Xianyu uses Flutter for the **mobile app** but a separate React web stack for `goofish.com` — Flutter Web is great for app-like experiences, but for SEO-heavy e-commerce product listing pages, traditional HTML frameworks still have an edge.

---

**References:**

- [Flutter Desktop Support – flutter.dev](https://docs.flutter.dev/platform-integration/desktop)
- [Flutter Web Support – flutter.dev](https://docs.flutter.dev/platform-integration/web)
- [Flutter Development Trends 2026](https://www.monterail.com/blog/flutter-development-trends)
