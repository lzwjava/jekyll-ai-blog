---
audio: false
generated: true
image: false
lang: en
layout: post
title: Valgrind Memory Profiling Guide
translated: false
type: note
---

**Question:** How do you use Valgrind for memory profiling, and does it work on macOS?

---

**Answer:**

## What is Valgrind?

Valgrind is a suite of tools for debugging and profiling. It automatically detects memory management and threading bugs, and performs detailed profiling. The current stable version is 3.26.0.

Valgrind's architecture is modular, so new tools can be created easily. The main tools included are: **Memcheck** (memory error detector), **Cachegrind** (cache and branch-prediction profiler), **Callgrind** (call-graph generating cache profiler), **Helgrind** (thread error detector), and **DHAT** (heap profiler).

---

## Installation

**On Linux (Ubuntu/Debian):**

```bash
sudo apt-get install valgrind
```

**On macOS** — see the macOS section below.

---

## How to Use Valgrind

### Step 1: Compile with Debug Symbols

Compile your program with `-g` to include debugging information so that Memcheck's error messages include exact line numbers. Using `-O0` is also a good idea if you can tolerate the slowdown.

```bash
gcc -g -O0 -Wall myprogram.c -o myprogram
```

### Step 2: Run with Valgrind

The basic syntax is:

```bash
valgrind --tool=<toolname> <valgrind-options> ./myprogram [program-args]
```

Memcheck is the default Valgrind tool and can be run with `valgrind program` without specifying `--tool=memcheck`.

---

## Memcheck — Memory Error Detection

Memcheck is a memory error detector. It can detect: accessing memory you shouldn't (e.g., overrunning heap blocks, accessing memory after it has been freed), using undefined/uninitialized values, and memory leaks.

**Basic command:**

```bash
valgrind ./myprogram
```

**Full leak check command:**

```bash
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all -v ./myprogram
```

**Key flags for Memcheck:**

| Flag | Description |
| --- | --- |
| `--leak-check=full` | Show details of each individual memory leak |
| `--show-leak-kinds=all` | Show all types of leaks |
| `--track-origins=yes` | Report where undefined values came from |
| `-v` | Verbose output |

**Example output for a memory leak:**

```
==17624== HEAP SUMMARY:
==17624==     in use at exit: 40 bytes in 1 blocks
==17624==   total heap usage: 1 allocs, 0 frees, 40 bytes allocated
==17624== LEAK SUMMARY:
==17624==    definitely lost: 40 bytes in 1 blocks
```

Programs run ten to thirty times more slowly with Memcheck than when run normally.

---

## Massif — Heap Memory Profiler

Massif is a heap profiler — it measures how much heap memory your program uses. It can give you information about heap usage, heap admin bytes, and stack sizes. Heap profiling is useful to help reduce the amount of memory your program uses.

**Run Massif:**

```bash
valgrind --tool=massif ./myprogram
```

When the program finishes, Massif prints summary space statistics and creates a graph representing the program's heap usage in a file called `massif.<pid>.ps`, which can be read by any PostScript viewer.

**Visualize results:**

```bash
ms_print massif.out.<pid>
```

---

## Callgrind — Call Graph & Cache Profiler

To use Callgrind, simply pass the program executable along with any arguments:

```bash
valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./myprogram
```

Callgrind produces a large amount of data about the program's execution. It is most easily understood using the **kcachegrind** GUI tool, which creates a list of function calls along with timing information.

---

## Does Valgrind Work on macOS?

**Short answer: Not well natively, but there are workarounds.**

The official Valgrind does **not** support modern macOS versions (especially Apple Silicon / M1/M2 chips). However:

1. **Community macOS fork**: There is a community-maintained repository (`LouisBrunner/valgrind-macos`) that includes patches to improve support for the macOS platform. It can be installed via Homebrew by tapping that repository.

   ```bash
   export HOMEBREW_NO_INSTALL_FROM_API=1
   brew tap Homebrew/core
   brew tap LouisBrunner/valgrind
   brew install --HEAD LouisBrunner/valgrind/valgrind
   ```

2. **macOS native alternative — `leaks`**: `leaks` is a tool available on Mac computers that performs similar kinds of memory checking to Valgrind. Before running it, set `MallocStackLogging=1` in the terminal to preserve information about memory allocations.

   ```bash
   MallocStackLogging=1 ./myprogram &
   leaks myprogram
   ```

3. **Xcode Instruments**: Apple's Xcode includes Instruments, which provides memory profiling capabilities and is the officially recommended macOS alternative.

4. **AddressSanitizer (ASan)**: A compiler-based alternative that works on both Linux and macOS:

   ```bash
   clang -fsanitize=address -g ./myprogram.c -o myprogram
   ./myprogram
   ```

5. **Heapusage**: Heapusage is a lightweight tool for finding heap memory errors in Linux and macOS applications. It provides a small subset of Valgrind's memcheck functionality and is useful for large/complex applications that cannot run at Valgrind's slowdown speed.

---

## Summary Table

| Tool | Platform | Use Case |
| --- | --- | --- |
| Valgrind Memcheck | Linux (best) | Memory leaks, illegal access |
| Valgrind Massif | Linux | Heap usage profiling |
| Valgrind Callgrind | Linux | CPU/call graph profiling |
| `leaks` | macOS | Basic memory leak detection |
| Xcode Instruments | macOS | Full memory/CPU profiling |
| AddressSanitizer | Linux & macOS | Fast memory error detection |

---

**References:**

- [Valgrind Quick Start](https://valgrind.org/docs/manual/quick-start.html)
- [Red Hat: Using Valgrind to Profile Memory](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/performance_tuning_guide/s-memory-valgrind)
- [Valgrind macOS Community Fork](https://github.com/LouisBrunner/valgrind-macos)
- [Mac leaks tool guide](https://computerscience.chemeketa.edu/guides/valgrind/leaks/)
- [Heapusage for macOS](https://github.com/d99kris/heapusage)
- [NERSC Valgrind Guide](https://docs.nersc.gov/tools/debug/valgrind/)
