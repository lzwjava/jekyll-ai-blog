---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: GCC Compiler Options Guide
translated: false
type: note
---

I'll give you a comprehensive introduction to GCC (GNU Compiler Collection) options, organized by category.

## Basic Usage

The basic GCC syntax is:
```bash
gcc [options] file...
```

## Essential Compilation Options

**-c** — Compile source files to object files (.o) without linking
```bash
gcc -c main.c  # produces main.o
```

**-o** — Specify output file name
```bash
gcc main.c -o myprogram
```

**-E** — Preprocess only (output to stdout)
**-S** — Compile to assembly (.s) without assembling
**-save-temps** — Keep intermediate files (preprocessed, assembly, object)

## Optimization Levels

**-O0** — No optimization (default, fastest compilation)
**-O1** or **-O** — Basic optimizations
**-O2** — Moderate optimizations (recommended for production)
**-O3** — Aggressive optimizations (may increase code size)
**-Os** — Optimize for size
**-Ofast** — -O3 plus fast non-standard math optimizations
**-Og** — Optimize for debugging experience

## Warning Options

**-Wall** — Enable common warnings (essential for most projects)
**-Wextra** — Additional warnings beyond -Wall
**-Werror** — Treat warnings as errors
**-pedantic** — Strict ISO C/C++ compliance warnings
**-Wno-unused-variable** — Disable specific warnings
**-w** — Suppress all warnings (not recommended)

Specific useful warnings: **-Wformat**, **-Wuninitialized**, **-Wshadow**, **-Wconversion**

## Debugging Options

**-g** — Include debugging information (for gdb)
**-ggdb** — Produce debugging info specifically for gdb
**-g3** — Maximum debug info (includes macro definitions)
**-p** — Generate profiling information for prof
**-pg** — Generate profiling information for gprof

## Language Standards

**-std=c89** / **-std=c90** — ANSI C / C90
**-std=c99** — C99 standard
**-std=c11** — C11 standard (default for recent GCC)
**-std=c17** / **-std=c18** — C17 standard
**-std=gnu11** — GNU C11 with extensions (often default)

For C++: **-std=c++11**, **-std=c++14**, **-std=c++17**, **-std=c++20**, **-std=c++23**

## Include and Library Options

**-I/path/to/headers** — Add directory to include search path
**-L/path/to/libs** — Add directory to library search path
**-l<library>** — Link with library (e.g., -lm for math library)
**-static** — Link statically instead of dynamically
**-shared** — Create a shared library
**-fPIC** — Generate position-independent code (needed for shared libraries)

Example:
```bash
gcc main.c -I./include -L./lib -lmylib -o program
```

## Preprocessor Options

**-D<macro>=<value>** — Define preprocessor macro
```bash
gcc -DDEBUG=1 -DVERSION=\"1.0\" main.c
```
**-U<macro>** — Undefine preprocessor macro
**-include <file>** — Include file before processing source

## Architecture and Machine Options

**-m32** — Generate 32-bit code
**-m64** — Generate 64-bit code
**-march=native** — Optimize for current CPU architecture
**-mtune=<cpu>** — Tune for specific CPU without restricting instruction set
**-msse**, **-msse2**, **-mavx** — Enable specific CPU instruction sets

## Code Generation Options

**-fno-strict-aliasing** — Disable strict aliasing rules
**-fstack-protector** — Enable stack protection
**-fstack-protector-all** — Protect all functions
**-fomit-frame-pointer** — Don't keep frame pointer in register
**-fpic** / **-fPIC** — Position-independent code (small/large model)
**-pie** — Create position-independent executable

## Linker Options

**-Wl,<options>** — Pass options to the linker
```bash
gcc main.c -Wl,-rpath,/custom/path
```
**-rdynamic** — Export all symbols for dynamic symbol resolution
**-nostdlib** — Don't use standard system libraries
**-nodefaultlibs** — Don't use standard system library defaults

## Analysis and Sanitizers

**-fanalyzer** — Static analysis (GCC 10+)
**-fsanitize=address** — AddressSanitizer (memory errors)
**-fsanitize=thread** — ThreadSanitizer (data races)
**-fsanitize=undefined** — UndefinedBehaviorSanitizer
**-fsanitize=leak** — LeakSanitizer (memory leaks)

## Common Combinations

**Development build:**
```bash
gcc -Wall -Wextra -g -O0 main.c -o program
```

**Production build:**
```bash
gcc -Wall -O2 -DNDEBUG main.c -o program
```

**Maximum warnings and debugging:**
```bash
gcc -Wall -Wextra -Wpedantic -g3 -Og main.c -o program
```

**Optimized with sanitizers:**
```bash
gcc -Wall -O2 -g -fsanitize=address,undefined main.c -o program
```

## Verbose and Diagnostic Options

**-v** — Verbose output (shows compilation steps)
**-Q** — Print function names as they are compiled
**--help** — Display GCC help
**-dumpversion** — Print GCC version
**-print-search-dirs** — Show search paths for libraries

## Dependency Generation

**-M** — Generate dependency rules for make
**-MM** — Like -M but ignore system headers
**-MD** — Generate dependencies and compile
**-MF <file>** — Specify dependency output file

GCC has hundreds of options total. You can explore more with `man gcc` or `gcc --help=<class>` where class can be optimizers, warnings, target, etc.