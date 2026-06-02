---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decrypt Firefox Saved Passwords Tool
translated: false
type: note
---

**Question:** What is the firefox-decrypt tool and how does it work?

**Answer:**

**firefox-decrypt** (most commonly referring to https://github.com/unode/firefox_decrypt) is a popular open-source Python script designed to extract and decrypt saved passwords from Mozilla-based browser/email profiles.

It supports:

- Firefox
- Waterfox
- Thunderbird
- SeaMonkey
- and various derivative products

### What it actually does

Firefox (and related applications) store saved logins in files inside your profile folder:

- `logins.json` — contains the list of websites + encrypted username + encrypted password
- `key4.db` (newer Firefox versions) or older `key3.db` — contains the encryption keys

All passwords are encrypted using symmetric encryption (historically 3DES-CBC, later versions moved toward AES).

The encryption key is protected in two ways:

1. **No master password** → key is stored in a decryptable form (protected only by OS login / file permissions)
2. **Master password set** → key itself is encrypted with a key derived from your master password (using 3DES or PBKDF2 + AES in newer versions)

**firefox-decrypt** reads these files and:

- If no master password is used → immediately shows all passwords
- If a master password exists → prompts you to enter it, then decrypts everything

It **does not** perform any brute-force, dictionary, or cracking of the master password — you must know it.

### Basic usage

```bash
# Clone the repo
git clone https://github.com/unode/firefox_decrypt.git
cd firefox_decrypt

# Run it (Python 3.9+ required in recent versions)
python3 firefox_decrypt.py
```

Typical output flow:

1. Lists detected profiles (if multiple exist)
2. You select one (or it auto-picks the default)
3. If master password is set → prompts: `Master Password:`
4. Prints table with: hostname, username, password (and sometimes more fields)

You can also point it directly to a profile folder:

```bash
python3 firefox_decrypt.py /path/to/your/profile
```

### Important notes (2025–2026 era)

- Works well on Firefox versions up to ~120–130 without major issues
- Firefox 144+ reportedly introduced AES-256-CBC changes in some cases — the original firefox-decrypt may need updates or forks for perfect compatibility
- Many people now use **LaZagne**, **HackBrowserData**, **firepwd.py**, or **browser password dumpers** that include Firefox support and handle newer formats more reliably
- For legal & ethical forensics/recovery use only (your own machine, incident response with authorization, CTF challenges, etc.)

### Alternatives worth knowing

- **firepwd.py** (https://github.com/lclevy/firepwd) — pure Python, no NSS dependency, very educational
- **NSS-based tools** — use real Mozilla NSS libraries (pwdecrypt, modutil, etc.)
- **LaZagne** — multi-browser password extractor (includes Firefox module)
- GUI tools: PasswordFox (NirSoft), Browser Password Recovery tools

In short: **firefox-decrypt** is the classic, lightweight, command-line way many people (pentesters, forensic analysts, CTF players, forgetful users) have used for ~10 years to read saved Firefox passwords when they have profile access and — when needed — know the master password.

**References:**

- [https://github.com/unode/firefox_decrypt](https://github.com/unode/firefox_decrypt)
- [https://github.com/lclevy/firepwd](https://github.com/lclevy/firepwd)
