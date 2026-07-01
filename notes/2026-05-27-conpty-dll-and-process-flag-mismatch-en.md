---
audio: false
generated: true
image: false
lang: en
layout: post
title: ConPTY DLL and Process Flag Mismatch
translated: false
type: note
---

Now I have a complete picture. Here's the analysis:

---

## Why `terminal` (Windows Terminal) works with git-bash but `warp` doesn't

There are 5 key architectural differences, and the combination is what causes the MSYS2 fork() deadlock in Warp.

### 1. ConPTY Library: Static vs Bundled DLL

**Windows Terminal** builds ConPTY from source as a static library:

- `src/inc/conpty-static.h` — direct symbol linkage
- Uses newer APIs: `ConptyReparentPseudoConsole`, `ConptyPackPseudoConsole`, `ConptyClearPseudoConsole`
- The ConPTY code is at `src/winconpty/winconpty.cpp` — built alongside Terminal, always the latest version with all fork() fixes

**Warp** loads `conpty.dll` dynamically at runtime:

- `conpty_api.rs:57`: `HSTRING::from("conpty.dll")`
- Bundled from `assets/windows/{arch}/conpty.dll`
- Only loads: `CreatePseudoConsole`, `ResizePseudoConsole`, `ClosePseudoConsole`, `ConptyShowHidePseudoConsole`, `ConptyReleasePseudoConsole`
- Missing the newer APIs entirely

This is likely the **primary cause**. Windows Terminal's ConPTY has been patched over the years to handle MSYS2/Cygwin fork() edge cases. The bundled DLL Warp uses may predate those fixes.

### 2. Pipe Architecture: Duplex vs Split

**Windows Terminal** uses a single duplex pipe for both ConPTY directions:

```cpp
// ConptyConnection.cpp:411-412
auto pipe = Utils::CreateOverlappedPipe(PIPE_ACCESS_DUPLEX, 128 * 1024);
ConptyCreatePseudoConsole(size, pipe.client.get(), pipe.client.get(), _flags, &_hPC);
//                           ^^^^same handle for both in/out
```

**Warp** uses separate pipes:

```rust
// mod.rs:131-135
let pipes::DuplexPipe { client, server } = pipes::create_async_anonymous_pipe()?;
conpty_api.create(size.to_coord(), client, 0)
```

The duplex pipe in Windows Terminal means the ConPTY server reads and writes through the same handle, which creates a more stable I/O path for MSYS2's fork() — the child process inherits a single unified console handle rather than separate ones.

### 3. CREATE_BREAKAWAY_FROM_JOB

**Windows Terminal**:

```cpp
// ConptyConnection.cpp:172
EXTENDED_STARTUPINFO_PRESENT | CREATE_UNICODE_ENVIRONMENT
```

**Warp**:

```rust
// mod.rs:194-197
PROCESS_CREATION_FLAGS(0)
    | EXTENDED_STARTUPINFO_PRESENT
    | CREATE_UNICODE_ENVIRONMENT
    | CREATE_BREAKAWAY_FROM_JOB  // <--- extra flag
```

`CREATE_BREAKAWAY_FROM_JOB` lets the spawned process break out of any job object hierarchy. ConPTY uses job objects internally to manage the pseudo-console process tree. When MSYS2's bash does fork(), the child might inherit the breakaway flag and detach from ConPTY's process management, corrupting the `sync_proc_subproc` mutex state.

### 4. ConPTY Flags: 0 vs Feature Flags

**Windows Terminal** passes feature flags:

```cpp
// ConptyConnection.cpp:412
ConptyCreatePseudoConsole(size, in, out, _flags, &_hPC)
// _flags can include: PSEUDOCONSOLE_INHERIT_CURSOR,
//   PSEUDOCONSOLE_GLYPH_WIDTH_GRAPHEMES, PSEUDOCONSOLE_AMBIGUOUS_IS_WIDE
```

**Warp** passes 0:

```rust
// mod.rs:135
conpty_api.create(size.to_coord(), client, 0)  // flags = 0
```

### 5. Windows Terminal Reparents the Console

Windows Terminal calls `ConptyReparentPseudoConsole` to attach the pseudo-console to its window handle. This establishes a proper window hierarchy that ConPTY uses to manage focus and input routing. Warp doesn't call this, which might leave ConPTY in a less stable state for child process management.

### Summary

| Aspect | Windows Terminal | Warp |
| -------- | ----------------- | ------ |
| ConPTY lib | Static, built from source | Bundled DLL, possibly older |
| Pipe setup | Single duplex pipe | Separate client/server pipes |
| Process flags | `EXTENDED_STARTUPINFO_PRESENT \| CREATE_UNICODE_ENVIRONMENT` | Same + `CREATE_BREAKAWAY_FROM_JOB` |
| ConPTY flags | Feature flags for cursor, glyph width | `0` |
| Console reparent | Yes (`ConptyReparentPseudoConsole`) | No |

The root cause is most likely **#1 + #3**: an older ConPTY DLL that lacks fork() fixes, combined with `CREATE_BREAKAWAY_FROM_JOB` which disrupts ConPTY's job object management during MSYS2's fork() emulation.

### Potential Fixes for Warp

1. **Remove `CREATE_BREAKAWAY_FROM_JOB`** from the MSYS2 spawn path — it's not needed for shell processes
2. **Update the bundled `conpty.dll`** to the latest from Windows Terminal's build
3. **Use a duplex pipe** instead of split pipes for ConPTY I/O
4. **Load newer ConPTY APIs** (`ConptyReparentPseudoConsole`, `ConptyPackPseudoConsole`) for better console lifecycle management
