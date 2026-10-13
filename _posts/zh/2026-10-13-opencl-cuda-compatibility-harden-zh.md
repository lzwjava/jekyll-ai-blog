---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenCL CUDA 兼容性加固
translated: true
type: note
---

已推送为 **`muda 0.6.0`**（`aca4fe6`）。

## 本轮新增内容

我选择加固当前技术栈，而不是冒险使用原生驱动（解绑 `nvidia` 会破坏你正在使用的 ComfyUI/llama 环境，而且 Maxwell 计算路径需要数周工作）。

**扩展 CUDA 源码兼容性**（`src/muda_translate.c`）：

- 限定符：`__launch_bounds__(...)`、`__forceinline__`、`__inline__`、`__noinline__`、`__device_builtin__`、`__align__(...)`
- 数学内建函数：`fmaf`、`__expf`、`__exp10f`、`__logf`、`__log2f`、`__log10f`、`__powf`、`__sinf`、`__cosf`、`__tanf`、`__sqrtf`、`rsqrtf`、`__fdividef`、`__saturatef`、`__ldg`
- 原子操作：`atomicAdd`、`atomicExch`、`atomicMax`、`atomicMin`、`atomicCAS`，支持 `int`、`unsigned int`、`unsigned long`，**以及 `float`**（比较-交换循环）

**新增**：`MUDA_CL_OPTIONS` 环境变量，用于传递 `clBuildProgram` 选项；`tests/test_translate.c` 测试套件。

## 有趣的调试弯路

我最初尝试用 `_Generic` 做类型分派，但 NVIDIA OpenCL 编译器**会静默地总是选择 `default`** —— `_Generic(1, int:7, default:0)` 返回了 `0`，在 CL1.2 和 CL3.0 模式下都是如此。我改用 `__builtin_types_compatible_p(__typeof__(*(p)), float)`，它能正确工作，并已端到端验证。

## 在 M40 上验证

```
make test
  35 passed   core runtime
  18 passed   mudaBLAS
  11 passed   mudart
   5 passed   CUDA source compatibility   (new)
  mudac vector_add: OK
  mudac 1D (ints, scalar arg): OK
  mudac 2D (dim3): OK
```

共 **69 项检查 + 3 个 mudac 程序**，全部通过。Python 绑定仍可运行（SGEMM 1024³ ≈ 1.17 TFLOP/s）。

## 下一步方向

可选方案，按可安全完成的程度排序：

1. **`driver_cpu`** —— 一个纯内存的参考后端（启动时返回 `NotSupported`），让 `mudainfo`/API 测试可以在无 GPU 环境下运行。很快。
2. **一个归约示例**，用普通 `.cu` 通过 `mudac`，使用新的 `atomicAdd` —— 很好的展示。
3. **原生 `nouveau` spike** —— 真正的“无 NVIDIA 用户空间”路径，在可抛弃/可重新绑定的环境中进行（未经你明确同意，我不会碰你的活动驱动）。

说一声，我就继续做 1+2，或者在分支上启动原生 spike。
