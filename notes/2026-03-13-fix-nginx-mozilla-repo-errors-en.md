---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Nginx Mozilla Repo Errors Quickly
translated: false
type: note
---

Question: How do I fix the `nginx/binary-i386/Packages` architecture warning and the Mozilla apt repository `400 Bad Request` error, and how do I remove those repositories?

Answer:

You have **two separate issues** to fix:

---

## Issue 1: Nginx i386 Architecture Warning (N: warning)

This is **not a real error** — it's just a notice. Your system is trying to fetch i386 (32-bit) packages from the nginx repo, but nginx only publishes amd64 packages.

### Option A: Fix by specifying arch in the repo file (Recommended)

Edit the nginx source file and add `arch=amd64` to restrict it to 64-bit only:

```bash
sudo nano /etc/apt/sources.list.d/nginx.list
```

Change this:
```
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```

To this:
```
deb [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```

If there is no `signed-by` part, just add `[arch=amd64]` like this:
```
deb [arch=amd64] http://nginx.org/packages/ubuntu jammy nginx
```

### Option B: Remove the nginx repository entirely

If you want to **completely remove** the nginx external repo:

```bash
sudo rm /etc/apt/sources.list.d/nginx.list
```

---

## Issue 2: Mozilla Repository `400 Bad Request` (E: error — this one IS a real error)

The `400 Bad Request [IP: 127.0.0.1 7890]` error means your system is going through a **local proxy** (port 7890, likely Clash or a similar proxy tool), and the proxy is blocking or mishandling the request to `packages.mozilla.org`.

### Fix A: Remove the Mozilla apt repository (cleanest solution)

Find the Mozilla source file:

```bash
ls /etc/apt/sources.list.d/ | grep -i mozilla
```

Then remove it:

```bash
sudo rm /etc/apt/sources.list.d/mozilla.list
# or whatever the filename is, e.g.:
sudo rm /etc/apt/sources.list.d/mozillateam-ubuntu-ppa-jammy.list
```

Also remove the associated GPG key if present:

```bash
sudo rm /usr/share/keyrings/mozillateam-archive-keyring.gpg
```

### Fix B: Bypass the proxy for this specific domain

If you want to keep the Mozilla repo but fix the proxy issue, add a proxy bypass for `packages.mozilla.org` in your proxy software (e.g., Clash), or set `no_proxy` for apt:

```bash
sudo nano /etc/apt/apt.conf.d/99proxy-bypass
```

Add:
```
Acquire::https::packages.mozilla.org::DIRECT "true";
```

---

## After Fixing — Run Update to Verify

```bash
sudo apt update
```

You should no longer see the `N:` warning or the `E:` error.

---

## Summary Table

| Issue | Type | Solution |
|---|---|---|
| `nginx binary-i386` | Warning (N:) | Add `arch=amd64` to nginx.list, or remove the file |
| `Mozilla 400 Bad Request` | Error (E:) | Remove mozilla source file, or fix proxy bypass |

References:

- [Fix nginx i386 architecture warning](https://ariq.nauf.al/blog/n-skipping-acquire-of-configured-file-nginx-binary-i386-packages-as-repository-http-nginx-org-packages-ubuntu-bionic-inrelease-doesnt-support-architecture-i386/)
- [How to fix APT i386 architecture warning — TechOverflow](https://techoverflow.net/2025/01/27/how-to-fix-apt-skipping-acquire-of-configured-file-doesn-t-support-architecture-i386/)
- [Repository doesn't support architecture i386 — It's FOSS](https://itsfoss.com/repository-doesnt-support-architecture-i386/)