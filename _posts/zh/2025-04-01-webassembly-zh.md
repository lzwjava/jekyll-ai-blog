---
audio: false
generated: true
lang: zh
layout: post
title: WebAssembly
translated: true
type: note
---

让我们深入了解 WebAssembly (Wasm)。我将把它分解成易于理解的几个部分：它是什么、如何工作、为何重要、如何使用以及未来发展方向。读完本文后，你将扎实掌握 WebAssembly 并了解如何开始使用它。

---

### **1. 什么是 WebAssembly？**
WebAssembly 是一种二进制指令格式，设计为编程语言的可移植高性能编译目标。它是一种类似汇编的低级语言，具有紧凑的二进制表示形式，但并非供人类直接编写——而是通过编译 C、C++、Rust、Go 甚至 Python 等高级语言生成。

- **主要特性：**
  - **高性能：** 通过利用硬件能力，以接近原生速度执行。
  - **可移植性：** 跨平台（浏览器、服务器、物联网设备等）一致运行。
  - **安全性：** 在沙箱环境中运行，与主机系统隔离。
  - **互操作性：** 与 JavaScript 协同工作，而非对立。

- **发展历程：**
  - 2015 年由 Mozilla、Google、Microsoft 和 Apple 合作推出。
  - 2019 年成为 W3C 推荐标准，标志着其成为官方 Web 标准。

- **应用场景：**
  - 网页游戏（例如 Unity 或 Unreal Engine 导出）。
  - 性能关键型应用（例如 Figma 等视频编辑器或类似 Photoshop 的工具）。
  - 服务端应用（例如与 Node.js 配合使用）。
  - 在现代环境中运行遗留代码库。

---

### **2. WebAssembly 如何工作？**
WebAssembly 弥合了高级代码与机器执行之间的差距。流程如下：

1. **源代码：** 使用 C++ 或 Rust 等语言编写代码。
2. **编译：** 编译器（例如用于 C/C++ 的 Emscripten 或用于 Rust 的 `wasm-pack`）将其转换为 WebAssembly 的二进制格式（`.wasm` 文件）。
3. **执行：**
   - 在浏览器中，`.wasm` 文件被获取（通常通过 JavaScript），经过验证并由浏览器的 Wasm 运行时编译为机器码。
   - 运行时在沙箱中执行代码，确保安全。

- **文本格式 (WAT)：** WebAssembly 也有一种人类可读的文本表示形式（`.wat`），适用于调试或学习。例如：
  ```wat
  (module
    (func (export "add") (param i32 i32) (result i32)
      local.get 0
      local.get 1
      i32.add)
  )
  ```
  这定义了一个函数 `add`，它接受两个 32 位整数并返回它们的和。

- **内存模型：** Wasm 使用线性内存模型——一个程序可以读/写的扁平字节数组。它通过手动管理或源语言的运行时进行管理。

- **与 JavaScript 交互：** 使用 `WebAssembly.instantiate()` 或 `fetch()` 在 JavaScript 中加载 Wasm 模块，并调用导出的函数。Wasm 也可以回调到 JavaScript。

---

### **3. 为何使用 WebAssembly？**
- **速度：** 预编译的二进制文件比解释型 JavaScript 运行更快。
- **语言灵活性：** 可以使用 C、Rust 等语言，而不必局限于 JavaScript。
- **体积效率：** `.wasm` 文件比等效的 JavaScript 更小，减少了加载时间。
- **跨平台：** 一次编写，随处运行——浏览器、服务器或嵌入式设备。
- **安全性：** 沙箱机制防止恶意代码访问主机系统。

**权衡之处：**
- 无法直接访问 DOM（需要通过 JavaScript 实现）。
- 对于初学者来说，工具链可能较为复杂。
- 调试比 JavaScript 更棘手。

---

### **4. 开始使用 WebAssembly**
让我们通过一个简单示例来了解：将 C 函数编译为 WebAssembly 并在浏览器中运行。

