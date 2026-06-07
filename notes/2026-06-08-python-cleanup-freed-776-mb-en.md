---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Cleanup Freed 776 MB
translated: false
type: note
---

## Python Cleanup Summary

**Started with:** 5 Python installations
**Ended with:** 3 Python installations (2 Homebrew + 1 system)

---

### Removed

| What | Version | How | Freed |
|------|---------|-----|-------|
| python.org framework | 3.11.6 | `sudo rm -rf /Library/Frameworks/Python.framework` + 14 symlinks in `/usr/local/bin` + `/Applications/Python 3.11` | ~200 MB |
| python@3.13 (Homebrew) | 3.13.12 | `brew uninstall` (auto-removed as orphan after awscli/azure-cli deleted) | 72 MB |
| awscli | 2.34.19 | `brew uninstall` | 154 MB |
| azure-cli | 2.84.0 | `brew uninstall` | 350 MB |

**Total freed:** ~776 MB

---

### Remaining

| Path | Version | Role | Depended on by |
|------|---------|------|----------------|
| `/opt/homebrew/bin/python3` | 3.14.3 | **Default** (`python3`) | llvm, nmap, rust, yt-dlp, docutils + 85 tools |
| `/opt/homebrew/bin/python3.11` | 3.11.14 | ML workhorse | accelerate, ctranslate2, chroma, alembic + 75 tools |
| `/usr/bin/python3` | 3.9.6 | **macOS system** (Xcode CLT) | macOS internals, Xcode — can't remove (SIP protected) |

---

### Side effects

- Bare `python3` now resolves to `/usr/bin/python3` (3.9.6) instead of Homebrew's 3.14.3, because `/usr/bin` comes before `/opt/homebrew/bin` in your PATH. The old python.org symlink in `/usr/local/bin` was previously winning. Fix: `ln -s /opt/homebrew/bin/python3 /usr/local/bin/python3`
- The 464 pip packages and 20 tools (ansible, ipython, markdown2, etc.) that were under the old python@3.13 are gone. Reinstall under python@3.14 if needed: `pip3 install ansible ipython markdown2`
