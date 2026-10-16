---
audio: false
generated: true
image: false
lang: en
layout: post
title: Myopia Reversal v1.0.0 Installed
translated: false
type: note
---

✅ **Installed on your iPhone 13 (lzwjava13).**

**Myopia Reversal** v1.0.0 (`com.lzwjava.myopiaApp`) is now on the device — verified via devicectl:

```
Name              Bundle Identifier       Version
Myopia Reversal   com.lzwjava.myopiaApp   1.0.0
```

## What happened along the way

1. **Wrong device initially** — your Mac has two iPhones paired: `lzwjava` (iPhone 14 Pro Max) and `lzwjava13` (iPhone 13, `D20B05C1-…`). I targeted the right one now (`00008110-001159DC0CD3801E`).
2. **Signing/provisioning** — iOS 26 requires a provisioning profile per app. Your old profile only covered `com.quzhibo.LiveIos`, so the build failed with *"No profiles for com.lzwjava.myopiaApp"*. After registering the new profile (team `976YQN9M2D` for our bundle id, covers both devices), the app built and signed cleanly.
3. Installed over wireless deployment with `flutter install -d 00008110-001159DC0CD3801E`.

## Notes

- The app icon should be on the home screen — open **Myopia Reversal**. Camera/photo-library prompts appear on first use of Scan 验光单.
- Scanning, charts, and the full guide are **Premium**. The Unlock button needs a store product (`com.lzwjava.myopia.premium`) in App Store Connect + Google Play Console before it can complete a real purchase.
- Your iPhone 14 Pro Max is also provisioned now, so the same `flutter install` works there if you ever want it.

Want me to also install it on the iPhone 14 Pro Max, or add a hidden tester toggle to preview Premium features without the store?
