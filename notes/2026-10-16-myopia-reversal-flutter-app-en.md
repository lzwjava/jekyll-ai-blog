---
audio: false
generated: true
image: false
lang: en
layout: post
title: Myopia Reversal Flutter App
translated: false
type: note
---

Done. I built a complete Flutter app (Android + iOS) in `/Users/lzwjava/projects/myopia-reversal`, committed to git.

## What was built

**"Myopia Reversal"** — a companion app to *Comfortable Daily Eyeglass Use at 1.50D Below Full Prescription*:

### 📷 Scan 验光单 & record (Premium)
- Camera screen to photograph the prescription sheet, or import from gallery
- Google ML Kit OCR (Chinese **and** Latin scripts), with EXIF orientation normalization and rotate/re-scan
- Heuristic parser detects OD/右 & OS/左 markers and separates 球镜/柱镜/视力 values, handling both decimal (`-3.50`) and whole-number (`350`) formats — covered by unit tests
- Review screen shows the parsed values alongside the raw OCR text; user confirms/corrects before saving to history

### 💳 In-app purchase
- One-time Premium unlock via `in_app_purchase` (`com.lzwjava.myopia.premium`), with restore + local persistence
- Gates: OCR scanning, progress charts, unlimited records (free = 10), full guide (free = 1 article)

### Other features
- **Prescription history** — add/edit/delete records, switchable `350°` vs `-3.50` display
- **Progress charts** — myopia + astigmatism per eye (fl_chart), pace guidance (~0.25 D/quarter)
- **Undercorrection calculator** — daily pair (−1.50 D), driving pair (full), and multifocal progressive design (−1.00 D far / −1.75 D near)
- **Guide** — 8 articles summarizing the method, mechanism, and the author's 3-year data; seedable example journey data
- SQLite storage, Material 3 light/dark themes, Home/History/Guide/Settings tabs

## Validation
- `flutter analyze` clean, all tests pass
- ✅ `flutter build apk --debug` (Android; AGP bumped to 8.2.1 for JDK 21, added desugaring + CAMERA permission)
- ✅ `flutter build ios --no-codesign` (fixed broken CocoaPods, deployment target set to 15.5 for ML Kit)

## To make the Unlock button work on real stores
Create a non-consumable product with id `com.lzwjava.myopia.premium` in App Store Connect and Google Play Console (changeable in `lib/config.dart`). See the README for details. Note that scanner OCR accuracy depends on sheet quality — the review step covers OCR mistakes.
