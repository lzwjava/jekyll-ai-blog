---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Git Bash Warp Proc Lock Error
translated: false
type: note
---

**Question:** How to fix the Cygwin/MSYS2 `get_proc_lock` / `sync_proc_subproc` error when using Git Bash as a terminal profile in Warp on Windows?

**Answer:**

The error is a classic Cygwin fork/proc locking issue:

```
[sig] bash 10696! get_proc_lock: Couldn't acquire sync_proc_subproc for(4,0), last 2, Win32 error 0
[sig] bash 10696! proc_subproc: couldn't get proc lock. what 4, val 0
```

This happens because Warp injects its own PTY/shell hooks that conflict with Cygwin's process synchronization primitives. Git Bash is MSYS2/Cygwin-based, so it's sensitive to how the parent process sets up the environment.

**Fix options, in order of effectiveness:**

**1. Launch Git Bash with `--login -i` flags in Warp's profile**

In Warp → Settings → Features → Terminal Profiles, set the shell command to:

```
C:\Program Files\Git\bin\bash.exe --login -i
```

The `--login` flag ensures `.bash_profile` is sourced properly and Cygwin initializes its runtime correctly before Warp's hooks fire.

**2. Disable Warp's shell integration for Git Bash**

Warp's shell integration (for prompt detection, command blocks, etc.) injects code that forks subprocesses — exactly what triggers this. In Warp settings, disable shell integration specifically for Git Bash, or add to your `~/.bashrc`:

```bash
unset WARP_IS_LOCAL_SHELL_SESSION
```

**3. Set `MSYS` env var to suppress fork warnings**

Add to your Git Bash `.bashrc` or set in Warp's profile environment variables:

```
MSYS=winsymlinks:nativestrict
MSYS2_ARG_CONV_EXCL="*"
```

More directly, the fork error is sometimes suppressed by:

```
MSYS=disable_pcon
```

**4. Use Git Bash via `mintty` wrapper instead of bare `bash.exe`**

```
C:\Program Files\Git\git-bash.exe
```

But this opens a separate window — not ideal for Warp embedding.

**5. Switch to WSL2 as your Warp profile instead**

Honestly the cleanest fix. Git Bash on Windows is a compatibility shim. If you're doing serious dev work (which you are), WSL2 Ubuntu in Warp gives you a real Linux environment without the Cygwin proc-lock nonsense. Warp's shell integration works natively with WSL2 bash/zsh.

**Root cause in one sentence:** Warp forks child processes to implement its command detection, and Cygwin's `sync_proc_subproc` mutex times out or fails when the parent process (Warp) doesn't conform to Cygwin's expected process tree — Win32 error 0 means the lock object wasn't found, not a permission error.