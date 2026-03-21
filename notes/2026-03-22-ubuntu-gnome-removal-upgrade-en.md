---
audio: false
generated: true
image: false
lang: en
layout: post
title: GNOME Removal During Ubuntu Major Upgrades
translated: false
type: note
---

Question: During an Ubuntu 22 to Ubuntu 24 upgrade, can the GNOME desktop environment get completely uninstalled?

Answer:

**Yes, this can absolutely happen during a major Ubuntu release upgrade.** Here's a comprehensive explanation of why and how:

---

## Why GNOME Gets Uninstalled During Ubuntu 22 → 24 Upgrade

### 1. Package Transition and Renamed Meta-packages

During `do-release-upgrade`, the upgrade tool (`ubuntu-release-upgrader`) resolves dependency trees between releases. If any of the following occur, desktop packages can be removed:

- **Meta-package conflicts**: `ubuntu-desktop` in 24.04 may have different dependencies or transitional package names than in 22.04
- **Held packages**: If you previously held back any GNOME-related package (`apt-mark hold`), the resolver may choose to remove dependent packages instead of upgrading them
- **Third-party PPAs**: PPAs that provided patched GNOME packages can cause conflicts, leading the resolver to remove conflicting packages entirely

### 2. The "Autoremove" Cascade

Ubuntu's upgrade process marks many packages as "automatically installed." If a meta-package like `ubuntu-desktop` gets removed or replaced, all its auto-installed dependencies become orphaned and eligible for autoremoval. This creates a cascade:

```
ubuntu-desktop removed
  → gdm3 marked for removal
    → gnome-shell marked for removal
      → gnome-session marked for removal
        → gnome-settings-daemon marked for removal
```

### 3. The `rc` Status Is the Smoking Gun

The `rc` state (removed, config retained) on `gdm3`, `gnome-shell`, and `gnome-settings-daemon` confirms these were **cleanly removed by the package manager** — not corrupted. This is a controlled removal, not a crash.

### 4. The `active (exited)` GDM3 Trap

This is a particularly confusing symptom. Here's the flow:

```
systemd starts gdm3 service
  → triggers /etc/init.d/gdm3 (SysV compat)
    → script checks: test -x /usr/sbin/gdm3
      → binary missing → exits 0 (success!)
        → systemd reports: active (exited) ✓
```

The service appears healthy but has done nothing. Combined with `graphical.target` still being the default and `/etc/X11/default-display-manager` still pointing to the missing binary, the system boots silently to TTY with no errors logged.

---

## How to Prevent This in Future Upgrades

- **Before upgrading**, manually install the meta-package: `sudo apt install ubuntu-desktop`
- **Disable all PPAs** before running `do-release-upgrade`
- **Check for held packages**: `apt-mark showhold`
- **Review the upgrade summary carefully** — the installer shows packages to be removed; watch for `gdm3`, `gnome-shell`, `ubuntu-desktop`

---

## Recovery

As already identified, the fix is straightforward:

```bash
sudo apt install ubuntu-desktop
sudo reboot
```

This reinstalls the full meta-package, pulls back GDM3, GNOME Shell, and all dependencies, and restores the graphical login on next boot.

References:

- [Ubuntu Release Upgrade — Official Docs](https://ubuntu.com/server/docs/upgrade-introduction)
- [Ubuntu 24.04 LTS Release Notes](https://discourse.ubuntu.com/t/noble-numbat-release-notes/39890)
- [Debian Package Status Fields (`rc`, `ii`, etc.)](https://www.debian.org/doc/manuals/debian-faq/pkg-basics.en.html)