---
audio: false
generated: true
lang: en
layout: post
title: Rust's Relationship with C
translated: false
type: note
---

No, Rust is not "built on C" in the sense that it compiles to C or requires C as a foundational layer for its own operations. Rust is a separate, modern systems programming language.

Here's a breakdown of the relationship between Rust and C, and how Rust interacts with C libraries:

**Is Rust Built on C?**

* **Compiler:** The Rust compiler (`rustc`) is primarily written in Rust itself. Early versions of the compiler were bootstrapped using OCaml, but it's now self-hosting.
* **Low-level Interaction:** Rust is a low-level language that can interact directly with the operating system and hardware, much like C or C++. It doesn't rely on C as an intermediary for these fundamental operations.
* **LLVM:** Rust's compiler uses LLVM (Low Level Virtual Machine) as its backend for code generation and optimization. LLVM itself is largely written in C++. This means that Rust code eventually gets translated into LLVM Intermediate Representation (IR), which then gets optimized and compiled to machine code. So, in that sense, there's a dependency on a C++-based toolchain (LLVM), but Rust itself isn't "built on C."

**Can Rust Use All C Libraries?**

Yes, Rust has excellent interoperability with C libraries through its **Foreign Function Interface (FFI)**. This means you can call functions and use data structures from existing C libraries directly within your Rust code.

Here's how it generally works:

1. **`extern "C"` blocks:** You define an `extern "C"` block in your Rust code to declare the signatures of the C functions you want to call. This tells the Rust compiler that these functions adhere to the C Application Binary Interface (ABI), which dictates how functions are called and data is laid out in memory.
2. **`#[link]` attribute:** You use the `#[link(name = "foo")]` attribute to tell the Rust linker to link against the specified C library (e.g., `libfoo.so` or `foo.lib`).
3. **`unsafe` blocks:** Calls to C functions are typically wrapped in `unsafe` blocks in Rust. This is because Rust's strong memory safety guarantees cannot be enforced when interacting with "foreign" code that doesn't follow Rust's rules. You, as the programmer, are responsible for ensuring the safety of these calls.
4. **`bindgen`:** For larger C libraries, manually writing all the `extern "C"` declarations can be tedious. Tools like `bindgen` can automatically generate Rust FFI bindings from C header files, greatly simplifying the process.
5. **`cty` crate:** The `cty` crate provides C-compatible primitive types (like `c_int`, `c_char`, etc.) to ensure correct data type mapping between Rust and C.

**Why use C libraries in Rust?**

* **Leverage existing code:** There's a vast ecosystem of well-tested and highly optimized C libraries for various tasks (e.g., system calls, cryptography, numerical computing, graphics). Rust allows you to tap into this existing resource without rewriting everything from scratch.
* **Operating system interfaces:** Operating systems expose many of their functionalities through C-compatible interfaces. Rust needs to be able to call these functions to interact with the OS.
* **Performance-critical sections:** While Rust is generally very fast, some highly specialized performance-critical code might already exist in C and can be directly integrated.

In summary, Rust is not "built on C," but it provides robust mechanisms (FFI) for seamless interoperability with C libraries, allowing Rust developers to leverage the extensive C ecosystem.
