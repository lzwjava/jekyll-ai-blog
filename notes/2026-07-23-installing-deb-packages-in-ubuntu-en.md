---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing .deb Packages in Ubuntu
translated: false
type: note
---

There are several ways to install a `.deb` package in Ubuntu.

### Method 1: Using `apt` (Recommended)

Open a terminal, navigate to the folder containing the `.deb` file, and run:

```bash
sudo apt install ./package_name.deb
```

Example:

```bash
sudo apt install ./google-chrome-stable_current_amd64.deb
```

Using `apt` is recommended because it automatically installs any required dependencies.

---

### Method 2: Using `dpkg`

Install the package with:

```bash
sudo dpkg -i package_name.deb
```

If there are missing dependencies, fix them with:

```bash
sudo apt --fix-broken install
```

---

### Method 3: Using the GUI

1. Double-click the `.deb` file.
2. It will open in Ubuntu's Software Center (or another package installer).
3. Click **Install**.
4. Enter your password when prompted.

---

### Verify the installation

To check if the package is installed:

```bash
dpkg -l | grep package_name
```

Or, if it's a command-line application:

```bash
package_name --version
```

If you're having trouble installing a specific `.deb` file, tell me:

* Your Ubuntu version (`lsb_release -a`)
* The name of the `.deb` file
* Any error messages you receive