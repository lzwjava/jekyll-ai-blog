---
audio: false
generated: true
lang: en
layout: post
title: Selenium GeckoDriver Ubuntu Installation
translated: false
type: note
---

To install the Selenium Firefox driver (geckodriver) on Ubuntu, follow these steps:

1. **Install Firefox** (if not already installed):
   ```bash
   sudo apt update
   sudo apt install firefox
   ```

2. **Download geckodriver**:
   - Visit the [geckodriver releases page](https://github.com/mozilla/geckodriver/releases).
   - Choose the latest version compatible with your Firefox version. For Ubuntu, download the Linux 64-bit version (e.g., `geckodriver-vX.XX.X-linux64.tar.gz`).
   - Example command to download (replace `X.XX.X` with the latest version):
     ```bash
     wget https://github.com/mozilla/geckodriver/releases/download/vX.XX.X/geckodriver-vX.XX.X-linux64.tar.gz
     ```

3. **Extract the downloaded file**:
   ```bash
   tar -xvzf geckodriver-vX.XX.X-linux64.tar.gz
   ```

4. **Move geckodriver to a system path**:
   - Move the extracted `geckodriver` to `/usr/local/bin` to make it accessible system-wide:
     ```bash
     sudo mv geckodriver /usr/local/bin/
     ```
   - Make it executable:
     ```bash
     sudo chmod +x /usr/local/bin/geckodriver
     ```

5. **Install Selenium for Python** (if using Python):
   ```bash
   pip install selenium
   ```

6. **Verify installation**:
   - Check geckodriver version:
     ```bash
     geckodriver --version
     ```
   - Test with a simple Python script:
     ```python
     from selenium import webdriver

     driver = webdriver.Firefox()
     driver.get("https://www.example.com")
     print(driver.title)
     driver.quit()
     ```

**Notes**:
- Ensure your Firefox version is compatible with the geckodriver version (check release notes on the geckodriver GitHub page).
- If you encounter issues, ensure `python3-pip` is installed:
  ```bash
  sudo apt install python3-pip
  ```
- If geckodriver isn’t found, add `/usr/local/bin` to your `PATH`:
  ```bash
  export PATH=$PATH:/usr/local/bin
  ```

This should set up the Selenium Firefox driver on Ubuntu. Let me know if you hit any issues!

---

The difference between `geckodriver-v0.36.0-linux-aarch64.tar.gz` and `geckodriver-v0.36.0-linux64.tar.gz` lies in the target CPU architecture:

- **linux-aarch64**: This is for 64-bit ARM architectures (e.g., ARMv8-A), commonly used in devices like Raspberry Pi, some servers, or modern ARM-based Linux systems. The "aarch64" stands for 64-bit ARM architecture.

- **linux64**: This is for 64-bit x86 architectures (also known as x86_64 or AMD64), which are standard for most desktop and server PCs running Linux.

**Key Points**:
- Choose `linux-aarch64` if your system has a 64-bit ARM processor.
- Choose `linux64` if your system has a 64-bit x86 processor.
- You can check your system's architecture on Linux by running `uname -m`. If it outputs `aarch64`, use the ARM version; if it outputs `x86_64`, use the linux64 version.

The `.asc` files are GPG signatures for verifying the integrity and authenticity of the corresponding `.tar.gz` files.
