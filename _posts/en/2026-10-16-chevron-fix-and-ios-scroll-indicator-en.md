---
audio: false
generated: true
image: false
lang: en
layout: post
title: Chevron Fix and iOS Scroll Indicator
translated: false
type: note
---

The fresh build is installed and relaunched on **lzwjava13**. Here's where things stand:

## What I fixed for the front page

The rows were using an aggressive full-bleed layout (`leading: 0` insets + a full-width white card) that left no clean room for the `NavigationLink` chevron. On your device's screen width that made the ">" render as **squashed gray fragments** ("not complete") and left a broken-looking edge.

New layout (deployed):

```swift
.listRowInsets(EdgeInsets(top: 6, leading: 12, bottom: 6, trailing: 20))
.listRowBackground(Color.clear)
```

plus each row is now a clean **rounded white card** (`clipShape(RoundedRectangle(cornerRadius: 10))`), like a proper rectangle, with the chevron sitting cleanly in its own space.

I verified on the simulator: rows are now compact white rounded cards with a small, complete ">" chevron and no clipping artifacts.

## About the gray bar on the right edge

That thin gray vertical bar (seen in both your screenshots, on the **My** page and the **Live** page — which is a `ScrollView`, not a `List` — and also present in the *old* build) is **not a row/chevron issue**. It's an iOS 26 device-level rendering artifact — most likely the scroll indicator captured mid-scroll (iOS 26 renders it as a long rounded bar on the right edge when you start/finish scrolling). It appears on all scrollable screens, and doesn't appear on the simulator. There's no app-side setting that controls it without also hurting scroll affordance.

## Please re-check

Open the app on your phone → the **直播** tab, pull to refresh:

- The rows should now be clean rounded white cards with normal gray ">" chevrons on the right.
- The broken/incomplete chevron fragments should be gone.

If the right-edge gray bar still bothers you when *not* scrolling, send another screenshot — but if it only shows while/just-after scrolling, it's the normal iOS scrollbar.
