---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Stop Dock Auto-Hide in macOS
translated: false
type: note
---

Question: How to make the macOS Dock not hide automatically in the latest version?

Answer: 

In the latest macOS version (macOS Tahoe 26.x as of February 2026), follow these steps to stop the **Dock** from automatically hiding and keep it always visible:

1. Click the **Apple menu** () in the top-left corner of your screen.
2. Select **System Settings** (or System Preferences in much older versions).
3. In the sidebar, scroll down if needed and click **Desktop & Dock**.
4. Look for the option labeled **Automatically hide and show the Dock** (it may appear as a checkbox or toggle switch).
5. **Turn it OFF** / **uncheck** the box.

The Dock will now stay visible permanently at the bottom (or side) of your screen.

### Quick alternative method using keyboard shortcut (if enabled):
- Press **Command (⌘) + Option (⌥) + D**  
  This toggles the auto-hide setting instantly. If it turns off auto-hide, you're done.

### If the setting keeps re-enabling itself:
- Go to **System Settings → Keyboard → Keyboard Shortcuts** (or search for "shortcuts" in System Settings).
- Look for **Turn Dock hiding on/off** (usually under Mission Control or App Shortcuts).
- **Uncheck** or disable that shortcut to prevent accidental toggling (common cause of the issue coming back).

### If the option is grayed out or doesn't work properly:
This occasionally happens in certain betas or configurations (e.g., with Stage Manager or specific window tiling settings). Try:
- Turning Stage Manager off temporarily (System Settings → Desktop & Dock → Stage Manager)
- Restarting your Mac
- As a last resort, reset Dock preferences in Terminal:  
  ```
  defaults delete com.apple.dock && killall Dock
  ```
  (This resets many Dock settings to default — you can then turn auto-hide off again.)

These steps work consistently in macOS Ventura, Sonoma, Sequoia, and Tahoe.

References:  

- [Change Desktop & Dock settings on Mac - Apple Support](https://support.apple.com/guide/mac-help/change-desktop-dock-settings-mchlp1119/mac)
- [Apple Support Communities - Dock keeps auto-hiding on macOS Tahoe](https://discussions.apple.com/thread/256140771)
- [Apple Stack Exchange - Why does my dock's "Automatically Hide" keep getting re-enabled?](https://apple.stackexchange.com/questions/441389/why-does-my-docks-automatically-hide-keep-getting-re-enabled)