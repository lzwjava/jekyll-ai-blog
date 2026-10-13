---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Muda: 使用OpenCL的CUDA运行时'
translated: true
type: note
---

完成了。我在 `/home/lzw/projects/muda` 中构建了 **`muda`**，它能在你的 Tesla M40 上运行真实的 kernel。

## 结果

```
$ make && ./build/test_muda
driver: opencl
== device ==
  device 0: Tesla M40 sm_52, 11436 MiB, 24 SMs
== memory ==
== vector_add ==
== saxpy ==
== shared_memory_+_syncthreads ==
== 2d_grid ==
== streams_and_events ==
13 passed, 0 failed

$ ./build/vector_add
vector_add of 1048576 elements: OK (0.206 ms, 61.2 GB/s)
```

## 它是什么

一个兼容 CUDA 的 runtime + 它自己的 driver 层，**从不链接或加载 `libcuda`**：

- `include/muda.h` — 类似 CUDA 的 API（`mudaMalloc`、`mudaMemcpy`、`mudaModuleLoadData`、`mudaLaunchKernel`、streams、events）。
- `src/muda_internal.h` — 一个真正的 `muda_driver` vtable，因此 backends 是可插拔的。
- `src/driver_opencl.c` — 默认的“muda driver”：通过 `dlopen` 加载 `libOpenCL.so.1`，并通过 OpenCL ICD 进行分发。
- `src/muda_translate.c` — 将 CUDA C 重写为 OpenCL C（我已验证输出）。处理 `__global__`、`__shared__`、`threadIdx/blockIdx/blockDim/gridDim`、`__syncthreads()`，并在指针参数上自动插入 `__global` 地址空间限定符，因此正常的 CUDA 签名可以原样工作。
- 构建时不需要 CUDA toolkit、`nvcc` 或 OpenCL 开发 headers。

## 唯一坦诚的提醒

你的原话是“不要用 CUDA driver，用 muda driver。”我完全避免使用 `libcuda`，但最底层仍然是 NVIDIA 的 **OpenCL** userspace ICD，因为从零开始实现 Maxwell driver 需要重新实现 PMU/FECS 固件引导。我记录了这一情况，并为 vtable 提供了一条通往真正的 `nouveau`/MMIO backend 的清晰路径。

## 我可以采取的后续步骤

- 添加一个 `driver_nouveau` backend，直接与开源的 `nouveau` kernel driver 通信（解绑 `nvidia`，使用 `/dev/dri` pushbuffers）——这是真正的“无 NVIDIA userspace”路径。
- 添加一个 `driver_cpu` 参考实现，以便在没有 GPU 的情况下运行测试。
- 将 commit 推送到 `git@github.com:lzwjava/muda.git`。

已在本地提交为 `62c8806`。需要我推送吗？