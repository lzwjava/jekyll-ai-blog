---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CFFI Python C Interface Guide
translated: false
type: note
---

### What is CFFI?

CFFI (C Foreign Function Interface) is a Python library for calling C functions from Python code. It's compatible with both CPython and PyPy, providing a safer and more portable alternative to libraries like ctypes. It supports two main modes: ABI (calling existing shared libraries) and API (compiling C code inline).

### Installation

Install CFFI using pip:

```bash
pip install cffi
```

CFFI requires a C compiler (e.g., GCC on Linux, Visual Studio on Windows) to build modules.

### Basic Usage Example

Here's a step-by-step guide to a simple use case: calling a C function that adds two integers using API mode (recommended for new code).

1. **Import and Set Up FFI**:

   ```python
   from cffi import FFI
   ffibuilder = FFI()
   ```

2. **Define C Declarations**:
   Specify the C function signatures in a string:

   ```python
   ffibuilder.cdef("""
       int add(int a, int b);
   """)
   ```

3. **Provide C Source Code**:
   Include the C implementation:

   ```python
   ffibuilder.set_source("_example",
       """
       int add(int a, int b) {
           return a + b;
       }
       """)
   ```

4. **Compile the Module**:
   Run this script once to build the C extension:

   ```python
   if __name__ == "__main__":
       ffibuilder.compile(verbose=True)
   ```

   This generates a compiled module (e.g., `_example.cpython-39-x86_64-linux-gnu.so`).

5. **Use the Compiled Module**:
   In your Python code, import and call the function:

   ```python
   from _example import lib
   result = lib.add(5, 3)
   print(result)  # Output: 8
   ```

### Key Concepts

- **FFI Object**: The main interface, created with `FFI()`. Use `cdef()` for declarations and `set_source()` for code.
- **Declarations**: Tell Python about C types, structs, functions, etc. Strings must match C syntax exactly.
- **Type Conversion**: CFFI handles basic types (int, float, pointers) automatically. Use arrays, structs, or callbacks for complexity.
- **Error Handling**: Exceptions like `CDefError` occur for invalid C definitions. C runtime errors (e.g., via `errno`) can be checked with `ffi.errno`.
- **Memory Management**: Use `ffi.new()` for C structs/arrays, and ensure proper deallocation to avoid leaks.

### Modes: ABI vs. API

- **ABI Mode** (for existing libraries): Load a shared library (e.g., `ffi.dlopen("mylib.so")`) and call functions directly. Example:

  ```python
  from cffi import FFI
  ffi = FFI()
  ffi.cdef("int add(int a, int b);")
  lib = ffi.dlopen("/path/to/libmylib.so")
  result = lib.add(5, 3)
  ```

  This is faster for prebuilt libs but less portable—you need the exact binary.

- **API Mode** (recommended): Compile C code inline, as in the example above. It's safer, optimizes better, and works across platforms.

### Advanced Features

- **Structs and Unions**: Define complex types, e.g., `cdef("struct Point { int x, y; }")`.
- **Arrays and Pointers**: Use `ffi.new("int[10]")` for arrays or `ffi.cast("int*", ptr)` for casts.
- **Callbacks**: Pass Python functions to C using `ffi.callback()`.
- **Integration with Packages**: Many libraries (e.g., cryptography, NumPy) use CFFI for performance.
- **Performance Tips**: Compilation takes time; use inplace builds or cffi packages for distribution. Avoid heavy Python-C transitions in loops.

For full documentation, see the [official CFFI docs](https://cffi.readthedocs.io/). This covers the essentials—experiment with the examples to adapt to your needs. If you have a specific use case, provide more details for tailored advice.
