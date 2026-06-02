---
audio: false
generated: true
image: false
lang: en
layout: post
title: Alacritty's ConPTY Implementation Analysis
translated: false
type: note
---

**Alacritty is much more like Warp than Windows Terminal.** Here's the point-by-point comparison:

## ConPTY Library Loading

Alacritty (conpty.rs:51-88):

```rust
fn new() -> Self {
    match Self::load_conpty() {
        Some(conpty) => { /* use conpty.dll */ },
        None => { /* fallback to Windows API */ },
    }
}
fn load_conpty() -> Option<Self> {
    let hmodule = LoadLibraryW(w!("conpty.dll"));
    // loads: CreatePseudoConsole, ResizePseudoConsole, ClosePseudoConsole
}
```

**Verdict: Like Warp** — dynamic loading of conpty.dll. Only loads the same 3 functions. BUT with a key difference: Alacritty falls back to the Windows built-in API if conpty.dll isn't found. Warp bundles its own DLL and crashes if it's bad.

## Pipe Architecture

Alacritty (conpty.rs:118-119):

```rust
let (conout, conout_pty_handle) = miow::pipe::anonymous(0)?;
let (conin_pty_handle, conin) = miow::pipe::anonymous(0)?;
```

**Verdict: Like Warp** — separate client/server pipes, NOT a duplex pipe like Windows Terminal.

## Process Creation Flags

Alacritty (conpty.rs:207-211):

```rust
let mut creation_flags = EXTENDED_STARTUPINFO_PRESENT;
// CREATE_UNICODE_ENVIRONMENT only if custom env is set
```

**Verdict: Like Windows Terminal** — NO `CREATE_BREAKAWAY_FROM_JOB`. This is a significant difference from Warp.

## ConPTY Flags

Alacritty (conpty.rs:127):

```rust
(api.create)(window_size.into(), conin_handle, conout_handle, 0, &mut pty_handle)
```

**Verdict: Like Warp** — passes `0` for flags. Windows Terminal passes feature flags.

## No ConptyReparentPseudoConsole

**Verdict: Like Warp** — doesn't call it. Only loads 3 APIs.

## Summary Table

| Aspect              | Win Terminal          | Warp                    | Alacritty               |
|---------------------|-----------------------|-------------------------|-------------------------|
| ConPTY lib          | Static, built-in      | Bundled conpty.dll      | conpty.dll w/ fallback  |
| Pipe setup          | Single duplex         | Split pipes             | Split pipes             |
| CREATE_BREAKAWAY    | No                    | **Yes**                 | No                      |
| ConPTY flags        | Feature flags         | 0                       | 0                       |
| Reparent console    | Yes                   | No                      | No                      |
| APIs loaded         | All (static)          | 3                       | 3                       |

## Conclusion

Alacritty is **70% Warp, 30% Windows Terminal**. It shares Warp's architecture on 4 out of 5 dimensions, but critically avoids `CREATE_BREAKAWAY_FROM_JOB` — which your analysis identified as one of the two primary root causes (along with the older ConPTY DLL).

This means for the git-bash/MSYS2 fork() deadlock:

- **Alacritty should behave better than Warp** because it avoids the `CREATE_BREAKAWAY_FROM_JOB` problem
- **But it's still vulnerable** to the stale conpty.dll issue (split pipes + no newer APIs)
- **The fallback to Windows API** is actually a safety net — if conpty.dll is missing, it uses whatever ConPTY ships with Windows, which may have fork() fixes if the OS is up-to-date

The practical implication: if you're debugging a fork() deadlock in Alacritty on Windows with git-bash, the first thing to check is which ConPTY version it actually loaded — the bundled conpty.dll or the system API. The `info!("Using conpty.dll...")` / `info!("Using Windows API...")` log line tells you.
