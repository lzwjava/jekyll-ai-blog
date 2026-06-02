---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Flutter Verbose Mode Debugging Guide
translated: false
type: note
---

Ahh got it 👍 — Yes, Flutter has a **verbose mode** which prints *everything* it’s doing under the hood so you can see where it hangs.

---

### ✅ Run `flutter` Commands with Verbose Logging

Just add the `-v` (or `--verbose`) flag:

- For `flutter clean`:

  ```bash
  flutter clean -v
  ```

- For fetching dependencies:

  ```bash
  flutter pub get -v
  ```

- For running your app:

  ```bash
  flutter run -v
  ```

This will dump detailed logs (network calls, file deletions, pod commands, etc.) to the terminal.

---

### 📌 Tips for Reading Verbose Logs

- Look at the **last few lines** shown before it stops responding → that tells you what step is hanging.
- Often hangs happen during:
  - **CocoaPods** resolution (network slow / repo outdated).
  - **Gradle sync** (on Android build).
  - Permissions (if Flutter doesn’t have access to some directories).

---

👉 If `flutter clean -v` still appears stuck, paste the last ~20 lines it prints here ⬇️, and I can help analyze exactly where it’s hanging.

Do you want me to write you a **shortcut cleaning script with verbosity** so you can run `./super_clean.sh` instead of typing every command?
