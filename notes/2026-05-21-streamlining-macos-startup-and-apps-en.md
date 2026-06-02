---
audio: false
generated: true
image: false
lang: en
layout: post
title: Streamlining macOS Startup and Apps
translated: false
type: note
---

**Question:** Using Hermes to audit startup items and unnecessary apps is great — planning to uninstall Sogou IME (have WeChat IME), HP printer software (printer broken for years), KindlePreviewer (haven't used Kindle in years, reading via AI now), etc. on macOS M2 Air — good call?

**Answer:**

Yes, exactly right. Dead weight is dead weight. Here's a systematic cleanup approach for your M2 Air:

## What You're Removing — Validated

| App | Why it's safe to nuke |
|-----|----------------------|
| Sogou IME | WeChat IME covers it; two IMEs fight each other for input focus |
| HP Printer software | Printer dead + HP software is notoriously bloated with background daemons |
| KindlePreviewer | Developer tool for Kindle format testing — zero use if you're not publishing eBooks |

## Full Cleanup Playbook

### 1. Audit startup items first (if not already)

```bash
# List all launch agents/daemons (what's running at boot)
ls ~/Library/LaunchAgents/
ls /Library/LaunchAgents/
ls /Library/LaunchDaemons/

# See what's actually loaded right now
launchctl list | grep -v com.apple
```

### 2. Uninstall properly (not just drag to Trash)

For apps with deep system hooks (IMEs, printer drivers), use:

```bash
# Install a proper uninstaller
brew install --cask appcleaner
```

AppCleaner finds all the hidden plist/daemon/cache files that drag-to-trash misses. For Sogou especially — it installs input method daemons that survive a simple delete.

### 3. Sogou-specific cleanup

After AppCleaner, verify the IME is gone:

```bash
# Check for lingering Sogou processes
ps aux | grep -i sogou

# Check LaunchAgents
ls ~/Library/LaunchAgents/ | grep -i sogou

# Remove if found
launchctl unload ~/Library/LaunchAgents/com.sogou.*.plist 2>/dev/null
```

### 4. HP printer driver deep clean

```bash
# HP leaves a lot of junk
sudo rm -rf /Library/Printers/hp/
sudo rm -rf /Library/Printers/HPDefinitions/
# Also check:
ls /Library/LaunchDaemons/ | grep -i hp
```

### 5. Check what's eating RAM/CPU right now

```bash
# Top memory consumers
ps aux --sort=-%mem | head -20

# Or with a better view
brew install htop && htop
```

### 6. Other common M2 Mac bloat to audit

```bash
# Check all login items programmatically
osascript -e 'tell application "System Events" to get the name of every login item'

# Spotlight on large directories wasting space
du -sh ~/Library/Application\ Support/* | sort -hr | head -20
du -sh ~/Library/Caches/* | sort -hr | head -20
```

## Things Worth Keeping (don't nuke these)

- Any Rosetta 2 stuff if you run x86 apps
- Homebrew's LaunchAgents (e.g. for services you actually use)
- `com.apple.*` daemons obviously

## After Cleanup

```bash
# Clear system caches after uninstalling
sudo purge

# Verify startup items shrunk
launchctl list | grep -v com.apple | wc -l
```

The M2 Air baseline is already very clean — removing these three alone (Sogou daemons, HP drivers, Kindle) could easily free 500MB+ RAM at boot and shave a few seconds off login time. Do it.
