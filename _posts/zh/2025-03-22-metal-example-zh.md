---
audio: false
generated: true
lang: zh
layout: post
title: 金属向量加法示例
translated: true
type: note
---

若您在 macOS 环境下希望通过 Metal（苹果的低层级图形与计算 API）进行 GPU 编程，可以实现与我之前提供的 CUDA 示例类似的功能。Metal 专为直接访问 Apple 设备（包括 Mac）的 GPU 而设计，同时支持图形和计算操作。以下是一个基础的 Metal 示例，使用 C++ 中的底层 Metal 构造执行向量加法（类似于 CUDA 示例）。

### Metal 向量加法示例

本示例使用 Metal 在 GPU 上对两个数组进行加法运算。它避免使用高层抽象，坚持使用核心 Metal API 以实现底层操作。

```cpp
#include <iostream>
#include <Metal/Metal.hpp>
#include <Foundation/Foundation.hpp>

int main() {
    // 初始化 Metal 设备
    NS::SharedPtr<MTL::Device> device = NS::TransferPtr(MTL::CreateSystemDefaultDevice());
    if (!device) {
        std::cerr << "Failed to create Metal device" << std::endl;
        return 1;
    }

    // 向量大小
    const int n = 1024;
    const size_t bufferSize = n * sizeof(float);

    // 主机数据
    float* h_a = new float[n];
    float* h_b = new float[n];
    float* h_c = new float[n];

    // 初始化主机数组
    for (int i = 0; i < n; i++) {
        h_a[i] = static_cast<float>(i);
        h_b[i] = static_cast<float>(i * 2);
    }

    // 创建 Metal 缓冲区
    NS::SharedPtr<MTL::Buffer> d_a = NS::TransferPtr(device->newBuffer(h_a, bufferSize, MTL::ResourceStorageModeShared));
    NS::SharedPtr<MTL::Buffer> d_b = NS::TransferPtr(device->newBuffer(h_b, bufferSize, MTL::ResourceStorageModeShared));
    NS::SharedPtr<MTL::Buffer> d_c = NS::TransferPtr(device->newBuffer(bufferSize, MTL::ResourceStorageModeShared));

    // 创建命令队列
    NS::SharedPtr<MTL::CommandQueue> queue = NS::TransferPtr(device->newCommandQueue());

    // 加载 Metal 着色器源码（向量加法内核）
    const char* kernelSource = R"(
        #include <metal_stdlib>
        using namespace metal;

        kernel void vectorAdd(device const float* a,
                             device const float* b,
                             device float* c,
                             uint id [[thread_position_in_grid]]) {
            c[id] = a[id] + b[id];
        }
    )";

    // 创建 Metal 库和函数
    NS::Error* error = nullptr;
    NS::SharedPtr<NS::String> source = NS::TransferPtr(NS::String::string(kernelSource, NS::UTF8StringEncoding));
    NS::SharedPtr<MTL::Library> library = NS::TransferPtr(device->newLibrary(source.get(), nullptr, &error));
    if (!library) {
        std::cerr << "Failed to create library: " << error->localizedDescription()->utf8String() << std::endl;
        return 1;
    }

    NS::SharedPtr<MTL::Function> function = NS::TransferPtr(library->newFunction(NS::String::string("vectorAdd", NS::UTF8StringEncoding)));
    if (!function) {
        std::cerr << "Failed to create function" << std::endl;
        return 1;
    }

    // 创建计算管线状态
    NS::SharedPtr<MTL::ComputePipelineState> pipeline = NS::TransferPtr(device->newComputePipelineState(function.get(), &error));
    if (!pipeline) {
        std::cerr << "Failed to create pipeline: " << error->localizedDescription()->utf8String() << std::endl;
        return 1;
    }

    // 创建命令缓冲区和编码器
    NS::SharedPtr<MTL::CommandBuffer> commandBuffer = NS::TransferPtr(queue->commandBuffer());
    NS::SharedPtr<MTL::ComputeCommandEncoder> encoder = NS::TransferPtr(commandBuffer->computeCommandEncoder());

    // 设置管线和缓冲区
    encoder->setComputePipelineState(pipeline.get());
    encoder->setBuffer(d_a.get(), 0, 0);
    encoder->setBuffer(d_b.get(), 0, 1);
    encoder->setBuffer(d_c.get(), 0, 2);

    // 配置线程组
    MTL::Size gridSize = MTL::Size(n, 1, 1);
    int threadsPerGroup = pipeline->maxTotalThreadsPerThreadgroup();
    if (threadsPerGroup > n) threadsPerGroup = n;
    MTL::Size threadgroupSize = MTL::Size(threadsPerGroup, 1, 1);

    // 分发计算内核
    encoder->dispatchThreads(gridSize, threadgroupSize);
    encoder->endEncoding();

    // 执行并等待
    commandBuffer->commit();
    commandBuffer->waitUntilCompleted();

    // 获取结果
    float* results = static_cast<float*>(d_c->contents());
    for (int i = 0; i < 10; i++) {
        std::cout << h_a[i] << " + " << h_b[i] << " = " << results[i] << std::endl;
    }

    // 清理
    delete[] h_a;
    delete[] h_b;
    delete[] h_c;

    return 0;
}
```

### 前置条件

1. **macOS**：此代码需在配备兼容 GPU（任何现代 Mac 均可）的 macOS 上运行。
2. **Xcode**：安装 Xcode 以获取 Metal 框架和命令行工具。
3. **编译**：使用 `clang++` 并链接 Metal 框架：

   ```bash
   clang++ -framework Metal -framework Foundation vector_add.mm -o vector_add
   ```

   注意：由于使用了 Objective-C++（Metal 需要 Objective-C 运行时），请将文件保存为 `.mm` 扩展名。

### 关键底层特性

1. **手动资源管理**：显式创建缓冲区（`newBuffer`）并在无高层封装的情况下管理内存。
2. **直接着色器定义**：Metal 着色语言（MSL）内核以内联字符串形式定义，并在运行时编译。
3. **线程配置**：手动计算网格和线程组大小，类似于 CUDA 的块和线程概念。
4. **命令缓冲区控制**：显式创建并提交命令缓冲区以执行 GPU 操作。
5. **无抽象层**：避免使用 MetalKit 或其他高层框架，仅使用核心 Metal API。

### 输出

运行后将产生类似以下结果：

```
0 + 0 = 0
1 + 2 = 3
2 + 4 = 6
3 + 6 = 9
...
```

### 与 CUDA 的差异

- **API 风格**：Metal 使用基于 Objective-C++ 的 API（`NS::` 对象），而 CUDA 采用 C 风格 API。
- **内存模型**：Metal 的共享存储模式（`MTL::ResourceStorageModeShared`）允许 CPU/GPU 访问同一内存，相比 CUDA 的显式 `cudaMemcpy` 更为简化。
- **线程模型**：Metal 使用 `dispatchThreads` 及网格/线程组大小配置，概念上类似 CUDA 的网格/块模型，但术语和配置方式不同。

### macOS 上使用 Metal 的提示

- **调试**：使用 Xcode 的 Metal 调试器检查 GPU 执行情况。
- **文档**：查阅 Apple 的 Metal 文档以获取更深入细节（可通过 Xcode 或 developer.apple.com 在线获取）。
- **性能**：对于较大数据集，可根据 `maxTotalThreadsPerThreadgroup` 优化线程组大小。

这是一个在 macOS 上进行底层 Metal 编程的起点。您可以根据需要扩展它以处理更复杂的计算任务或图形渲染！
