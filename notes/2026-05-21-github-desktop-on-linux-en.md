---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Desktop on Linux
translated: false
type: note
---

Sure, here's the full picture:

---

## GitHub Desktop on Linux — What You Just Installed

### What is the shiftkey/desktop fork?

GitHub Desktop (the official app by GitHub Inc.) only supports macOS and Windows. There is no official Linux build. **shiftkey/desktop** is the de facto Linux port — maintained by Brendan Forster (GitHub alumnus) and the community. It tracks the official upstream desktop/desktop codebase closely, adding Linux-specific patches for:

- Native file dialogs (via GTK)
- Linux keychain integration (libsecret/gnome-keyring)
- AppIndicator/tray support
- .deb packaging for Debian/Ubuntu-based distros

The latest release is **3.4.13-linux1** (Feb 2025) — it's an "RC" but has been very stable for most users. It's the same version as GitHub Desktop 3.4.13 on Windows/Mac under the hood.

### How to use it

| Action | How |
|---|---|
| **Launch** | `github-desktop` in terminal, or find "GitHub Desktop" in your app menu |
| **First run** | Sign in with your GitHub account (OAuth flow opens your browser) |
| **Clone a repo** | File > Clone Repository, or paste a URL |
| **Open a local repo** | File > Add Local Repository |
| **Push/Pull/Fetch** | Toolbar buttons at the top |
| **Create PR** | Branch > Create Pull Request (opens in browser) |

### What it can do

- Clone, init, add, commit, push, pull, fetch repos
- Visually review diffs (side-by-side or unified)
- Create and switch branches, manage PRs
- Resolve merge conflicts with a GUI
- View commit history with a graph
- Stash/unstash changes
- Manage multiple repos in one window
- SSH key and GPG signing support

### Caveats to be aware of

1. **Not an official GitHub product** — it's a community fork. It works well but may lag behind upstream releases by a few weeks.
2. **No auto-update** — the Linux build doesn't have the built-in updater. You'll need to manually download and `dpkg -i` new `.deb` releases as they come out.
3. **AppIndicator/tray** — it minimises to system tray; if your Mint panel doesn't show tray icons by default, you may need a tray extension (e.g., `snapd-glib`, `libayatana-appindicator` should be pre-installed on Mint).
4. **No GPG signing in GUI** — CLI-based GPG signing works fine but the GUI doesn't expose commit signing settings on Linux.
5. **Keychain** — uses GNOME Keyring / libsecret for storing credentials. If you don't have one set up, it'll ask for a keychain password on first credential save.

### File locations

| Path | Purpose |
|---|---|
| `/usr/bin/github-desktop` | The main binary |
| `/usr/share/applications/github-desktop.desktop` | App menu entry |
| `~/.config/GitHub Desktop/` | Application config and keychain data |
| `/tmp/github-desktop.deb` | The downloaded installer (still there if you want to keep for reinstall) |

### Updating later

When a new release comes out, the same recipe works:

```bash
# Find the latest .deb URL from:
#   https://github.com/shiftkey/desktop/releases/latest
cd /tmp
curl -fsSL -O <url-to-newest-amd64.deb>
pkexec dpkg -i GitHubDesktop-linux-amd64-*.deb
```

No `apt install -f` needed — the `.deb` bundles all its Electron dependencies.