#### **步骤 1：安装工具**
- **Emscripten：** 用于将 C/C++ 编译为 WebAssembly 的工具链。
  - 安装：遵循 [Emscripten 指南](https://emscripten.org/docs/getting_started/downloads.html)（需要 Python、CMake 等）。
- **Node.js：** 可选，用于在浏览器外运行 Wasm。
- **Web 服务器：** 浏览器要求通过 HTTP 提供 `.wasm` 文件（例如使用 `python -m http.server`）。

#### **步骤 2：编写代码**
创建文件 `add.c`：
```c
int add(int a, int b) {
    return a + b;
}
```

#### **步骤 3：编译为 WebAssembly**
运行以下 Emscripten 命令：
```bash
emcc add.c -s EXPORTED_FUNCTIONS='["_add"]' -s EXPORT_ES6=1 -s MODULARIZE=1 -o add.js
```
- 输出 `add.js`（胶水脚本）和 `add.wasm`（二进制文件）。

#### **步骤 4：在 HTML 中使用**
创建 `index.html`：
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
    <script type="module">
        import init, { add } from './add.js';
        async function run() {
            await init();
            console.log(add(5, 3)); // 输出 8
        }
        run();
    </script>
</body>
</html>
```

#### **步骤 5：提供并测试**
- 启动本地服务器：`python -m http.server 8080`
- 在浏览器中打开 `http://localhost:8080`，并检查控制台。

对于 Rust，可以使用 `cargo` 和 `wasm-pack`——过程类似，工具链不同。

---

### **5. 生态系统与工具**
- **语言支持：**
  - **C/C++：** Emscripten。
  - **Rust：** `wasm-pack`、`wasm-bindgen`。
  - **Go：** 内置 Wasm 支持（`GOOS=js GOARCH=wasm`）。
  - **AssemblyScript：** 类似 TypeScript 语法的 Wasm。

- **运行时：**
  - **浏览器：** Chrome、Firefox、Safari、Edge。
  - **Node.js：** 使用 `--experimental-wasm-modules`。
  - **独立运行时：** Wasmtime、Wasmer、WasmEdge。

- **库：**
  - **WebGL：** 用于图形处理（例如游戏）。
  - **WASI：** 用于非 Web 场景的 WebAssembly 系统接口（文件 I/O 等）。

---

### **6. 高级特性**
- **线程：** 通过 SharedArrayBuffer 支持并行处理。
- **SIMD：** 用于数学密集型任务的向量指令（例如图像处理）。
- **WASI：** 将 Wasm 扩展到 Web 之外，增加系统调用。
- **动态链接：** 加载多个 `.wasm` 模块并在运行时链接它们。

---

### **7. WebAssembly 的未来**
- **更广泛的应用：** 更多语言和框架正在添加 Wasm 支持。
- **无服务器计算：** Wasm 的轻量特性适合边缘计算。
- **标准化：** 垃圾回收和异常处理等提案正在进行中。
- **非 Web 领域的增长：** WASI 和 Wasmer 等运行时正在将 Wasm 推向物联网、桌面应用等更多领域。

---

### **8. 扩展学习资源**
- **官方网站：** [webassembly.org](https://webassembly.org/)
- **MDN 文档：** [MDN 上的 WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly)
- **教程：** 《Rust and WebAssembly》书籍 (rustwasm.github.io/book) 或 Emscripten 文档。
- **X 平台帖子：** 在 X 上搜索 #WebAssembly 获取实际案例和讨论。

---

### **快速回顾**
WebAssembly 在性能和可移植性方面具有革命性意义。你可以用自己喜欢的语言编写代码，编译为 `.wasm`，并在任何地方快速运行。它并非万能药（JavaScript 仍然主导着 Web 的交互性），但它是现代开发者工具包中的强大工具。

想要尝试具体示例、探索使用场景或解决特定问题吗？请告诉我！
