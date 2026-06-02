---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: CFFI Python C接口指南
translated: true
type: note
---

### 什么是 CFFI？
CFFI（C 外部函数接口）是一个用于从 Python 代码调用 C 函数的 Python 库。它兼容 CPython 和 PyPy，为 ctypes 等库提供了更安全、更便携的替代方案。它支持两种主要模式：ABI（调用现有共享库）和 API（内联编译 C 代码）。

### 安装
使用 pip 安装 CFFI：
```bash
pip install cffi
```
CFFI 需要 C 编译器（例如 Linux 上的 GCC，Windows 上的 Visual Studio）来构建模块。

### 基础用法示例
以下是一个简单用例的逐步指南：使用 API 模式（推荐用于新代码）调用一个将两个整数相加的 C 函数。

1. **导入并设置 FFI**：
   ```python
   from cffi import FFI
   ffibuilder = FFI()
   ```

2. **定义 C 声明**：
   在字符串中指定 C 函数签名：
   ```python
   ffibuilder.cdef("""
       int add(int a, int b);
   """)
   ```

3. **提供 C 源代码**：
   包含 C 实现：
   ```python
   ffibuilder.set_source("_example",
       """
       int add(int a, int b) {
           return a + b;
       }
       """)
   ```

4. **编译模块**：
   运行此脚本一次以构建 C 扩展：
   ```python
   if __name__ == "__main__":
       ffibuilder.compile(verbose=True)
   ```
   这将生成一个编译后的模块（例如 `_example.cpython-39-x86_64-linux-gnu.so`）。

5. **使用编译后的模块**：
   在 Python 代码中，导入并调用函数：
   ```python
   from _example import lib
   result = lib.add(5, 3)
   print(result)  # 输出：8
   ```

### 关键概念
- **FFI 对象**：主接口，使用 `FFI()` 创建。使用 `cdef()` 进行声明，使用 `set_source()` 提供代码。
- **声明**：告诉 Python 关于 C 类型、结构体、函数等信息。字符串必须完全匹配 C 语法。
- **类型转换**：CFFI 自动处理基本类型（int、float、指针等）。对于复杂情况，使用数组、结构体或回调。
- **错误处理**：对于无效的 C 定义，会抛出如 `CDefError` 的异常。可以通过 `ffi.errno` 检查 C 运行时错误（例如通过 `errno`）。
- **内存管理**：使用 `ffi.new()` 创建 C 结构体/数组，并确保正确释放以避免内存泄漏。

### 模式：ABI 与 API
- **ABI 模式**（用于现有库）：加载共享库（例如 `ffi.dlopen("mylib.so")`）并直接调用函数。示例：
  ```python
  from cffi import FFI
  ffi = FFI()
  ffi.cdef("int add(int a, int b);")
  lib = ffi.dlopen("/path/to/libmylib.so")
  result = lib.add(5, 3)
  ```
  这对于预构建的库更快，但可移植性较差——你需要确切的二进制文件。

- **API 模式**（推荐）：内联编译 C 代码，如上例所示。它更安全，优化更好，并且跨平台工作。

### 高级功能
- **结构体和联合**：定义复杂类型，例如 `cdef("struct Point { int x, y; }")`。
- **数组和指针**：使用 `ffi.new("int[10]")` 创建数组，或使用 `ffi.cast("int*", ptr)` 进行类型转换。
- **回调**：使用 `ffi.callback()` 将 Python 函数传递给 C。
- **与包的集成**：许多库（例如 cryptography、NumPy）使用 CFFI 来提高性能。
- **性能提示**：编译需要时间；对于分发，使用原地构建或 cffi 包。避免在循环中进行繁重的 Python-C 转换。

完整文档请参阅 [官方 CFFI 文档](https://cffi.readthedocs.io/)。本文涵盖了基本内容——通过实验这些示例来适应你的需求。如果你有特定的用例，请提供更多细节以获得针对性的建议。
