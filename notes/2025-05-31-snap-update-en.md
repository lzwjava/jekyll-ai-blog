---
audio: false
generated: true
lang: en
layout: post
title: Updating VSCode via Snap on Ubuntu
translated: false
type: note
---

To update Visual Studio Code (VSCode) installed via Snap on Ubuntu, follow these steps:

1. **Open a terminal**: You can do this by pressing `Ctrl + Alt + T`.

2. **Check for updates**: Snap automatically checks for updates in the background, but you can manually trigger an update check by running:

   ```bash
   sudo snap refresh
   ```

3. **Update VSCode**: If a newer version of VSCode is available, the `snap refresh` command will download and install it. You’ll see output indicating the progress, like:

   ```
   code 1.85.2 from Visual Studio Code (code✓) refreshed
   ```

   If no updates are available, it will say:

   ```
   All snaps up to date.
   ```

4. **Verify the update**: To confirm the installed version of VSCode, run:

   ```bash
   code --version
   ```

   This will display the current version of VSCode.

### Notes

- **Automatic updates**: Snap packages, including VSCode, are typically updated automatically in the background. You usually don’t need to manually intervene unless you want to force an update.
- **Root privileges**: The `sudo` command is required for system-wide Snap operations.
- **Check Snap status**: If you want to see which Snap packages are installed and their versions, use:

   ```bash
   snap list
   ```

- **Troubleshooting**: If the update fails, ensure your internet connection is stable and that the Snap daemon is running (`sudo systemctl status snapd`). You can also try refreshing Snap metadata with:

   ```bash
   sudo snap refresh --list
   ```

This process ensures VSCode stays up to date with the latest version available in the Snap store.
