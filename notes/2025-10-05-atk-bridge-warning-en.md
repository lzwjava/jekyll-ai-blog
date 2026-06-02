---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding the atk-bridge Warning Message
translated: false
type: note
---

This warning message appears in GTK-based applications (like Firefox, Snap Store, or GitHub CLI) on Linux systems, especially Ubuntu. It's not an error—it's just informational. The "atk-bridge" module was once used to connect the Accessibility Toolkit (ATK) for screen readers and other accessibility features, but newer versions of GTK (starting around 3.22) include this functionality directly. Loading the separate module is redundant, so GTK skips it and logs this note.

It's harmless and doesn't affect app performance, but if it's cluttering your terminal output, you can suppress it by setting the environment variable `NO_AT_BRIDGE=1` before running the app. For example:

```bash
export NO_AT_BRIDGE=1
firefox  # Or whatever app triggers it
```

To make it permanent, add that export line to your `~/.bashrc` or `~/.profile` file.

### References

- [Not loading module "atk-bridge": The functionality is provided by GTK natively](https://stackoverflow.com/questions/75406844/not-loading-module-atk-bridge-the-functionality-is-provided-by-gtk-natively)
- [When launching firefox, get error Not loading module "atk-bridge"](https://askubuntu.com/questions/1462267/when-launching-firefox-get-error-not-loading-module-atk-bridge)
- [giving message when run any gh commad: Not loading module "atk-bridge"](https://github.com/cli/cli/issues/9043)
