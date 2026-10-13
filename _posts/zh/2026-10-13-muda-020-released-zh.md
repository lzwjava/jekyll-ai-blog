---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Muda 0.2.0 发布
translated: true
type: note
---

已推送为 **`muda 0.2.0`**（`67ae082`）。以下是新增内容。

## 新增 API 接口

**运行时 / 设备**
- `mudaSetDevice`, `mudaGetDevice`, `mudaDeviceGetName`, `mudaDeviceGetAttribute`（23 个属性）、`mudaDeviceGetPCIBusId`、`mudaDeviceReset`
- `mudaRuntimeGetVersion`, `mudaDriverGetVersion`, `mudaCtxGetDevice`

**内存**
- `mudaMallocHost`, `mudaFreeHost`, `mudaHostGetDevicePointer`
- `mudaMemGetInfo`, `mudaPointerGetAttributes` + 一个完整的分配注册表，用于跟踪每次设备/主机分配
- `mudaMemcpy2D` / `mudaMemcpy2DAsync`, `mudaMemsetD8`, `mudaMemsetD32`
- `mudaMemAdvise`, `mudaMemPrefetchAsync`（文档注明为无操作）

**模块 / 启动**
- `mudaFuncGetAttributes`（工作组大小、局部/私有内存）
- `mudaLaunchKernelEx` + 支持完整打包的 `extra[]` 参数（`MUDA_LAUNCH_PARAM_BUFFER_POINTER/SIZE`）
- `mudaOccupancyMaxActiveBlocksPerMultiprocessor`

**流 / 事件**
- `mudaStreamCreateWithFlags`, `mudaStreamQuery`, `mudaStreamWaitEvent`
- `mudaEventCreateWithFlags`, `mudaEventQuery`
- 流现在是包装对象，跟踪其最后一个 `cl_event`，因此非阻塞 `Query` 实际上可以工作

## 驱动内部
- 扩展了 `muda_driver` vtable，新增约 15 个操作
- 流包装 + 按流跟踪事件以支持查询/等待
- 打包参数解包，采用自然对齐
- `MUDA_VERBOSE=1` 会转储 OpenCL 构建日志（我用它发现并修复了 4 个编译器警告——删除了 preamble 中冗余的 typedef）

## 示例与测试

| 示例 | M40 上的结果 |
| --- | --- |
| `vector_add`（1M 浮点数） | ~0.18 ms, ~70 GB/s |
| `saxpy`（4M 浮点数，流） | ~0.24 ms, ~210 GB/s |
| `matmul` 256×256 分块 | ~0.09 ms, ~395 GFLOP/s |

测试套件规模从 **13 → 35 项**增长，全部通过，覆盖了 2D 拷贝、打包启动、指针自省、设备属性、函数属性/占用率，以及流/事件查询。README 已针对 0.2.0 更新。

仓库现在与 `origin/main` 保持干净同步。接下来要我处理 `driver_nouveau` 后端吗（真正的“无 NVIDIA 用户空间”路径）？