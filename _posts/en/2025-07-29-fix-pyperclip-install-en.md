---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Pyperclip Installation Error
translated: false
type: note
---

The error occurs during the installation of the `pyperclip` package, specifically when building its wheel, due to an issue in the `setuptools` package related to the `install_layout` attribute. This is likely caused by an incompatibility between the version of `setuptools` and the Python environment or a deprecated option in the `pyperclip` setup process. Here's how to fix it:

### Steps to Resolve

1. **Update `setuptools` and `pip`**
   Ensure you have the latest versions of `setuptools` and `pip`, as outdated versions can cause compatibility issues.

   ```bash
   pip install --upgrade pip setuptools
   ```

2. **Install `pyperclip` with a Specific Version**
   The error may be due to an older or incompatible version of `pyperclip`. Try installing a specific, stable version of `pyperclip`.

   ```bash
   pip install pyperclip==1.8.2
   ```

   If `1.8.2` doesn't work, you can try the latest version explicitly:

   ```bash
   pip install pyperclip
   ```

3. **Use the `--no-binary` Option**
   If the wheel-building process fails, you can bypass it by installing the source distribution directly:

   ```bash
   pip install pyperclip --no-binary pyperclip
   ```

   This forces `pip` to install from the source rather than trying to build a wheel.

4. **Check Python Version Compatibility**
   Ensure your Python version is compatible with `pyperclip`. As of 2025, `pyperclip` supports Python 3.6 and above, but older versions may have issues. Check your Python version:

   ```bash
   python3 --version
   ```

   If you're using an older Python version (e.g., Python 3.5 or earlier), upgrade to a newer version (e.g., Python 3.8+). You can manage Python versions using tools like `pyenv`.

5. **Clear pip Cache**
   A corrupted `pip` cache can cause issues. Clear it and try again:

   ```bash
   pip cache purge
   ```

6. **Use a Virtual Environment**
   To avoid conflicts with system packages, create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install --upgrade pip setuptools
   pip install pyperclip
   ```

7. **Downgrade `setuptools` (if needed)**
   If updating `setuptools` doesn't resolve the issue, try downgrading to a version known to work with `pyperclip`. For example:

   ```bash
   pip install setuptools==59.6.0
   pip install pyperclip
   ```

8. **Check for System-Specific Issues**
   The error mentions `/usr/lib/python3/dist-packages`, indicating you might be using a system Python installation (e.g., on Ubuntu). System Python installations can have restricted permissions or conflicts with globally installed packages. Using a virtual environment (Step 6) is the best way to avoid this. Alternatively, ensure you have permissions to install packages:

   ```bash
   sudo pip install pyperclip
   ```

   However, avoid using `sudo` unless necessary, as it can mess with system Python.

9. **Alternative: Install via `apt` (Ubuntu/Debian)**
   If you're on a Debian-based system and `pip` continues to fail, you can install `pyperclip` using the system package manager:

   ```bash
   sudo apt update
   sudo apt install python3-pyperclip
   ```

10. **Debug Further**
    If none of the above work, check the `pyperclip` GitHub page or PyPI for known issues or compatibility notes. You can also try installing from the source directly:

    ```bash
    git clone https://github.com/asweigart/pyperclip.git
    cd pyperclip
    python3 setup.py install
    ```

### Additional Notes

- The error specifically points to `install_layout`, which was removed in newer versions of `setuptools`. This suggests `pyperclip`'s setup script may be outdated or incompatible with your `setuptools` version.
- If you're working in a specific environment (e.g., Docker, WSL, or a custom Python build), ensure all dependencies like `build-essential` (for compiling wheels) are installed:

  ```bash
  sudo apt install build-essential python3-dev
  ```

- If the issue persists, provide more context (e.g., Python version, OS, and whether you're using a virtual environment) for further assistance.

### References

- [Pyperclip GitHub](https://github.com/asweigart/pyperclip)
- [Setuptools Documentation](https://setuptools.pypa.io/en/latest/)
- [Pip Documentation](https://pip.pypa.io/en/stable/)
