---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Mihomo on Ubuntu Guide
translated: false
type: note
---

**Question:** How do I install `mihomo-linux-amd64-v3-alpha-0317d9f.deb` on Ubuntu?

**Answer:**

The `.deb` file is a Debian package, and Ubuntu natively supports installing it using either `dpkg` or `apt`. Here is the complete step-by-step guide:

---

## Step 1: Make Sure the File is Downloaded

Ensure the `.deb` file is in your current directory. If not, navigate to where it was saved:

```bash
cd ~/Downloads
ls mihomo*.deb
```

---

## Step 2: Install the `.deb` Package

**Method A — Using `dpkg` (direct and straightforward):**

```bash
sudo dpkg -i mihomo-linux-amd64-v3-alpha-0317d9f.deb
```

If there are missing dependencies after this step, fix them with:

```bash
sudo apt --fix-broken install
```

**Method B — Using `apt` (automatically handles dependencies):**

```bash
sudo apt install ./mihomo-linux-amd64-v3-alpha-0317d9f.deb
```

> Note: The `./` prefix is required to tell `apt` to use the local file instead of searching online repositories.

---

## Step 3: Verify Installation

After installation, check that mihomo is available:

```bash
mihomo -v
# or
which mihomo
```

---

## Step 4: Set Up the Configuration Directory

Mihomo requires a configuration file to work:

```bash
sudo mkdir -p /etc/mihomo
# Place your config.yaml in this directory
sudo nano /etc/mihomo/config.yaml
```

---

## Step 5: Enable and Start Mihomo as a System Service

The `.deb` package from MetaCubeX typically installs a systemd service. Start it with:

```bash
sudo systemctl daemon-reload
sudo systemctl enable mihomo
sudo systemctl start mihomo
```

Check the service status:

```bash
sudo systemctl status mihomo
```

---

## Notes on the `-amd64-v3` Variant

The `amd64-v3` in the filename means this binary is optimized for CPUs supporting **x86-64-v3** instruction sets (such as Intel Haswell or newer, AMD Ryzen and newer). If your CPU is older and does not support these instructions, the binary may crash with an **Illegal instruction** error. In that case, download the `-amd64-v1` version instead which is compatible with all 64-bit x86 CPUs.

To check your CPU level support:

```bash
/lib64/ld-linux-x86-64.so.2 --help | grep "x86-64-v"
```

If `x86-64-v3` appears as **(supported)**, you are good to go.

---

**References:**

- [MetaCubeX/mihomo GitHub Releases](https://github.com/MetaCubeX/mihomo/releases)
- [https://deepwiki.com/MetaCubeX/Meta-Docs/2-installation-and-setup](https://deepwiki.com/MetaCubeX/Meta-Docs/2-installation-and-setup)
- [https://reajason.eu.org/writing/ubuntu2004mihomotunmode/](https://reajason.eu.org/writing/ubuntu2004mihomotunmode/)