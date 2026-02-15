---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dark Mode Gaps in Google Cloud Console
translated: false
type: note
---

**Question:** Why does the Google Cloud Console have a dark theme, but the tutorial or side panel remains in light mode and doesn't support dark mode?

**Answer:**

The Google Cloud Console supports **dark mode** natively as of early 2026 (it became generally available recently). You can enable it via:

1. Open the Google Cloud Console.
2. Click the **Settings and utilities** icon (gear/cog) in the toolbar.
3. Select **Appearance** from the menu.
4. Choose **Dark**, **Light**, or **Same as device** (to match your OS theme).

The main console interface—including navigation, headers, and most panels—should switch to dark mode properly.

However, the **tutorial pane** (the guided walkthrough or contextual help panel that often appears on the side/right when starting a new feature or following a codelab-like guide in the console) sometimes stays in light mode even when the rest of the console is dark. This is a known inconsistency in some Google Cloud interfaces:

- Certain overlaid or embedded help/tutorial components (like side drawers, onboarding wizards, or inline documentation panels) are not yet fully themed to respect the console's dark mode setting.
- This behavior has been reported in similar Google products (e.g., side panels in other services occasionally not syncing themes perfectly).
- The main console UI is fully dark-mode compatible, but auxiliary elements like tutorials or specific legacy/iframe-based help content may default to light mode for readability or development reasons.

**Possible workarounds:**
- Try refreshing the page or closing/reopening the tutorial pane after switching themes.
- If it's persistent, it may be a temporary limitation—Google has been actively improving dark mode coverage across services (e.g., recent updates to Vertex AI, Cloud Shell Editor, etc., show better support).
- For better eye comfort in tutorials, you can use browser extensions like Dark Reader (though it may break some interactive console elements, so use cautiously).
- Check the official docs for any updates, as theme consistency is still being refined.

If this issue continues or affects a specific tutorial, consider providing feedback directly in the console (via the "?" help menu → Send feedback) to help Google prioritize fixes.

**References:**

- [Change the appearance of the Google Cloud console](https://docs.cloud.google.com/docs/get-started/console-appearance)
- [Google Cloud blog/news mentions of Dark Mode GA](https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud)