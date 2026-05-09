---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Zig CLI Tutorial
translated: false
type: note
---

A short walkthrough of what we just did: from zero Zig installed, to a working CLI that prints `Hello, world!` plus system info, pushed to GitHub.

## 1. Install the toolchain

```sh
brew install zig
zig version   # 0.15.2
```

That pulls in `llvm@20` and `lld@20` as deps. ~200 MB on disk.

## 2. Scaffold the project

```sh
zig init
```

This creates four files:

```
build.zig         # build script (DSL over std.Build)
build.zig.zon     # package manifest (name, version, deps)
src/main.zig      # entry point
src/root.zig      # library module
```

`zig init` assumes you might want both an executable and a reusable library. For a single-file CLI you don't, so I deleted `src/root.zig` and stripped `build.zig` down to ~20 lines — just executable + `run` step. The default scaffold is ~150 lines mostly comments.

## 3. The CLI

Two things worth noting in `src/main.zig`:

**Zig 0.15's new writer API.** The old `std.io.getStdOut().writer()` is gone. The new pattern is explicit: you supply the buffer, get a `File.Writer`, and grab its `interface`:

```zig
var stdout_buffer: [4096]u8 = undefined;
var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
const out = &stdout_writer.interface;

try out.print("Hello, world!\n", .{});
// ...
try out.flush();   // don't forget this
```

The buffer lives on the stack. You decide its size. You also have to call `flush()` yourself — buffered IO is no longer hidden behind a polymorphic writer.

**Where system info comes from.** Three different sources, depending on what kind of fact it is:

| Fact                  | Source                                                                |
| --------------------- | --------------------------------------------------------------------- |
| OS, arch, Zig version | `@import("builtin")` — comptime constants baked into the binary       |
| Hostname, kernel      | `std.posix.uname()` — POSIX syscall                                   |
| CPU count             | `std.Thread.getCpuCount()`                                            |
| User, shell           | `std.process.getEnvVarOwned(allocator, "USER")` — env vars, allocated |
| Cwd                   | `std.posix.getcwd(&buf)` — fills a stack buffer                       |
| Time                  | `std.time.timestamp()`                                                |

`builtin` is the interesting one: `builtin.os.tag` and `builtin.cpu.arch` are *compile-time* enums, so `@tagName()` gives you the string with zero runtime cost. The build target is the answer.

`uname` returns fixed-size null-terminated arrays (`[65]u8` or so). To print them as Zig slices, you need `std.mem.sliceTo(&uts.nodename, 0)` to find the null terminator.

`getEnvVarOwned` returns an error union, not an optional — `USER` may genuinely not be set. The idiomatic handling:

```zig
if (std.process.getEnvVarOwned(allocator, "USER")) |u| {
    defer allocator.free(u);
    try out.print("User: {s}\n", .{u});
} else |_| {
    try out.print("User: (unknown)\n", .{});
}
```

The `|u|` / `else |_|` split handles success and error in one expression. The success branch owns the allocation and must free it.

## 4. Build and run

```sh
zig build run        # build + run
zig build            # build → ./zig-out/bin/ii
```

Output:

```
Hello, world!

== System Info ==
OS:           macos
Architecture: aarch64
Zig version:  0.15.2
Hostname:     lzw-mac.local
Kernel:       Darwin 25.4.0
CPU cores:    8
Working dir:  /Users/lzwjava/projects/ii
User:         lzwjava
Shell:        /bin/zsh
Unix time:    1778318750
```

## 5. Git

```sh
git init
echo -e ".zig-cache/\nzig-out/" > .gitignore
git add .gitignore build.zig build.zig.zon src/main.zig
git commit -m "Initial commit: Zig CLI printing hello world and system info"
git remote add origin git@github.com:lzwjava/ii.git
git push -u origin main
```

`.zig-cache/` and `zig-out/` are the two things to ignore — incremental cache and install prefix respectively.

## Takeaways

- `zig init` gives you a generous scaffold; trim it.
- The 0.15 IO rewrite is more verbose but more honest — you see the buffer, you call `flush`.
- Most "system info" on Unix is one of: comptime `builtin`, a POSIX syscall (`uname`, `getcwd`), or an env var.
- Total source: ~50 lines of Zig + a 20-line build script.

Repo: `git@github.com:lzwjava/ii.git`