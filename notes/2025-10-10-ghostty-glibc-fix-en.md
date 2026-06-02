---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Resolving Ghostty GLIBC Version Conflict
translated: false
type: note
---

The issue you're running into isn't just about conflicting installations—it's primarily that both the Snap and the `.deb` you downloaded were built against GLIBC 2.38 (from Ubuntu 24.04), but your system is on Ubuntu 22.04 (based on the GLIBC 2.35 version in your `libc-bin` package). This causes the "version `GLIBC_2.38' not found" error when trying to run the binary. Having both installs active can also lead to path conflicts (e.g., which`ghostty` binary gets executed), so yes, you should remove them first to clean things up.

### Step 1: Remove Existing Installations

Run these commands to uninstall both:

```
sudo snap remove ghostty
sudo apt remove ghostty
```

- This will remove the Snap version and the `.deb` version without affecting your system otherwise.
- Verify removal with `which ghostty` (should return nothing) and `snap list | grep ghostty` (should be empty).

### Step 2: Install a Compatible Version

Ghostty doesn't have official `.deb` packages for Ubuntu 22.04 yet, but there's a reliable unofficial repository that builds compatible `.deb` files for it (and other versions). It handles GLIBC compatibility automatically.

The easiest way is to use their automatic installer script, which detects your Ubuntu version and grabs the right package:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/mkasberg/ghostty-ubuntu/HEAD/install.sh)"
```

- This downloads and installs the latest compatible `.deb` (currently around v1.2.x as of recent releases).
- After it finishes, run `ghostty` to test—it should launch without the GLIBC error.
- If you see any dependency prompts during install (e.g., for `libonig5`), just approve them with `Y`.

If you prefer manual installation:

1. Go to the [releases page](https://github.com/mkasberg/ghostty-ubuntu/releases).
2. Download the `.deb` file labeled for Ubuntu 22.04 (e.g., something like `ghostty_1.2.1-0.ppa1_amd64_22.04.deb`—exact name varies by release).
3. Install it with `sudo dpkg -i ghostty_*.deb` (run from the download folder).
4. If it complains about missing dependencies, fix with `sudo apt install -f`.

### Additional Notes

- **Why build from source isn't needed here**: The unofficial repo does the heavy lifting for you, but if you want to build Ghostty yourself (e.g., for a custom version), follow the [official source build guide](https://ghostty.org/docs/install/build). It requires Zig 0.13 and some deps like `libgtk-4-dev`, but the `.deb` route is simpler.
- **Upgrading Ubuntu?** If you're open to it, moving to 24.04 would let you use the official Snap or the 24.04 `.deb` you tried earlier without issues.
- After install, you can configure Ghostty via `~/.config/ghostty/config` (see [docs](https://ghostty.org/docs/config) for options).

If you hit any errors during these steps, paste the output here for more help!
