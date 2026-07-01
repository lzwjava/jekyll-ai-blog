---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Mac Spotlight Missing Installed Apps
translated: false
type: note
---

Question: Why doesn't Mac Spotlight search find installed apps (like VLC), and instead shows "Search App Store"? How can I fix it?

Answer:

## Why Mac Spotlight Search Fails to Find Your Installed Apps

This is a very common and well-known macOS bug, especially after updates like macOS Sequoia (15.x). The root cause is a **corrupted or incomplete Spotlight index** — Spotlight's internal database has lost track of your installed apps, so it falls back to suggesting the App Store instead.

---

## Fixes (Try in Order)

### ✅ Fix 1: Check if "Applications" is Enabled in Spotlight Settings

1. Open **System Settings** → **Spotlight**
2. Make sure **Applications** is checked in the search results list
3. Even if it's already checked — **uncheck it, then check it again**
4. **Restart your Mac**

This toggle trick alone fixes the problem for many users.

---

### ✅ Fix 2: Rebuild the Spotlight Index (Recommended by Apple)

This forces Spotlight to re-scan your Applications folder:

1. Go to **System Settings → Spotlight → Search Privacy** (or "Spotlight Privacy" button)
2. Click the **`+`** button and add your **Applications folder** (or your whole `Macintosh HD`)
3. Wait a few seconds
4. Select it and click **`–`** to remove it
5. Click **Done**, then quit System Settings
6. Wait for re-indexing to complete (you'll see a progress bar in Spotlight)

---

### ✅ Fix 3: Rebuild Index via Terminal (More Thorough)

Open **Terminal** (find it in `/Applications/Utilities/Terminal`) and run:

```bash
sudo mdutil -E /
```

- Type your admin password when asked (nothing will appear as you type — that's normal)
- This erases and fully rebuilds the Spotlight index
- Give it 15–30 minutes; apps should appear quickly even before full completion

---

### ✅ Fix 4: Force Full Re-index via Terminal (Nuclear Option)

If Fix 3 doesn't work, use these two commands in order:

```bash
sudo mdutil -Eai off
sudo mdutil -Eai on
```

Then restart your Mac. This completely wipes and rebuilds all index data.

---

### ✅ Fix 5: Open the App Manually Once

Some users report that after **manually opening an app once** (via Finder or Launchpad), it starts showing up in Spotlight again. This is a temporary workaround, not a real fix, but useful if you're in a hurry.

---

## Summary Table

| Fix | Effort | Works For |
| ----- | -------- | ----------- |
| Toggle "Applications" checkbox + restart | Easy | Most cases |
| Add/Remove folder in Search Privacy | Easy | Most cases |
| `sudo mdutil -E /` in Terminal | Medium | Persistent issues |
| `mdutil -Eai off/on` + restart | Medium | Stubborn cases |
| Open app manually once | Quick workaround | One-off apps |

---

## Why Does This Keep Happening?

This is a known bug in **macOS Sequoia (15.x)** and some earlier versions. Spotlight can lose its index for third-party apps (like VLC, Firefox, etc.) especially after macOS updates or if the Mac goes to sleep on battery. Apple has been issuing partial fixes in point releases, but the problem resurfaces for some users.

References:

- [Apple Support – Rebuild the Spotlight Index](https://support.apple.com/en-us/102321)
- [Apple Community – Spotlight doesn't find some apps on Mac](https://discussions.apple.com/thread/255834181)
- [MacRumors Forum – Spotlight not showing apps in results](https://forums.macrumors.com/threads/spotlight-not-showing-apps-in-results.2442417/)
- [How-To Geek – Apps Not Showing in Spotlight on Your Mac](https://www.howtogeek.com/apps-not-showing-in-spotlight-on-your-mac/)
- [SuperEasyApps – How to Fix Spotlight Search on Mac](https://blog.supereasyapps.com/how-to-fix-spotlight-search-on-mac-spotlight-search-not-showing-apps/)
