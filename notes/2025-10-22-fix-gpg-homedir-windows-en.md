---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing GPG Homedir Paths on Windows
translated: false
type: note
---

Yes, you're correct. In Git Bash on Windows (which runs on an MSYS2/Cygwin-like environment), using backslashes (`\`) in the `--homedir` path for `gpg` causes the shell to misinterpret the argument due to how escapes and path conversions work. This mangles the path (e.g., `C:\Users\me\.gnupg` might resolve to something invalid like `C:Usersme.gnupg` or get further garbled during auto-conversion to Windows format), making the directory unresolvable. As a result, GPG can't locate the key files, leading to a "no secret key" error (or similar, like "No such file or directory" for `pubring.kbx`).

### Quick Fix
- Use forward slashes (`/`) with the MSYS2-style drive prefix: `gpg --homedir /c/Users/me/.gnupg ...`
- This gets automatically converted by MSYS2 to the proper Windows path (e.g., `C:\Users\me\.gnupg`) when passed to the native GPG binary.
- Avoid drive letters like `c:/` without the leading `/`—they're treated as relative paths, prepending your current working directory and causing the same lookup failure.

For environment variables like `GNUPGHOME`, the same rule applies: set it with `/` (e.g., `export GNUPGHOME=/c/Users/me/.gnupg`).

[MSYS2 Filesystem Paths](https://www.msys2.org/docs/filesystem-paths/)
[GNUPGHOME in MSYS2 Discussion](https://lists.gnupg.org/pipermail/gnupg-users/2025-February/067536.html)
[GPG --homedir Bug on Windows/MSYS2](https://www.reddit.com/r/GnuPG/comments/1cl4dw8/bug_windows_homedir_with_drive_letter_treated_as/)
