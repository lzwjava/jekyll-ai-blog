---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting a macOS Parblo Tablet
translated: false
type: note
---

Good question. Here's exactly what I ran and what each one does:

---

### 1. Find the app bundle

```
find /Applications /System/Applications ~/Applications -iname '*parblo*' -maxdepth 3
```

Uses `find` with `-iname` (case-insensitive name match) to locate anything named '*parblo*' in the three standard application directories, max 3 directories deep.

---

### 2. Check launchd (auto-start services)

```
launchctl list | grep -i parblo
```

`launchctl list` shows every user-space service registered with launchd. Piping through `grep -i parblo` filters for anything Parblo.

```
sudo launchctl bootout gui/$(id -u) /Library/LaunchAgents/com.parblo.Tablet.plist
```

`bootout` stops the service and unregisters it from launchd. `gui/$(id -u)` targets the current user's graphical session. The path is the plist file that defines it.

```
ls /Library/LaunchAgents /Library/LaunchDaemons -name '*parblo*'
```

`LaunchAgents` = user-level auto-start. `LaunchDaemons` = system-level (root) auto-start.

---

### 3. Check binary architecture (Intel vs ARM)

```
file /Applications/ParbloTablet/.../ParbloTabletDriver
```

`file` inspects a binary's Mach-O headers and tells you if it's `x86_64` (Intel), `arm64` (Apple Silicon), or a universal binary containing both.

---

### 4. Read the Info.plist (version, build info)

```
defaults read /Applications/.../Info.plist
```

Dumps the full plist as JSON. I looked at `CFBundleShortVersionString` (v3.7.1), `DTXcode` (10.3), `DTSDKName` (macosx10.14), and `LSMinimumSystemVersion` (10.10) to see how old the build was.

---

### 5. Check brew services

```
brew services info ollama  (for ollama)
brew services list | grep -i parblo  (for parblo)
```

Shows whether Homebrew manages the service and its loaded/running status.

---

### 6. Check USB / connected hardware

```
system_profiler SPUSBDataType | grep -A 10 -i 'parblo\|tablet\|drawing'
```

Dumps all USB-connected devices and searches for tablet-related entries.

---

### 7. Check login items (System Settings)

```
osascript -e 'tell application "System Events" to get the name of every login item'
```

AppleScript via `osascript` queries System Events for the user's login items list (the list you see in System Settings > General > Login Items).

---

### 8. Check environment variables

```
env | grep -i ollama
```

Searches all environment variables for any OLLAMA_ (or PARBLO_) related vars.

---

### 9. Check listening ports

```
lsof -i :11434
lsof -i -P | grep -i parblo
```

`lsof -i :PORT` shows what's listening on a specific port (11434 = Ollama default). `lsof -i -P` with `-P` disables port name resolution for speed and accuracy.

---

### 10. Check kernel & system extensions (deep system hooks)

```
kextstat | grep -i parblo
systemextensionsctl list | grep -i parblo
```

`kextstat` lists loaded kernel extensions (very deep, can crash the system if removed wrong). `systemextensionsctl` shows newer-style system extensions (network filters, driver kit drivers).

---

### 11. Check package receipts

```
pkgutil --pkgs | grep -i parblo
ls /private/var/db/receipts/*parblo*
```

`pkgutil --pkgs` lists all packages registered with the system installer. The receipts are also stored as `.plist` files in `/private/var/db/receipts/`.

---

### 12. Check user-library cache/config locations

```
ls ~/Library/Preferences/com.parblo*
ls ~/Library/Caches/com.parblo*
ls ~/Library/Application\ Support/Parblo*
ls ~/Library/Containers/com.parblo*
ls ~/Library/Group\ Containers/*parblo*
ls ~/Library/Saved\ Application\ State/*parblo*
```

Standard macOS locations where apps store data — preferences, caches, app data, sandbox containers, shared group containers, and window state.

---

### 13. Check Trash

```
ls ~/.Trash/*parblo*
```

Some uninstallers just move to Trash rather than deleting.

---

Want me to walk through any of these in more detail?
