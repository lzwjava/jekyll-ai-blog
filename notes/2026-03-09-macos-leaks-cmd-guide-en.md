---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Leaks Command Guide
translated: false
type: note
---

**Question:** How do you use the `leaks` command in macOS to search for leaked memory in a process?

**Answer:**

## Overview

The `leaks` command identifies leaked memory — memory that an application has allocated but has been lost and cannot be freed. It examines a specified process's memory for values that may be pointers to `malloc`-allocated buffers. Any buffer not reachable from a pointer in writable global memory, a register, or the stack is considered a leak.

The tool is located at `/usr/bin/leaks` and is built into macOS — no installation required.

---

## Basic Usage Syntax

```
leaks [options] pid | partial-process-name | memory-graph-file
leaks [options] --atExit -- <command-and-arguments>
```

---

## Method 1: Inspect a Running Process by PID

Find the PID first using `ps` or `pgrep`, then run:

```bash
# Get the PID
ps aux | grep MyApp

# Run leaks against it
leaks 12345
```

Or use the partial process name directly:

```bash
leaks MyApp
```

---

## Method 2: Launch and Inspect at Exit (`--atExit`)

This is the most common and convenient method for command-line programs.

```bash
leaks --atExit -- ./my_program
leaks --atExit -- ./my_program arg1 arg2
```

Using `-atExit` will automatically set `MallocStackLogging=lite` for the specified command so that stack backtraces can be shown for leaked allocations.

For full stack trace detail, set it manually:

```bash
MallocStackLogging=YES leaks -quiet -atExit -- ./my_program
```

---

## Method 3: Enable Stack Logging Before Running

For richer output including allocation stack traces:

```bash
# In one terminal: launch your program with stack logging
MallocStackLogging=1 ./my_program &

# In another terminal: run leaks against it
leaks <PID>
```

---

## Common Options

| Option | Description |
|---|---|
| `-quiet` | Suppress informational output, show only leaks |
| `-nocontext` | Do not print hex/string content of leaked memory |
| `-nostacks` | Skip printing backtraces of leaked blocks |
| `-exclude <symbol>` | Exclude leaks whose backtrace includes the given symbol (can be repeated) |
| `-trace <address>` | Print reference chain from roots to a specific block |
| `-outputGraph <path>` | Save a `.memgraph` file for later analysis |
| `-fullContent` | Include full object content in the memory graph file |
| `-list` | List all leaked blocks |
| `-groupByType` | Group leaked blocks by type |

The `-exclude` option allows ignoring leaks that are allocated in libraries for which you do not have source code.

---

## Practical Examples

**Basic check on a running app:**

```bash
leaks Safari
```

**Quiet mode — only show leaks:**

```bash
leaks -quiet --atExit -- ./myapp
```

**With stack trace logging:**

```bash
MallocStackLogging=1 leaks -quiet -atExit -- ./myapp
```

**Filter to show only leak lines (grep):**

```bash
leaks --atExit -- ./myapp | grep LEAK:
```

**Exclude known system leaks:**

```bash
leaks --atExit -exclude CFRunLoopRun -- ./myapp
```

**Save a memory graph for later analysis:**

```bash
leaks --outputGraph /tmp/myapp.memgraph --atExit -- ./myapp
```

**Analyze a saved memory graph:**

```bash
leaks /tmp/myapp.memgraph
```

---

## Environment Variables

| Variable | Effect |
|---|---|
| `MallocStackLogging=1` | Records stack traces for all allocations |
| `MallocStackLogging=lite` | Lighter-weight stack logging (used by `-atExit` automatically) |
| `MallocScribble=1` | Fills freed blocks with `0x55`, reducing false pointer matches |

The `leaks` command may detect more leaks if the target process is run with the `MallocScribble` environment variable. When set, freed malloc blocks are filled with `0x55` bytes, overwriting stale pointer data and reducing false positives.

---

## Exit Status

The `leaks` command exits with: `0` if no leaks were detected, `1` if one or more leaks were detected, and `>1` if an error occurred.

This makes it easy to use in scripts:

```bash
leaks -quiet --atExit -- ./myapp
if [ $? -eq 1 ]; then
    echo "Memory leaks found!"
fi
```

---

## Tips for Better Results

- Run `leaks` during unit testing, because unit testing exercises all code paths in a repeatable manner, making you more likely to find leaks than in a production environment.
- If `leaks` reports a leak intermittently, set up a loop around the target code path and run the code hundreds or thousands of times to increase the likelihood of the leak reappearing consistently.
- For a GUI alternative, Xcode's **Instruments** app includes a Leaks instrument with the same detection capabilities plus visual call tree analysis.

**References:**

- [leaks man page (unix.com)](https://www.unix.com/man-page/osx/1/leaks/)
- [leaks man page (keith.github.io)](https://keith.github.io/xcode-man-pages/leaks.1.html)
- [Apple Developer: Finding Memory Leaks](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/ManagingMemory/Articles/FindingLeaks.html)
- [EECS 280 Leak Checking Tutorial](https://eecs280staff.github.io/tutorials/setup_leakcheck.html)
- [Detect memory leaks on macOS (Medium)](https://dr-rost.medium.com/detect-memory-leaks-on-macos-4cf257529aa)
