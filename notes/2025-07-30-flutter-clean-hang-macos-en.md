---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Resolving Flutter Clean Hang on macOS
translated: false
type: note
---

Ah, I see what you mean 👍
Sometimes `flutter clean` can appear to "hang" on macOS — especially if there are a lot of generated files, or if Xcode’s `DerivedData` folders are huge.

---

### ✅ Try These Steps

1. **Cancel the stuck command**
   Hit `CTRL + C`.

2. **Clean manually (same effect as `flutter clean`)**
   You can delete these build/cache folders yourself:

   ```bash
   rm -rf build/ .dart_tool/ ios/Pods ios/Podfile.lock ios/Flutter/Flutter.framework ios/Flutter/Flutter.podspec
   ```

   If you also want Xcode’s cache gone:

   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData
   ```

3. **Re-get dependencies**

   ```bash
   flutter pub get
   ```

4. **Reinstall CocoaPods (for iOS)**

   ```bash
   cd ios
   pod install --repo-update
   cd ..
   ```

5. **Build/run again**

   ```bash
   flutter run
   ```

---

⚡ **Tip:** The first time after cleaning may take a little longer (since Flutter needs to regenerate `.dart_tool`, `.pub-cache`, iOS Pods, etc.), but it should not stay frozen forever. If you keep seeing it "stuck", it might be related to:

- **Outdated Flutter SDK** → Run `flutter upgrade`
- **Outdated CocoaPods** → Run `sudo gem install cocoapods`
- **Rosetta / M1 chip issues**: If you’re on Apple Silicon, sometimes you need to run `arch -x86_64 pod install` inside the `ios` folder, depending on your setup.

---

👉 Do you want me to give you a **one-liner script** that wipes build caches and resets Pods (basically a "super clean") so you don’t have to debug `flutter clean` being stuck?
