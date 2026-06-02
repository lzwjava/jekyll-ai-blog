---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Disabling Ghostty's Bell Notification
translated: false
type: note
---

### What is Ghostty's "Notification Tab"?

In Ghostty (a GPU-accelerated terminal emulator), the "notification tab" likely refers to the visual bell notification feature. When a bell character (`\a`) is sent by a running command or application in the terminal (e.g., from a long-running process or error), Ghostty can prepend a bell emoji (🔔) to the title of the affected tab or window. This serves as a subtle alert to draw your attention back to that tab, especially if the terminal is unfocused or you're working in another tab. It's part of Ghostty's bell handling system, which aims to provide non-intrusive notifications without relying solely on audio or system popups.

This behavior is enabled by default under the `bell-features` configuration, specifically the `title` option. It's designed to be helpful for workflows like background jobs completing, but it can feel like an unwanted "notification" in the tab bar.

### How to Disable It

To cancel or disable this bell title notification (and potentially other bell behaviors), edit your Ghostty configuration file. The default location is `~/.config/ghostty/config` on Linux or `~/Library/Application Support/com.mitchellh.Ghostty/config` on macOS.

1. Open the config file in your preferred editor.
2. Add or modify the following line to disable the title emoji specifically (while keeping other bell features like attention requests intact):
   ```
   bell-features = no-title
   ```
   - This removes the 🔔 from the tab title but allows other bell effects (e.g., system audio or window highlighting).

3. For a fuller disable (no title emoji, no attention requests, etc.), use:
   ```
   bell-features = false
   ```
   - This turns off all bell features entirely.

4. Save the file and reload your config in Ghostty:
   - Press `Cmd/Ctrl + Shift + ,` (or run `ghostty --reload-config` from another terminal).
   - New windows/tabs will use the updated settings; existing ones may need a restart.

If this isn't the exact notification you mean (e.g., if it's an in-app toast like "Copied to clipboard" or desktop notifications from apps), you can also disable those:
- For in-app toasts (Linux GTK only): `app-notifications = false`
- For desktop notifications from terminal apps: `desktop-notifications = false`

Test by running a command that triggers a bell, like `echo -e '\a'`.

[Ghostty Config Reference](https://ghostty.org/docs/config/reference)
[Ghostty Bell Features Discussion](https://github.com/ghostty-org/ghostty/discussions/3242)
