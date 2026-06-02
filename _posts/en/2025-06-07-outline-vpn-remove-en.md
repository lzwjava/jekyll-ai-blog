---
audio: false
generated: true
lang: en
layout: post
title: Removing Outline VPN Client Ubuntu
translated: false
type: note
---

It seems like `apt` can't find a package named `outline-client`. This typically means one of two things:

1. **You didn't install Outline using `apt` (i.e., it wasn't installed as a .deb package).** This is the most common reason for this error with Outline, as many users install it via the AppImage.
2. **The package name is different, or the repository isn't configured.** While less likely for Outline, it's a possibility for other software.

Given your previous attempt, it's highly probable you installed it as an **AppImage**. In this case, you'll need to remove it manually.

Here's how to proceed:

**1. Locate and Delete the AppImage File:**

The Outline client, when installed as an AppImage, is usually a single executable file. You likely downloaded it to your `Downloads` folder, or perhaps moved it to a `bin` or `Applications` folder in your home directory.

* **Common locations to check:**
  * `~/Downloads/`
  * `~/Applications/` (if you created one)
  * `~/bin/` (if you created one)
  * The directory where you originally ran it from.

* **How to find it:** You can use the `find` command to search for it in your home directory:

    ```bash
    find ~ -name "Outline-Client*.AppImage" 2>/dev/null
    ```

    This command will search your home directory for any file starting with "Outline-Client" and ending with ".AppImage".
    Once found, delete it:

    ```bash
    rm /path/to/Outline-Client.AppImage
    ```

    (Replace `/path/to/` with the actual path found by the `find` command.)

**2. Remove Leftover Configuration and Autostart Files:**

Even if you delete the AppImage, Outline might have created some configuration files and an autostart entry for itself.

* **Remove configuration directory:**

    ```bash
    rm -rf ~/.config/Outline/
    ```

    This command removes the entire `Outline` directory within your user's configuration folder.

* **Remove autostart entry (if it was created):**
    If Outline was set to start automatically when you log in, there might be a `.desktop` file for it.

    ```bash
    rm -f ~/.config/autostart/Outline-Client.AppImage.desktop
    ```

* **Remove desktop icons (if any):**
    Sometimes AppImages create a desktop icon in your local icon directory.

    ```bash
    find ~/.local/share/icons -name "appimagekit-outline-client*.png" -delete
    ```

    This will delete any PNG icons related to the Outline AppImage.

**3. Check and Restore Network Configuration (if necessary):**

Outline, like other VPNs, can modify your DNS settings. If you experience internet connectivity issues after removing the AppImage, check your `/etc/resolv.conf` file.

* **Inspect `resolv.conf`:**

    ```bash
    cat /etc/resolv.conf
    ```

    Look for lines that look like they were added by Outline (e.g., specific IP addresses for nameservers that you don't recognize as your router's or ISP's DNS).

* **Restore `resolv.conf` (if needed):**
    If it appears Outline modified it:
  * **Option A (Recommended for modern Ubuntu):** If your system uses `systemd-resolved` (which is common in recent Ubuntu versions), you can usually fix this by re-creating the symlink:

        ```bash
        sudo rm /etc/resolv.conf
        sudo ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
        ```

  * **Option B (Manual Edit - use if Option A doesn't work or for older systems):**
        First, make a backup:

        ```bash
        sudo cp /etc/resolv.conf /etc/resolv.conf.bak
        ```

        Then, edit the file:

        ```bash
        sudo nano /etc/resolv.conf
        ```

        Comment out or remove any `nameserver` lines that were added by Outline. You can usually put in public DNS servers like Google's (`8.8.8.8` and `8.8.4.4`) or Cloudflare's (`1.1.1.1` and `1.0.0.1`) if you're unsure of your ISP's DNS.

**4. Reboot Your System:**

After completing these steps, it's highly recommended to reboot your Ubuntu system to ensure all changes take effect and any background processes related to Outline are completely terminated.

```bash
sudo reboot
```

By following these manual removal steps, you should be able to completely get rid of the Outline VPN client from your Ubuntu system.
