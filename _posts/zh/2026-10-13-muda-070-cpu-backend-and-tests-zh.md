---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda 0.7.0：CPU 后端和测试
translated: true
type: note
---

已推送为 **`muda 0.7.0`**（`8bb848f`）。

## 本轮新增内容

**`driver_cpu`**（`src/driver_cpu.c`）——第二个完全可插拔的后端：

- 在主机内存之上实现了完整的内存/上下文/流/事件接口。
- 内核启动返回 `mudaErrorNotSupported`（显然是一个参考后端）。
- `MUDA_DRIVER=cpu` 选择该后端；如果缺少 OpenCL，`mudaInit` 现在会**自动回退**到它，因此 `muda` 总能完成初始化。

**`examples/reduction.cu`** ——一个真正的 CUDA 块归约（共享内存 + `__syncthreads` + `atomicAdd(float)`），通过 `mudac` 编译并在 `make test` 中运行。它与参考调和级数和（14.4402）一致，并覆盖了 0.6.0 引入的 float 原子操作。

**`tests/test_memory.c`** + `make test-cpu` ——一个与驱动无关的 memory/stream/event 测试套件，可针对两个后端运行。

## 验证

```
make test
  35 passed   core
  18 passed   mudaBLAS
  11 passed   mudart
   5 passed   CUDA source compatibility
   8 passed   memory/stream/event
  mudac vector_add: OK
  reduction: OK (got 14.4402, ref 14.4402)   <- new
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK

make test-cpu
  driver: cpu
  8 passed, 0 failed
```

也就是 **77 项检查 + 4 个 mudac 程序**，全部通过。

## 项目现状

`muda` 现在拥有：一个 CUDA 兼容 API、一个 CUDA runtime 兼容层、一个 `<<<>>>` 预处理器、一个 BLAS、一个 Python 绑定、两个可插拔驱动、扩展的 CUDA intrinsics/atomics，以及六个示例工作负载——全部不依赖 `libcuda` 或 `nvcc`。

## 剩余方向

1. **原生 `nouveau` 试验**——真正的“无 NVIDIA 用户空间”路径。我会在单独分支上做这个，并带一个经过测试的 `unbind`/`rebind` 脚本和明确警告，因为它会暂时将 M40 从你的 ComfyUI/llama 配置中移走。这是剩余最大的事项。
2. **`cudaMemcpyToSymbol` + `__constant__`** ——许多 CUDA 示例都会用到。
3. **性能** ——双缓冲 SGEMM，以推动性能超越当前约 1.4 TFLOP/s，向 M40 约 6.8 TFLOP/s 的峰值迈进。

我该选哪一个？如果你能接受原生路径会碰驱动（并需要通过重启来恢复），我就从那里开始；否则我接下来会做 `__constant__` 支持。
