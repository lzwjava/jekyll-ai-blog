---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH key permission fix
translated: false
type: note
---

Fixed. The file went from `0644` (`-rw-r--r--`) to `0600` (`-rw-------`).

## What the permissions mean

| | Before (`0644`) | After (`0600`) |
| --- | --- | --- |
| Owner | read ✅ write ✅ | read ✅ write ✅ |
| Group | read ✅ | ❌ |
| Others | read ✅ | ❌ |

SSH refuses to use a private key if **anyone other than the owner** can read it, because that's a security risk.

## Notes

- `0600` = owner only (most common for personal keys)
- `0400` = owner read-only (even stricter, also works)
- The `@` after the permissions means the file has **extended attributes** (likely macOS quarantine/Spotlight metadata) — this is harmless and unrelated to the SSH error.
- You don't need `chown` (change owner) — the file already belongs to you (`lzwsta`). The problem was just the permission **bits**, which `chmod` fixed.

You should now be able to use the key without the "bad permissions" warning:

```bash
ssh -i private_key.pem user@host
```
