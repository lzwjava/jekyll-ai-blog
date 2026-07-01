---
audio: false
generated: true
image: false
lang: en
layout: post
title: ConPTY MSYS2 Fork Emulation Conflict
translated: false
type: note
---

Based on the code, here's the analysis:

## Root Cause

The `get_proc_lock` / `sync_proc_subproc` error is a Cygwin/MSYS2 fork() emulation issue caused by ConPTY (Windows Pseudo Console) interference.

From the spawn code in `app/src/terminal/local_tty/windows/mod.rs:159-161`:

```rust
ShellStarter::Direct(shell_starter) | ShellStarter::MSYS2(shell_starter) => {
    shell_command(shell_starter)?
}
```

Both Direct and MSYS2 shells go through the same ConPTY path. ConPTY creates a pseudo-console via `CreatePseudoConsole`, then spawns bash with `CreateProcessW` attached to it.

From `app/src/terminal/local_tty/shell.rs:690-694`, MSYS2 bash is launched with:

```rust
ShellType::Bash => {
    vec!["--noprofile".into(), "--norc".into()]
}
```

The conflict: MSYS2's `fork()` emulation uses shared memory and a `sync_proc_subproc` mutex to track process state. ConPTY intercepts console handles and process creation, which can deadlock MSYS2's internal synchronization.

## Solutions

**1. Use `Git\usr\bin\bash.exe` (not `Git\bin\bash.exe`)**

Warp already canonicalizes this (`warp_util/src/path.rs:524-533`):

```rust
pub fn canonicalize_git_bash_path(mut path: PathBuf) -> PathBuf {
    if !path.ends_with(Path::new("Git").join("bin").join("bash.exe")) {
        return path;
    }
    // Converts Git\bin\bash.exe -> Git\usr\bin\bash.exe
}
```

The `bin\bash.exe` is a wrapper that spawns `usr\bin\bash.exe` as a child — double-forking through ConPTY amplifies the proc lock race.

**2. Set MSYS2 environment variables before launching Warp**

Add to your Windows system environment variables:

```
MSYS=winsymlinks:nativestrict
MSYS_NO_PATHCONV=1
```

Or create a batch wrapper:

```bat
@echo off
set MSYS=winsymlinks:nativestrict
set MSYS_NO_PATHCONV=1
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Warp\Warp.exe"
```

**3. Disable ConPTY for MSYS2 (if your Git version supports it)**

Git Bash ships with MSYS2's mintty. You can use mintty instead of ConPTY by launching:

```
"C:\Program Files\Git\git-bash.exe" --con-host
```

But this bypasses Warp entirely. For Warp integration, ConPTY is required.

**4. The error is usually non-fatal**

From the bootstrap script (`bash_init_shell.sh:9`):

```bash
if [[ "$OS" == Windows_NT ]]; then WARP_IN_MSYS2=true; fi
```

Warp detects MSYS2 and adjusts its bootstrap protocol (using OSC instead of DCS for hooks, key-value pairs instead of JSON). The `get_proc_lock` error prints to stderr but bash typically continues. If the session hangs, close the tab and open a new one.

**5. Avoid fork-heavy commands in Warp MSYS2 sessions**

Commands that heavily use `fork()` are most likely to trigger the error:

- `make` / `autotools`
- `git` operations on large repos
- `python` (MSYS2 python, not native Windows Python)
- Piped commands with `xargs`, `parallel`

For these, use WSL or native PowerShell instead.

**6. Use WSL as the primary shell**

From `app/src/terminal/local_tty/shell.rs:659-683`, WSL shells go through `wsl.exe` which avoids MSYS2 entirely. If you need Unix tools on Windows, WSL is more reliable than Git Bash through ConPTY.

## Summary

| Fix | Impact |
| ----- | -------- |
| Use `Git\usr\bin\bash.exe` | Warp does this automatically via `canonicalize_git_bash_path` |
| `MSYS_NO_PATHCONV=1` | Reduces fork-heavy path conversions |
| `MSYS=winsymlinks:nivestrict` | Reduces symlink emulation overhead |
| Avoid `make`/`git` in MSYS2 | Prevents the specific fork() calls that deadlock |
| Switch to WSL | Eliminates MSYS2 fork() entirely |

The error is fundamentally a ConPTY + MSYS2 fork() emulation incompatibility. There's no code-level fix in Warp for this — it's a Windows/MSYS2 limitation.
