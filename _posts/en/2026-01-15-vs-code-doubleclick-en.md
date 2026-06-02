---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Double-Click to Open Files in VS Code
translated: false
type: note
---

**Question: In GitHub Desktop, when viewing a history commit, in the middle panel's changed files list, does double-clicking a file open it in VS Code?**

**Answer:**

**Yes, this is a supported feature in recent versions of GitHub Desktop.**

When you:

- Go to the **History** tab
- Select a past commit
- See the list of changed files in the middle panel (the "changed files" list for that commit)

Double-clicking a file in that list will open the file **in your configured external editor** (such as Visual Studio Code), if you have one set up.

This behavior was added as a highly requested community-contributed feature around 2023. It works both:

- In the **History** view (for files changed in a past commit — note that it opens the **current/working copy** version of the file, not the historical version from the commit)
- In the **Changes** view (for uncommitted/local changes)

To make this work with VS Code specifically:

1. Go to **File → Options → Integrations** (or **GitHub Desktop → Preferences** on macOS)
2. Under **External editor**, select **Visual Studio Code** (it should auto-detect if installed; if not, point to the executable)
3. Once set, double-clicking files in either the Changes list or a commit's changed files list will launch/open the file directly in VS Code.

Before this feature was added (in older versions), double-clicking typically just showed the diff inside GitHub Desktop itself, and you'd have to right-click → "Open in Visual Studio Code" (or use the menu/keyboard shortcut) to open the full file in the editor. Some users reported accidental opens due to fast clicking being interpreted as double-clicks in certain updates.

If double-click doesn't open VS Code for you:

- Confirm VS Code is correctly set as the external editor.
- Ensure you're double-clicking the file name/entry in the list (not the diff area).
- Update GitHub Desktop to the latest version, as this is a relatively modern addition.

This makes reviewing commit history and quickly jumping to edit files in VS Code much smoother — a nice quality-of-life improvement!

**References:**

- [GitHub Changelog: Community adds "Double click to Open External Editor"](https://github.blog/changelog/2023-08-16-github-desktop-community-adds-check-out-a-commit-and-double-click-to-open-external-editor)
- [GitHub Desktop issue discussions on double-click behavior](https://github.com/desktop/desktop/issues?q=is%3Aissue+double+click+file+external+editor)
