---
audio: false
generated: true
lang: en
layout: post
title: Installing Firefox via APT on Ubuntu
translated: false
type: note
---

This guide details how to install Firefox from the Mozilla APT repository on Ubuntu, replacing the default Snap package.

**Why use the APT version?**

While the Snap version is convenient, some users prefer the APT version for better integration and performance.

**Steps:**

1.  **Uninstall the Firefox Snap:**

    ```bash
    sudo snap remove firefox
    ```

2.  **Create an APT keyring directory (if it doesn't exist):**

    ```bash
    sudo install -d -m 0755 /etc/apt/keyrings
    ```

3.  **Import the Mozilla APT repo signing key:**

    ```bash
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
    ```
    *If `wget` is missing, install it first: `sudo apt install wget`*

4.  **Add the Mozilla repository to your sources list:**

    ```bash
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
    ```

5.  **Set package priority to prefer the Mozilla DEB:**

    This prevents Ubuntu's transition package from reinstalling the Snap.

    ```bash
    echo '
    Package: *
    Pin: origin packages.mozilla.org
    Pin-Priority: 1000

    Package: firefox*
    Pin: release o=Ubuntu
    Pin-Priority: -1' | sudo tee /etc/apt/preferences.d/mozilla
    ```

6.  **Remove the Ubuntu Firefox DEB (if present) and install the Mozilla version:**

    ```bash
    sudo apt update && sudo apt remove firefox
    sudo apt install firefox
    ```

Now you have Firefox installed from the official Mozilla APT repository!
