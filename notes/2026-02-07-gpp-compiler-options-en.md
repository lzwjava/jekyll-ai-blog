---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: G++ Compiler Options Guide
translated: false
type: note
---

G++ is the GNU C++ compiler, part of the GCC (GNU Compiler Collection) suite. It transforms C++ source code into executable programs through compilation and linking. Understanding its options is essential for effective C++ development.

## Basic Usage

The simplest g++ invocation compiles and links a program in one step:

```bash
g++ program.cpp -o program
```

This creates an executable named `program` from `program.cpp`.

## Essential Options

**Output Control**
- `-o <filename>` — Specify output file name (without this, defaults to `a.out`)
- `-c` — Compile to object file only, don't link (produces `.o` files)
- `-S` — Generate assembly code only (`.s` files)
- `-E` — Preprocess only, output to stdout

**Language Standards**
- `-std=c++11`, `-std=c++14`, `-std=c++17`, `-std=c++20`, `-std=c++23` — Select C++ standard version
- `-std=gnu++17` — Use GNU extensions with C++17

**Warning Options**
- `-Wall` — Enable most common warnings (doesn't actually mean "all")
- `-Wextra` — Additional warnings beyond `-Wall`
- `-Wpedantic` — Strict ISO C++ warnings
- `-Werror` — Treat warnings as errors
- `-Wconversion` — Warn about implicit conversions that may alter values
- `-Wshadow` — Warn when variables shadow others

**Optimization Levels**
- `-O0` — No optimization (default, fastest compilation)
- `-O1` or `-O` — Basic optimization
- `-O2` — Recommended optimization for release builds
- `-O3` — Aggressive optimization, may increase binary size
- `-Os` — Optimize for size
- `-Ofast` — `-O3` plus non-standards-compliant optimizations
- `-Og` — Optimize but maintain debuggability

**Debugging**
- `-g` — Include debugging information (for gdb, lldb)
- `-g3` — Maximum debugging info including macro definitions
- `-ggdb` — Debugging info specifically for GDB

## Include Paths and Libraries

**Headers**
- `-I<directory>` — Add directory to include search path
- `-isystem <directory>` — Add system header directory (suppresses warnings from these headers)

**Libraries**
- `-L<directory>` — Add directory to library search path
- `-l<library>` — Link against library (e.g., `-lm` for math library)
- `-static` — Link libraries statically instead of dynamically
- `-shared` — Create a shared library

**Example:**
```bash
g++ app.cpp -I./include -L./lib -lmylib -o app
```

## Preprocessor Options

- `-D<macro>` — Define preprocessor macro (e.g., `-DDEBUG`)
- `-D<macro>=<value>` — Define macro with value
- `-U<macro>` — Undefine macro
- `-include <file>` — Include file before processing source

## Code Generation

- `-fPIC` — Generate position-independent code (required for shared libraries)
- `-march=<arch>` — Generate code for specific architecture (e.g., `-march=native`)
- `-mtune=<cpu>` — Optimize for specific CPU without limiting compatibility
- `-m32` / `-m64` — Generate 32-bit or 64-bit code
- `-pthread` — Enable POSIX thread support

## Analysis and Safety

- `-fsanitize=address` — Enable AddressSanitizer (detects memory errors)
- `-fsanitize=undefined` — Enable UndefinedBehaviorSanitizer
- `-fsanitize=thread` — Enable ThreadSanitizer (race condition detection)
- `-fstack-protector-strong` — Stack buffer overflow protection
- `-D_FORTIFY_SOURCE=2` — Runtime buffer overflow protection

## Practical Compilation Patterns

**Debug Build:**
```bash
g++ -std=c++17 -Wall -Wextra -g -Og program.cpp -o program_debug
```

**Release Build:**
```bash
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG program.cpp -o program
```

**Multiple Files:**
```bash
# Compile separately
g++ -c -std=c++17 -Wall file1.cpp -o file1.o
g++ -c -std=c++17 -Wall file2.cpp -o file2.o

# Link together
g++ file1.o file2.o -o program
```

**With Sanitizers (during development):**
```bash
g++ -std=c++17 -g -fsanitize=address,undefined program.cpp -o program
```

## Advanced Options

- `-v` — Verbose output showing all compilation steps
- `-save-temps` — Keep intermediate files (preprocessed, assembly)
- `-pipe` — Use pipes instead of temporary files (faster compilation)
- `-fno-exceptions` — Disable C++ exception handling
- `-fno-rtti` — Disable runtime type information
- `-flto` — Enable link-time optimization

## Getting Help

- `g++ --help` — Show brief help
- `g++ --help=warnings` — Show warning options
- `man g++` — Full manual page

The most common combination for everyday development is something like `-std=c++17 -Wall -Wextra -O2` for release builds and `-std=c++17 -Wall -Wextra -g -Og` for debug builds.