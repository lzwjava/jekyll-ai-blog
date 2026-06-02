---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Fix Flutter Xcode Code Signing Failure
translated: false
type: note
---

You're hitting the common Flutter / Xcode code-signing failure: Xcode/`security` found no valid signing identities, so `flutter run` can't sign the app for a physical device. Below I’ll give a clear, ordered set of fixes and troubleshooting commands — pick the path you want (run in Simulator right now, or set up signing to run on a real device). I won’t ask for more info — I’ll assume you want to fix this now.

---

# Quick options (pick one)

**A — Run on simulator (no code signing required)**
If you just want to run quickly without dealing with certificates:

1. Open Simulator: `open -a Simulator`
2. Run Flutter targeting the simulator:
   `flutter run -d "$(xcrun simctl list devices | grep -m1 -o "iPhone.*(Simulator)" | sed 's/ (Simulator)//')"`
   Or more simply: `flutter run -d iPhone-14` (replace with an available simulator name shown by `xcrun simctl list`).

**B — Fix signing to deploy to a real device (recommended for device testing)**
Follow the steps below in order.

---

# Steps to fix signing for device deployment

## 1) Confirm environment & basic checks

Run these and note output:

```bash
flutter doctor -v
xcode-select --print-path
xcodebuild -version
security find-identity -p codesigning -v
xcrun simctl list devices
```

`security find-identity -p codesigning -v` should show at least one identity. Yours showed `0 valid identities found` — that’s why it fails.

## 2) Use Xcode automatic signing (easiest)

1. Open workspace:
   `open ios/Runner.xcworkspace`
2. In Xcode: select the `Runner` project → `Runner` target → **Signing & Capabilities**.
3. Set **Team** to your Apple ID / Apple Developer account. If your Apple ID is not added:

   * Xcode → Preferences → Accounts → `+` → add Apple ID.
4. Tick **Automatically manage signing**.
5. Ensure the **Bundle Identifier** is unique (reverse-DNS style, e.g. `com.yourname.yourapp`).
6. Xcode will attempt to create a development certificate & provisioning profile; if you see prompts, allow Xcode to manage it.

> Note: For full device deployment to an arbitrary device you need an Apple Developer membership ($99/yr). Xcode can use a free Apple ID for “free provisioning”, but it is limited (device counts, no certain entitlements).

## 3) Register your device (if required)

If Xcode cannot automatically register your device, go to Apple Developer Portal → Certificates, IDs & Profiles → Devices → add device UDID. You can get device UDID by connecting device and selecting it in Xcode’s Devices and Simulators window.

## 4) Generate/import certificate manually (if you already have p12)

If you have a `.p12` certificate and private key:

```bash
security import /path/to/certificate.p12 -k ~/Library/Keychains/login.keychain-db -P "P12_PASSWORD" -T /usr/bin/codesign
```

Then re-run `security find-identity -p codesigning -v` to confirm it appears.

## 5) If you prefer Xcode to create certificates for you

In Xcode → Accounts → Select your Apple ID → Manage Certificates → `+` → add **iOS Development**. This creates a cert in your keychain and shows up in `security find-identity`.

## 6) Make sure Command Line Tools are set

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

Then accept license if needed:

```bash
sudo xcodebuild -license accept
```

## 7) After signing is set, run from terminal

From project root:

```bash
flutter clean
flutter pub get
flutter run
```

If multiple devices, specify `-d <device-id>`.

---

# Troubleshooting tips & common pitfalls

* **"0 valid identities found" persists** — confirm certificate private key is in login keychain (open Keychain Access → login). If you imported certificate but not private key, signing fails.
* **Bundle ID mismatch** — the App ID in Developer Portal must match the bundle identifier in Xcode exactly (wildcards allowed for some cases).
* **Team not selected** — Xcode shows “No account” — add Apple ID in Xcode Preferences → Accounts.
* **Provisioning profile expired** — check Developer Portal and regenerate provisioning profile.
* **Free provisioning limitations** — if using a free Apple ID, you may need to re-provision every 7 days and have limited devices.
* **CI / automation** — use `fastlane match` or App Store Connect APIs to manage certs and profiles centrally.
* **Codesign permission errors** — ensure Keychain item grants codesign access; sometimes you must manually allow `/usr/bin/codesign` to access the private key in Keychain.
* **If `flutter run` still fails**, run the Xcode build to see a more detailed error: open the workspace and press Run in Xcode; check Signing & Capabilities errors in the UI.

---

# Useful commands copy-paste

List codesigning identities:

```bash
security find-identity -p codesigning -v
```

Import `.p12`:

```bash
security import /path/to/yourcert.p12 -k ~/Library/Keychains/login.keychain-db -P "P12PASSWORD" -T /usr/bin/codesign
```

Set Xcode command line tools:

```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

Open the iOS workspace:

```bash
open ios/Runner.xcworkspace
```

---

# If you want, I can

* give the exact sequence of Xcode clicks to create cert/profile step-by-step (I already included the core steps), or
* provide `fastlane`/`match` example commands if you want automation for multiple machines/CI, or
* help interpret any new error output after you try the Xcode automatic signing route.

Tell me which path you chose (Simulator now / Xcode automatic / manual p12 import / CI) and paste any new errors if it still fails — I’ll give the next steps.
