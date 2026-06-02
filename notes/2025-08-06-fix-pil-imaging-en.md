---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix PIL Imaging Backend Error
translated: false
type: note
---

This error means your PIL installation is either missing its binary backend (`_imaging`) or you’re accidentally using the old “PIL” package instead of the modern “Pillow.” Here’s how to fix it:

1. **Make sure you’re on Python 3**
   If `python` is pointing at Python 2, switch to Python 3:

   ```bash
   python3 --version
   python3 scripts/content/avatar.py
   ```

2. **Uninstall any stale PIL package**

   ```bash
   # this removes the old PIL if it’s installed via pip
   python3 -m pip uninstall -y PIL
   ```

3. **(Re)install Pillow**

   ```bash
   python3 -m pip install --upgrade --force-reinstall pillow
   ```

4. **Install required system libraries**
   On Ubuntu you’ll need the imaging headers so Pillow can build its `_imaging` extension:

   ```bash
   sudo apt update
   sudo apt install -y libjpeg-dev zlib1g-dev
   # then reinstall Pillow so it recompiles against those libs
   python3 -m pip install --upgrade --force-reinstall pillow
   ```

5. **Use a virtual-environment (optional but recommended)**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pillow
   python scripts/content/avatar.py
   ```

After that, `from PIL import Image` should work without the `_imaging` import error.
