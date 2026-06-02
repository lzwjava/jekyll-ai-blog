---
audio: false
generated: true
lang: en
layout: post
title: Fix Python distutils ModuleNotFoundError
translated: false
type: note
---

The error occurs because the `distutils` module, part of Python's standard library, is missing in your environment. This is common in minimal Python installations. Here's how to fix it:

### Solution:
1. **Install Python development tools** (includes `distutils`):
   ```bash
   sudo apt update && sudo apt install python3-distutils python3-dev
   ```

2. **Reinstall `setuptools`** (to ensure proper functionality):
   ```bash
   pip install --upgrade --force-reinstall setuptools
   ```

3. **Retry installing your requirements**:
   ```bash
   pip install -r requirements.local.txt
   ```

### Why this works:
- `python3-distutils` provides the missing `distutils` module.
- `python3-dev` includes necessary headers/building tools.
- Reinstalling `setuptools` resolves any lingering configuration issues.

If you're in a virtual environment, recreate it after installing the system packages to ensure the environment has access to the required modules.
