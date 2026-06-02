---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install and Use mtr on macOS
translated: false
type: note
---

**Question:** Does macOS have the `mtr` tool, and how do I install and use it?

**Answer:**

## `mtr` on macOS

`mtr` does **not** come pre-installed on macOS and is not available in the Apple App Store. However, it is fully supported and easy to install via **Homebrew**.

---

### Step 1 — Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Step 2 — Install `mtr`

Run the following command to install `mtr` via Homebrew:

```bash
brew install mtr
```

---

### Step 3 — Run `mtr`

After installation, you may need to run `mtr` with `sudo` because it requires raw socket access, which is restricted to root by default.

**Interactive (live) mode:**

```bash
sudo mtr api.binance.com
```

**Report mode (equivalent to your Linux command — 100 cycles):**

```bash
sudo mtr api.binance.com --report -c 100
```

**Example output:**

```
HOST: mba                         Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 192.168.1.1               0.0%   100    0.7   0.9   0.4   7.9   1.0
  2.|-- 10.0.0.1                  0.0%   100    1.2   1.5   0.8  15.0   2.1
  ...
```

---

### Why `sudo` is Required on macOS

macOS restricts raw ICMP socket access to root. Unlike Linux where you can sometimes set setuid permissions, on macOS you almost always need `sudo mtr` instead of just `mtr`.

---

### Summary Table

| Platform       | Install Command              | Run Command                          |
|----------------|------------------------------|--------------------------------------|
| Ubuntu/Debian  | `sudo apt install mtr`       | `mtr api.binance.com --report -c 100` |
| Amazon Linux   | `sudo yum install mtr`       | `mtr api.binance.com --report -c 100` |
| **macOS**      | `brew install mtr`           | `sudo mtr api.binance.com --report -c 100` |

---

### Alternative: MacPorts

If you use MacPorts instead of Homebrew, `mtr` is also available there as a port.

```bash
sudo port install mtr
```

**References:**

- [How to Perform a MTR in Windows, Mac OS, and Linux – ChemiCloud](https://chemicloud.com/kb/article/how-to-perform-a-mtr-in-windows-mac-os-and-linux/)
- [mtr — Homebrew Formulae](https://formulae.brew.sh/formula/mtr)
- [mtr on MacPorts](https://ports.macports.org/port/mtr/)
