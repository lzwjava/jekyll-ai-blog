---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Fixing Broken Python GI Bindings
translated: false
type: note
---

### Updated Diagnosis
Based on the new details, your Python 3.13.7 installation (likely manual or via PPA/source) has broken the system's GObject Introspection (GI) bindings. The `gi` module's `_gi` C extension is compiled for your distro's default Python (probably 3.10 or 3.11, given the directories in `/usr/lib/python`), not 3.13. This causes the circular import error when `gnome-terminal` (a Python script) tries to load it. The multi-version setup in `/usr/lib/python` confirms this mismatch—system packages like `python3-gi` aren't built for 3.13 yet (it's too new for most distros as of 2025).

The UFW logs remain irrelevant noise.

### Recommended Fix: Revert to System Default Python
The cleanest solution is to switch `/usr/bin/python3` back to your distro's default (e.g., 3.10), then reinstall GI bindings. This avoids hacks like copying .so files, which can cause inconsistencies.

1. **Identify and switch to the default Python version** (use `update-alternatives` if configured; otherwise, manual symlink):
   ```
   # Check if alternatives are set up
   sudo update-alternatives --config python3
   ```
   - If it lists options, select the lowest priority one (usually the distro default, like 3.10).
   - If no alternatives (common on stock Ubuntu), manually revert:
     ```
     # Assuming default is 3.10 (common for Ubuntu 22.04; swap to 3.11 if that's your base)
     sudo rm /usr/bin/python3
     sudo ln -s /usr/bin/python3.10 /usr/bin/python3
     ```
   - Verify: `python3 --version` should now show 3.10.x (or your default).

2. **Reinstall GI and GNOME Terminal packages**:
   ```
   sudo apt update
   sudo apt install --reinstall python3-gi gir1.2-glib-2.0 gnome-terminal
   ```

3. **Test**:
   ```
   python3 -c "from gi.repository import GLib, Gio; print('GI OK')"
   gnome-terminal
   ```
   - If the Python test passes but terminal still fails, reset its config: `dconf reset -f /org/gnome/terminal/`.

### If You Want to Keep Python 3.13
- This is trickier, as official `python3-gi` won't exist for 3.13 yet. You'd need to compile PyGObject from source:
  1. Install build deps: `sudo apt install libgirepository1.0-dev libcairo2-dev pkg-config python3.13-dev`.
  2. Download and build PyGObject: Follow [official guide](https://pygobject.gnome.org/install.html) with `--prefix=/usr/local`.
  3. But this risks breaking other system tools—revert if issues arise.
- Or, hackily copy the `_gi` extension (not recommended long-term):
  ```
  cd /usr/lib/python3/dist-packages/gi/
  sudo cp _gi.cpython-3[01]m*.so _gi.cpython-313m-x86_64-linux-gnu.so  # Adjust '3[01]' to your default (3.10 or 3.11)
  ```
  Then reinstall `python3-gi` as above.

### Prevention
- Don't manually override `/usr/bin/python3`—use virtualenvs (`python3 -m venv myenv`) for projects needing 3.13.
- If you installed 3.13 via deadsnakes PPA, remove it and stick to distro Python.

If this doesn't fix it, run `ls -l /usr/bin/python*` and `dpkg -l | grep python3 | grep -E 'gi|default'` and share the output.

[gnome-terminal will not start after trying to install newer version of Python 3](https://askubuntu.com/questions/880188/gnome-terminal-will-not-start-after-trying-to-install-newer-version-of-python-3)
[ImportError: cannot import name '_gi' from partially initialized module 'gi'](https://stackoverflow.com/questions/59838238/importerror-cannot-import-name-gi-from-partially-initialized-module-gi-mo)
[Why won't terminal open?](https://www.reddit.com/r/Ubuntu/comments/1f9qh0a/why_wont_terminal_open/)
