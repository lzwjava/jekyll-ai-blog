---
audio: false
generated: true
image: false
lang: en
layout: post
title: iPhone Smoothness Beyond Raw Hardware
translated: false
type: note
---

**Question:** Why does the iPhone X feel smoother than the Google Pixel 7, even though the Pixel 7 has a newer, faster chip?

**Answer:**

This is a classic perceived smoothness question. It comes down to several compounding factors, not just raw hardware.

## 1. VSYNC and Frame Pacing

iPhone X runs at **60Hz**, but Apple's rendering pipeline is extremely disciplined about hitting that 60fps target with consistent frame timing. A perfectly paced 60fps *feels* smoother than an inconsistently paced 90/120fps because **jank** (frame time variance) is what your eye actually perceives as stuttering.

Pixel 7's display runs at **90Hz**, but Android's frame scheduler has historically been looser. A frame that takes 15ms instead of 11.1ms causes a visible stutter even at 90Hz. Google has improved this, but Apple's pipeline is tighter end-to-end.

## 2. Touch Latency — The Real Killer

Apple's secret weapon is **touch sampling and input latency**:

- iPhone X has a **touch sampling rate of 120Hz** (double the display refresh rate)
- The touch controller is co-designed with the SoC — no third-party touch IC latency
- Apple processes touch input on a **dedicated low-latency path**, decoupled from the main render pipeline

Pixel 7 (Tensor G2): touch sampling is at display refresh rate (90Hz), and input goes through Android's `InputDispatcher` → `ViewRootImpl` → `Choreographer` pipeline, adding latency at each hop.

The result: iPhone X has roughly **~30-40ms** touch-to-pixel latency vs Android's often **~60-80ms**. That difference is *felt*, not just measured.

## 3. Core Animation vs Android's Render Thread

iOS uses **Core Animation**, which runs on a dedicated **render server** (`backboardd`/`SpringBoard`) separate from the app process:

```
App process → commits CA transaction → Render Server composites → GPU → display
```

Even if your app's main thread is busy, animations keep running on the render server at full frame rate. Scroll animations, spring physics, transitions — all fire-and-forget from the app's perspective.

Android's equivalent is the **RenderThread** (added in Android 5), but it's in-process and more tightly coupled to the app lifecycle. Jank in one layer can propagate.

## 4. ProMotion vs Fixed Refresh — but inverted here

Ironically, iPhone X doesn't have ProMotion (that came with iPhone 13 Pro). So the Pixel 7's 90Hz *should* win on paper. But 90Hz with bad frame pacing loses to 60Hz with perfect frame pacing — perceptually.

## 5. Scroll Physics and Spring Animations

Apple's scroll deceleration curve and spring physics (`UIScrollView`) are tuned obsessively. The **rubber-band effect**, momentum curves, and gesture recognizer priority system are all first-party and battle-tested over 15+ years.

Android's `RecyclerView` + `OverScroller` physics work differently, and third-party apps often override them inconsistently. The result is scroll behavior that varies app-to-app on Android.

## 6. GPU Driver Maturity

Apple's GPU driver is **userspace + compiled into iOS**. No kernel driver round-trips, no generic Vulkan/OpenGL overhead for UIKit rendering. The Metal stack is co-designed with the GPU.

Pixel 7's Tensor G2 uses an **ARM Mali GPU** with a generalized driver stack. Tensor chips have historically had GPU performance issues vs Qualcomm Snapdragon on Android, making the situation worse specifically for Pixel 7 vs other Android flagships.

## Summary Table

| Factor | iPhone X | Pixel 7 |
| --- | --- | --- |
| Display Hz | 60 | 90 |
| Touch sampling | 120Hz | 90Hz |
| Touch latency | ~35ms | ~65ms |
| Animation pipeline | Render Server (out-of-process) | RenderThread (in-process) |
| GPU driver | Metal, co-designed | Mali, generic stack |
| Frame pacing consistency | Excellent | Good but variable |

**The core insight:** Smoothness is dominated by *input latency* and *frame consistency*, not clock speed or refresh rate. Apple controls the full stack — silicon, OS, frameworks, apps — and has optimized this path for 15 years. Google is catching up but still shipping a software+hardware stack with more moving parts and less vertical integration.
