---
audio: false
generated: true
image: false
lang: en
layout: post
title: Normal Reasons for Brief Charging Pauses
translated: false
type: note
---

This is normal macOS behavior — there are a few reasons a brief not charging blip appears even with a working charger:

  1. USB-C Power Delivery renegotiation
  USB-C chargers negotiate power contracts with the Mac. Any tiny handshake interruption (cable flex, adapter settling)
  causes a brief not charging pause (~1–5 seconds) while PD re-negotiates. This is the most common cause of a single-sample
  blip.

  2. macOS battery health management
  "Optimized Battery Charging" can temporarily pause charging between charge cycles, briefly reporting not charging before
  resuming. More common near 80%, but can happen at other levels.

  3. Loose connector
  A MagSafe or USB-C connector that's slightly unseated can cause momentary drops and recoveries.

  ---
  Implication for the code: the current logic will fire a false-positive notification for these 1-tick transients. A simple
  fix is to require the state to persist across N consecutive checks before alerting:
