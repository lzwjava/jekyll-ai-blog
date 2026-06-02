---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Installing Emacs on RHEL
translated: false
type: note
---

### Installing Emacs on Red Hat Enterprise Linux

Red Hat Enterprise Linux (RHEL) primarily uses the DNF package manager for installing software. Emacs is available in the default repositories, so installation is straightforward. Below are the steps for modern versions (RHEL 8 and later). For older versions (e.g., RHEL 7), replace `dnf` with `yum`.

#### Prerequisites
- Ensure you have root privileges (use `sudo`).
- Your system should be registered with Red Hat Subscription Management if using official RHEL repositories.

#### Installation Steps
1. **Update your package cache** (recommended to ensure you get the latest available version):
   ```
   sudo dnf update
   ```

2. **Install Emacs**:
   ```
   sudo dnf install emacs
   ```
   This will install the latest stable version available in the repositories (e.g., Emacs 28.x or 29.x, depending on your RHEL version).

3. **Verify the installation**:
   Run the following to check the version:
   ```
   emacs --version
   ```
   You should see output like `GNU Emacs 28.2` (or similar).

#### Notes
- If you're on an older RHEL version using YUM (e.g., RHEL 7), the command is `sudo yum install emacs`.
- For the absolute latest Emacs version (e.g., 29+), you may need to compile from source or use third-party repositories like EPEL, as base repos might lag behind.
- To launch Emacs, simply type `emacs` in the terminal.

[GNU Emacs FAQ: Installing Emacs](https://www.gnu.org/software/emacs/manual/html_node/efaq/Installing-Emacs.html)
[Red Hat Documentation: Managing Software with DNF](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/managing_software_with_the_dnf_tool/index)
