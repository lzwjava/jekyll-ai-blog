---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu Screenshot Shortcuts Guide
translated: false
type: note
---

**Question:** How do I take screenshots in Ubuntu? I'm looking for the equivalent of macOS shortcuts like `⌘ + Ctrl + 4` or `⌘ + 5`.

**Answer:**

On modern Ubuntu (GNOME), the screenshot shortcuts are very similar to macOS.

| Action                            | Ubuntu                        | macOS                                      |
| --------------------------------- | ----------------------------- | ------------------------------------------ |
| Full screen                       | `PrtSc`                       | `⌘ + Shift + 3`                            |
| Select area                       | `Shift + PrtSc`               | `⌘ + Shift + 4`                            |
| Current window                    | `Alt + PrtSc`                 | `⌘ + Shift + 4`, then Space                |
| Screenshot UI (record/screenshot) | `PrtSc` (Ubuntu 22.04+)       | `⌘ + Shift + 5`                            |
| Copy to clipboard                 | Hold `Ctrl` with any shortcut | Hold `Ctrl` with macOS screenshot shortcut |

### Most useful shortcuts

```text
PrtSc
```

Opens Ubuntu's screenshot interface (similar to macOS `⌘ + Shift + 5`), where you can:

* Capture the entire screen
* Capture a window
* Capture a selected area
* Start screen recording (Ubuntu 22.04+)

---

```text
Shift + PrtSc
```

Select a rectangle to capture.

Equivalent to:

```text
⌘ + Shift + 4
```

on macOS.

---

```text
Alt + PrtSc
```

Capture only the active window.

---

```text
Ctrl + Shift + PrtSc
```

Capture a selected area **to the clipboard** instead of saving it.

Equivalent to:

```text
⌘ + Ctrl + Shift + 4
```

on macOS.

Likewise:

* `Ctrl + PrtSc` → full screen to clipboard
* `Ctrl + Alt + PrtSc` → active window to clipboard

### Where screenshots are saved

By default:

```text
~/Pictures/Screenshots/
```

(or sometimes directly in `~/Pictures` on older Ubuntu versions).

### Command-line screenshots

If you prefer the terminal:

```bash
gnome-screenshot
```

Capture an area:

```bash
gnome-screenshot -a
```

Capture the active window:

```bash
gnome-screenshot -w
```

Delay 5 seconds:

```bash
gnome-screenshot -d 5
```

### If you're on a laptop

Many laptops require holding the **Fn** key because `PrtSc` shares a key:

```text
Fn + PrtSc
```

or

```text
Fn + Shift + PrtSc
```

depending on the keyboard.

**References:**

* Ubuntu GNOME Screenshot documentation: [https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html)
* Ubuntu Desktop Guide: [https://help.ubuntu.com/stable/ubuntu-help/screen-shot-record.html](https://help.ubuntu.com/stable/ubuntu-help/screen-shot-record.html)
