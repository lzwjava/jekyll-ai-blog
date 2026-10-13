---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda 0.4.0：CUDA 运行时填充层
translated: true
type: note
---

里程碑 2 已完成并推送为 **`muda 0.4.0`**（`cf2e73a`）。

## 新增内容

**`mudart` — CUDA runtime API 适配层**（`include/mudart.h`、`src/mudart.c`）

将 CUDA **runtime** 名称映射到 muda：
- 内存：`cudaMalloc/Free`、`cudaMallocHost`、`cudaHostAlloc`、`cudaFreeHost`、`cudaMemcpy/Async/2D`、`cudaMemset`、`cudaMemGetInfo`
- 设备：`cudaGetDeviceCount/Get/Set`、`cudaGetDeviceProperties`（真实的 CUDA 结构 `cudaDeviceProp`）、`cudaDeviceSynchronize/Reset`
- 流/事件：`cudaStream*`、`cudaEvent*`
- 错误：`cudaGetLastError/PeekAtLastError/GetErrorName/GetErrorString`，并带有 `cudaError*` 常量别名
- 启动桥接：`dim3`、`cudaLaunchKernel((const void*)fn, grid, block, args, shared, stream)`，以及旧的 `cudaConfigureCall` / `cudaSetupArgument` / `cudaLaunch` 序列

**Python 绑定**（`python/muda.py`）—— 纯 `ctypes`，无需构建步骤：
- `muda.init()`、`device_info()`、`Module`、`Function`、`DeviceBuffer`（与 numpy 互操作）、`Stream`、`Event`
- `muda.matmul` / `gemm` / `gemm_buffers` / `gemv` / `saxpy`，由 mudaBLAS 提供支持
- 演示：`python/demo_kernel.py`（加载并启动内核）、`python/demo_matmul.py`（基准测试）

## 已在 M40 上验证

```
make test
  35 passed, 0 failed     # core runtime
  18 passed, 0 failed     # mudaBLAS
  11 passed, 0 failed     # mudart  (new)

make python PYTHON=.venv/bin/python
  vector_add: OK
  256^3    0.065 ms    518.8 GFLOP/s
  512^3    0.244 ms   1101.1 GFLOP/s
  1024^3   1.831 ms   1173.0 GFLOP/s
  2048^3   13.477 ms  1274.8 GFLOP/s
```

我创建了一个本地 `.venv`（已 gitignore）来为演示获取 numpy；`uv venv .venv && uv pip install --python .venv/bin/python numpy` 在你的机器上可用。

## 建议的下一步（里程碑 3）

实现“直接替换”剩下的差距是 `<<<...>>>` 启动语法，这需要一个前端。我会实现一个小的 **`mudac` 预处理器**，将以下内容重写：
```c
kernel<<<grid, block, shared, stream>>>(a, b, c, n);
```
为
```c
{ void* _a[] = {&a,&b,&c,&n}; cudaLaunchKernel((void*)kernel, grid, block, _a, shared, stream); }
```
这样普通的 `.cu` 文件可以通过 `mudac prog.cu | cc -x c - -lmuda` 不加修改地编译。你想让我先实现这个，还是继续推进原生的 `nouveau` 后端？