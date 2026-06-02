---
audio: false
generated: true
lang: en
layout: post
title: Install Outline Client on Ubuntu
translated: false
type: note
---

Yes, you can install the Outline Client on Ubuntu, as it is a Debian-based Linux distribution, and the Outline Client is provided as a Debian package, which is compatible with Ubuntu. There are two methods to install it: the recommended method using the repository and an alternative method by downloading the Debian package directly. Below, I’ll explain how to do it using the recommended repository method, which is preferable because it integrates with Ubuntu’s package manager, making updates easier to manage.

### Steps to Install Outline Client on Ubuntu (Recommended Method)

Follow these steps to install the Outline Client on your Ubuntu system:

1. **Open a Terminal**
   Launch the terminal application on your Ubuntu system. You can do this by searching for "Terminal" in the applications menu or pressing `Ctrl + Alt + T`.

2. **Install Outline’s Repository Key**
   Run the following command to download and add the repository’s signing key to your system’s trusted keys. This ensures that packages from the repository are verified for authenticity:
   ```bash
   wget -qO- https://us-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/gcloud-artifact-registry-us.gpg
   ```

3. **Add the Outline Client Repository**
   Add the Outline Client repository to your system’s sources list by running this command. This tells Ubuntu where to find the Outline Client package:
   ```bash
   echo "deb [arch=amd64] https://us-apt.pkg.dev/projects/jigsaw-outline-apps outline-client main" | sudo tee /etc/apt/sources.list.d/outline-client.list
   ```
   - Note: The `[arch=amd64]` part specifies that this is for 64-bit systems. Most modern Ubuntu installations are 64-bit, but you can confirm your system’s architecture by running `uname -m`. If it outputs `x86_64`, you’re using a 64-bit system, and this command will work as is.

4. **Update the Package List**
   Refresh your system’s package list to include the newly added Outline repository:
   ```bash
   sudo apt update
   ```

5. **Install the Outline Client**
   Install the latest version of the Outline Client with this command:
   ```bash
   sudo apt install outline-client
   ```

### Post-Installation

- **Launching the Outline Client**: After installation, you can find the Outline Client in your applications menu or launch it from the terminal by typing `outline-client`.
- **Keeping It Updated**: To check for and install updates, use Ubuntu’s standard update commands:
  ```bash
  sudo apt update
  sudo apt upgrade
  ```
  These commands will update all installed packages, including the Outline Client, since it’s managed through the repository. Note that in-app auto-updates are disabled for the Outline Client on Linux starting with version 1.15, so relying on the package manager is the best way to stay current.
- **Uninstalling**: If you need to remove the Outline Client, run:
  ```bash
  sudo apt purge outline-client
  ```

### Why Use the Recommended Method?

The repository method is recommended because:
- It integrates with Ubuntu’s `apt` package manager, allowing you to update the Outline Client alongside other system packages.
- You don’t need to manually download and install new versions, unlike the alternative method where you’d have to repeat the download and installation process for each update.

### Assumptions and Requirements

- **Ubuntu Version**: The instructions don’t specify a minimum Ubuntu version, but since Ubuntu is Debian-based and the package targets 64-bit systems, any recent 64-bit Ubuntu version should work. To be safe, ensure your system is up to date by running `sudo apt update && sudo apt upgrade` before starting.
- **Architecture**: These instructions assume a 64-bit system (amd64). If you’re using a different architecture (e.g., 32-bit or ARM), this method won’t work as provided, and you’d need to check for alternative packages or contact Outline support.

### Alternative Method (Optional)

If you prefer not to add a repository, you can download and install the Debian package directly:
1. Download the package:
   ```bash
   wget -O ./outline-client.deb https://s3.amazonaws.com/outline-releases/client/linux/stable/outline-client_amd64.deb
   ```
2. Install it:
   ```bash
   sudo apt install ./outline-client.deb
   ```
However, you’ll need to manually repeat this process for updates, which is less convenient.

### Conclusion

Using the recommended repository method, you can easily install and maintain the Outline Client on Ubuntu. Just follow the steps above, and you’ll have it up and running with the ability to keep it updated effortlessly through your system’s package manager.
