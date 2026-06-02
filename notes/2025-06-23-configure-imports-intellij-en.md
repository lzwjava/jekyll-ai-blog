---
audio: false
generated: true
lang: en
layout: post
title: Configuring Single-Class Imports in IntelliJ IDEA
translated: false
type: note
---

IntelliJ IDEA provides settings to control how it handles imports, including preventing the use of wildcards. Here's how you can configure it to always use single-class imports:

1.  **Open Settings/Preferences:**
    * **Windows/Linux:** `Ctrl + Alt + S`
    * **macOS:** `Cmd + ,` (Comma)

2.  **Navigate to Code Style for Java:**
    * In the left-hand pane of the Settings dialog, navigate to:
        `Editor` -> `Code Style` -> `Java`

3.  **Go to the "Imports" Tab:**
    * On the right side, select the `Imports` tab.

4.  **Configure Import Settings:**
    You'll see a few important settings here:

    * **`Use single class import`**: **Check this checkbox.** This is the primary setting that tells IntelliJ to prefer individual class imports over wildcard imports.

    * **`Class count to use import with '*'`**: This setting determines how many classes from a single package must be imported before IntelliJ automatically switches to a wildcard import (e.g., `java.util.*`). To effectively disable wildcard imports, **set this to a very high number**, such as `999` or `9999`. This ensures that you'll almost never reach the threshold for a wildcard import.

    * **`Names count to use static import with '*'`**: This is similar to the above but for static imports. Set this to a high number as well (e.g., `999` or `9999`) to prevent wildcard static imports.

    * **`Packages to Use Imports with '*'`**: This table lists packages for which IntelliJ will *always* use wildcard imports, regardless of the other settings. **Ensure this table is empty** if you want to completely avoid wildcard imports. If you see entries like `java.util.*` or `java.awt.*`, remove them.

5.  **Apply Changes:**
    * Click `Apply` and then `OK` to save your changes.

**After making these changes:**

* When you use the "Auto Import" feature (e.g., by pressing `Alt + Enter` on an unresolved class), IntelliJ will now insert individual class imports instead of wildcards.
* If you have existing files with wildcard imports, you can use the "Optimize Imports" action (`Ctrl + Alt + O` on Windows/Linux, `Cmd + Option + O` on macOS) to convert them to single-class imports according to your new settings.

By following these steps, you can effectively prevent IntelliJ IDEA from using wildcard imports for Java files.
