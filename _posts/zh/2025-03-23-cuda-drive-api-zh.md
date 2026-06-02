---
audio: false
generated: true
lang: zh
layout: post
title: CUDA驱动程序接口
translated: true
type: note
---

`<cuda.h>` 头文件属于 **CUDA 驱动 API**，相较于更高级的 CUDA 运行时 API（例如 `cudaMalloc`、`cudaMemcpy`），这是一个底层 API。驱动 API 提供了对 GPU 资源（如上下文、模块、流）更精细的控制，常用于多 GPU 编程、动态内核加载或底层优化等高级场景。

### 常用 CUDA 驱动 API 函数

以下是一些关键函数及其用途：

| 函数                                | 描述                                                                                   |
|-------------------------------------|---------------------------------------------------------------------------------------|
| **`cuInit(unsigned int flags)`**    | 初始化 CUDA 驱动。必须在调用其他任何驱动 API 函数前执行。                               |
| **`cuDeviceGet(CUdevice *dev, int ordinal)`** | 获取指定序号 GPU 设备的句柄（例如 `0` 表示第一个 GPU）。                               |
| **`cuCtxCreate(CUcontext *ctx, unsigned int flags, CUdevice dev)`** | 在指定设备上创建 CUDA 上下文。                                                        |
| **`cuModuleLoad(CUmodule *mod, const char *fname)`** | 将 PTX 或 cubin 文件作为模块加载到当前上下文中。                                       |
| **`cuModuleGetFunction(CUfunction *func, CUmodule mod, const char *name)`** | 从已加载模块中获取内核函数。                                                           |
| **`cuMemAlloc(CUdeviceptr *dptr, size_t bytesize)`** | 在 GPU 上分配内存。                                                                   |
| **`cuMemcpyHtoD(CUdeviceptr dst, const void *src, size_t bytes)`** | 将数据从主机（CPU）复制到设备（GPU）。                                                 |
| **`cuMemcpyDtoH(void *dst, CUdeviceptr src, size_t bytes)`** | 将数据从设备（GPU）复制到主机（CPU）。                                                 |
| **`cuLaunchKernel(CUfunction f, ...)`** | 使用指定的网格/块维度和参数启动内核函数。                                              |

---

### 工作流程示例

以下是通过 CUDA 驱动 API 实现的简化示例流程：

1. 初始化驱动
2. 分配 GPU 内存
3. 与 GPU 间传输数据
4. 从 PTX 文件加载内核并执行

```cpp
#include <cuda.h>
#include <stdio.h>

int main() {
    CUdevice dev;
    CUcontext ctx;
    CUmodule mod;
    CUfunction kernel;
    CUresult err;

    // 1. 初始化 CUDA 驱动
    cuInit(0);

    // 2. 获取设备 0 的句柄（第一个 GPU）
    cuDeviceGet(&dev, 0);

    // 3. 在设备上创建上下文
    cuCtxCreate(&ctx, 0, dev);

    // 4. 加载 PTX 模块（例如由 .cu 文件编译生成）
    cuModuleLoad(&mod, "my_kernel.ptx");

    // 5. 从模块中获取内核函数
    cuModuleGetFunction(&kernel, mod, "my_kernel");

    // 6. 分配 GPU 内存
    size_t N = 1024;
    CUdeviceptr d_data;
    cuMemAlloc(&d_data, N * sizeof(float));

    // 7. 将数据从主机复制到设备
    float h_data[N] = {1.0f};
    cuMemcpyHtoD(d_data, h_data, N * sizeof(float));

    // 8. 配置内核参数
    void *args[] = { &d_data, &N };
    int blockSize = 256;
    int gridSize = (N + blockSize - 1) / blockSize;

    // 9. 启动内核
    cuLaunchKernel(
        kernel,
        gridSize, 1, 1,    // 网格维度
        blockSize, 1, 1,   // 块维度
        0, NULL,           // 共享内存和流
        args, NULL         // 内核参数
    );

    // 10. 将结果复制回主机
    cuMemcpyDtoH(h_data, d_data, N * sizeof(float));

    // 11. 清理资源
    cuMemFree(d_data);
    cuModuleUnload(mod);
    cuCtxDestroy(ctx);

    return 0;
}
```

---

### 重要说明

1. **错误处理**：始终检查返回值（例如 `CUresult err = cuSomeFunction(...);`），可通过 `cuGetErrorString(err)` 解析错误信息
2. **内核参数**：向 `cuLaunchKernel` 传递参数时需使用参数指针数组，确保顺序与内核预期参数顺序一致
3. **PTX 文件**：内核必须编译为 PTX 格式（例如 `nvcc --ptx my_kernel.cu -o my_kernel.ptx`）
4. **上下文管理**：上下文类似于 CPU 进程——负责管理 GPU 资源。多线程代码中可使用 `cuCtxPushCurrent`/`cuCtxPopCurrent`

---

### 何时使用驱动 API？

- **动态内核加载**：运行时加载 PTX 模块
- **多 GPU 控制**：显式管理多个 GPU 设备
- **底层优化**：对上下文、流或内存进行细粒度控制

对于大多数应用场景，更高级的**运行时 API**（例如 `cudaMalloc`、`cudaMemcpy`）已足够且更简单。当需要驱动 API 的高级功能时再选择使用。
