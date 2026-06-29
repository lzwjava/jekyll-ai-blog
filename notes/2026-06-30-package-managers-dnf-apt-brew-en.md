---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Package Managers: dnf, apt, brew"
translated: false
type: note
---

Question: Compare dnf, apt, and brew as package managers.

Answer:

| | dnf | apt | brew |
|---|---|---|---|
| Distro/OS | Fedora/RHEL | Debian/Ubuntu | macOS/Linux |
| Format | `.rpm` | `.deb` | formula/cask (source + bottles) |
| Scope | system, root | system, root | userland, no root |
| Backend | libsolv (SAT solver) | APT resolver (libapt) | Ruby DSL |
| Repo metadata | XML (repodata) | flat `Packages` files | git repos (taps) |

**Dependency resolution.** This is the deepest real difference. dnf uses libsolv, a proper SAT solver — dependency resolution is a boolean satisfiability problem, and libsolv encodes package constraints as CNF clauses, then solves. This makes dnf's resolution more rigorous and its conflict diagnostics better. apt uses an older heuristic resolver (EDSP-pluggable, but default is greedy/backtracking, not a full SAT solver). In practice apt occasionally gives worse "broken packages" states that need `apt --fix-broken`. brew barely resolves — formulae are mostly flat with explicit deps, no real solver, because Homebrew avoids version pinning conflicts by mostly shipping one version per formula.

**Command mapping:**

```bash
# install
dnf install pkg        | apt install pkg        | brew install pkg
# remove
dnf remove pkg         | apt remove pkg         | brew uninstall pkg
# update metadata
dnf check-update       | apt update             | brew update
# upgrade all
dnf upgrade            | apt upgrade            | brew upgrade
# search
dnf search foo         | apt search foo         | brew search foo
# info
dnf info pkg           | apt show pkg           | brew info pkg
# what owns this file
dnf provides /path     | dpkg -S /path          | brew --prefix pkg
# list installed
dnf list installed     | apt list --installed   | brew list
```

**Key behavioral gotchas:**

- apt splits `update` (refresh metadata) from `upgrade` (apply). dnf does an implicit metadata refresh on most operations (cached, configurable via `metadata_expire`). Forgetting `apt update` before `apt install` is the classic stale-cache bug; dnf rarely has this.
- brew runs as your user, installs into `/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel). No sudo. Casks handle GUI `.app` bundles. This is why brew can't manage the base OS — it's a userland overlay, not a system package manager.
- dnf is Python (slow startup, ~hundreds of ms). dnf5 (Fedora 41+) is a C++ rewrite — much faster. apt is C++, fast. brew is Ruby, slow-ish, network-heavy because of git.
- Transactional rollback: dnf has `dnf history undo <id>` — genuinely useful, undoes a whole transaction. apt has no native equivalent (you reconstruct from `/var/log/dpkg.log`). brew has none.

**For your setup:** on the Ubuntu workstation (192.168.x.x) and AMD cloud you're on apt — remember `apt update && apt install`. ROCm/MI300X tooling ships as `.deb` via AMD's apt repos, so apt is unavoidable there. On the M2 Air, brew. There's no dnf in your stack unless you spin a Fedora droplet, which you don't.

One AI-native note: for reproducible ML envs, none of these are the right layer — pin with `uv`/`pip` + a container (`apt` inside the Dockerfile for system libs like `libnuma`, ROCm). Treat apt as the system-lib provider, not the env manager.
