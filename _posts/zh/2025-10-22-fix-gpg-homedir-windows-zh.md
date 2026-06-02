---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复Windows上的GPG主目录路径
translated: true
type: note
---

是的，您说得对。在 Windows 的 Git Bash（运行在类似 MSYS2/Cygwin 的环境下）中，在 `gpg` 的 `--homedir` 路径中使用反斜杠（`\`）会导致 shell 因转义和路径转换机制而误解该参数。这会破坏路径（例如 `C:\Users\me\.gnupg` 可能被解析为类似 `C:Usersme.gnupg` 这样的无效路径，或在自动转换为 Windows 格式时进一步混乱），使得目录无法被解析。因此，GPG 无法定位密钥文件，导致“没有私钥”错误（或类似错误，例如 `pubring.kbx` 的“没有该文件或目录”错误）。

### 快速解决方法
- 使用正斜杠（`/`）并加上 MSYS2 风格的驱动器前缀：`gpg --homedir /c/Users/me/.gnupg ...`
- 这样在传递给原生 GPG 二进制文件时，MSYS2 会自动将其转换为正确的 Windows 路径（例如 `C:\Users\me\.gnupg`）。
- 避免使用不带前导 `/` 的驱动器字母（如 `c:/`）——它们会被视为相对路径，会在当前工作目录前加上该路径，导致同样的查找失败问题。

对于像 `GNUPGHOME` 这样的环境变量，同样适用此规则：使用 `/` 来设置它（例如 `export GNUPGHOME=/c/Users/me/.gnupg`）。

[MSYS2 文件系统路径](https://www.msys2.org/docs/filesystem-paths/)
[MSYS2 中关于 GNUPGHOME 的讨论](https://lists.gnupg.org/pipermail/gnupg-users/2025-February/067536.html)
[Windows/MSYS2 上的 GPG --homedir 错误](https://www.reddit.com/r/GnuPG/comments/1cl4dw8/bug_windows_homedir_with_drive_letter_treated_as/)
