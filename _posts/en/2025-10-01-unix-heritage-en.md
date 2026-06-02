---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Unix Heritage of macOS and Linux
translated: false
type: note
---

### Common Origins of macOS and Linux

MacOS (formerly OS X) and Linux share conceptual roots in Unix, a pioneering multitasking operating system developed at Bell Labs in the 1970s. Linux, created by Linus Torvalds in 1991, is an open-source kernel modeled after Unix but developed independently—it's not derived from Unix source code. macOS, meanwhile, is built on Darwin (a Unix-like OS from Apple, based on FreeBSD), which includes Unix components and is certified as Unix-compliant by The Open Group. This shared heritage explains many similarities in tools and commands, as both aim to provide Unix-like functionality.

Supporting evidence: Unix's standards (e.g., POSIX) influenced both systems to ensure compatibility. Linux distributions like Ubuntu are explicitly Unix-like, and macOS inherits Unix tools through BSD (Berkeley Software Distribution), another early Unix branch.

### Why They Both Have the 'ps' Command

The 'ps' (process status) command displays information about running processes and originates directly from Unix, where it was first implemented in the 1970s. Both macOS and Linux include 'ps' because:

- It's part of their Unix heritage: macOS via Darwin/FreeBSD, and Linux via the PROC filesystem and standard utilities from GNU or POSIX specifications.
- It's essential for system diagnostics, scripting, and administration, so it's bundled by default in their core toolsets (e.g., in macOS's Terminal or Linux's shell).

The command syntax, like `ps -p pid -o pid,ppid,lstart,etime,command`, is supported on both due to shared POSIX standards, though options might vary slightly (e.g., macOS has BSD-flavored flags, while Linux often uses GNU variants). This isn't a coincidence—it's a direct lineage from Unix.

### Can We Say macOS and Linux Are Both Unix?

Not exactly: "Unix" is a family of OSes and a registered trademark. macOS qualifies as Unix because Darwin is certified (by The Open Group) and complies with Single Unix Specification (SUS). Linux, however, is a kernel that forms the basis for full OSes (distros like Debian), but the kernel itself and its distros are not officially "Unix"—they're Unix-like or Unix-compatible due to their adherence to POSIX without full certification or shared codebase.

You could say they are "Unix-like" or "bearers of Unix traditions," but calling them "all Unix" would be inaccurate for Linux. In practice, this doesn't matter much for most users, as they behave similarly for commands like 'ps'. If strictness is key, check certifications or refer to the official definitions.
