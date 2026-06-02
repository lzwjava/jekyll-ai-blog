---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: MinGW-w64 Included Executables
translated: false
type: note
---

### Executables Included in MinGW-w64

MinGW-w64 is primarily a minimal toolchain for cross-compiling native Windows applications using GCC and related tools. It focuses on development utilities rather than a full suite of Unix-like commands (e.g., it does **not** include `gpg` or GnuPG by default—those are available as separate packages in environments like MSYS2). The core installation's `bin` directory typically contains the following executables (based on a standard standalone download, such as from the official SourceForge releases). This list can vary slightly by version and build, but these are the common ones:

| Executable | Description |
|------------|-------------|
| `gcc.exe` | GNU C compiler |
| `g++.exe` | GNU C++ compiler |
| `cpp.exe` | C preprocessor |
| `gfortran.exe` | GNU Fortran compiler (if included in the build) |
| `ld.exe` | GNU linker |
| `as.exe` | GNU assembler |
| `ar.exe` | Archiver for creating libraries |
| `ranlib.exe` | Generates index for archive libraries |
| `nm.exe` | Lists symbols from object files |
| `objdump.exe` | Displays information from object files |
| `objcopy.exe` | Copies and translates object files |
| `strip.exe` | Strips symbols from executables |
| `size.exe` | Lists section sizes of object files |
| `strings.exe` | Prints printable strings in files |
| `readelf.exe` | Displays ELF file information (for cross-tools) |
| `dlltool.exe` | Creates DLL import/export files |
| `windres.exe` | Compiles Windows resource files |
| `gendef.exe` | Generates .def files from DLLs |
| `genidl.exe` | Generates .idl files from DLLs |
| `widl.exe` | Compiles IDL files for Wine/Winelib |
| `gcc-ar.exe` | GCC wrapper for ar |
| `gcc-nm.exe` | GCC wrapper for nm |
| `gcc-ranlib.exe` | GCC wrapper for ranlib |

These are mostly compiler, linker, and binary manipulation tools from GCC and Binutils. For a fuller Unix-like environment with tools like `gpg`, `make`, `bash`, etc., consider installing MSYS2 (which includes MinGW-w64 as a component) and adding packages via `pacman`.

[MinGW-w64 Official Site](https://www.mingw-w64.org/)
[MSYS2 Packages (for extensions like GnuPG)](https://packages.msys2.org/package/mingw-w64-x86_64-gnupg)
[SourceForge MinGW-w64 Downloads](https://sourceforge.net/projects/mingw-w64/files/)
