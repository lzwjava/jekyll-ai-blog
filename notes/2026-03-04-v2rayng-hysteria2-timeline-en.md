---
audio: false
generated: true
image: false
lang: en
layout: post
title: V2RayNG Adds Hysteria2 Support Timeline
translated: false
type: note
---

V2RayNG (the Android client from <https://github.com/2dust/v2rayNG>) added support for **Hysteria 2** (often abbreviated as hy2) sometime in 2024, after early requests in January 2024 where it was explicitly stated that support was not available (due to Xray core lacking it at the time; issue #2799 closed as completed but without addition then).

Evidence points to support being present by **September 2024**:

- Issues from late September 2024 (e.g., #3618, #3619) discuss bugs/features in **version 1.9.4** specifically for Hysteria2, such as missing input fields for obfuscation (salamander) password and comparisons to other clients. This confirms full or partial integration existed by v1.9.4 (likely released summer/fall 2024).

Initial addition likely occurred between February 2024 (no support) and mid-2024, probably via a plugin-based implementation first (as later refactored).

Later developments:

- By late 2024/early 2025, users were actively using/configuring Hysteria2 in v2rayNG (issues like #4080, #4107 discuss config exports, pinSHA256 validation for hy2 URIs).
- In **version 2.0.13** (released March 3, 2026), the developers **refactored Hysteria2** to integrate it directly with **Xray core** (instead of previous plugin/external implementation) and removed the plugin version. Changelog entry: "重构Hysteria2 ，使用xray core ，并移除插件版本" (Refactored Hysteria2, using Xray core, and removed the plugin version). This implies prior support was plugin-based before this native/core switch.
- A submodule related to Hysteria was removed around January 15, 2026, aligning with this refactor/cleanup.

Note: Early Hysteria2 requests were denied because upstream Xray-core didn't support it initially (Hysteria2 stable released ~2023-2024). v2rayNG used a separate integration method until aligning with Xray updates.

For exact initial version/date, check older release tags on GitHub (e.g., scan v1.9.x changelogs or commits around mid-2024 for "add hysteria2" or similar), but available evidence shows it was **not supported before mid-2024** and was actively used by September 2024 onward. If you're on a recent version (2.0+), Hysteria2 is supported natively via Xray.
