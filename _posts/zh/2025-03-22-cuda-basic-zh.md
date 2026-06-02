---
audio: false
generated: true
lang: zh
layout: post
title: 基础CUDA示例
translated: true
type: note
---

以下是一个基础的 CUDA 示例，展示了使用 CUDA C 进行底层 GPU 编程的方法。该示例使用最基础的 CUDA 结构在 GPU 上执行简单的向量加法：

```c
#include <stdio.h>
#include <cuda.h>

// 向量加法的 CUDA 核函数
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    int n = 1024;  // 向量大小
    size_t size = n * sizeof(float);

    // 主机内存分配
    float *h_a = (float*)malloc(size);
    float *h_b = (float*)malloc(size);
    float *h_c = (float*)malloc(size);

    // 初始化主机数组
    for(int i = 0; i < n; i++) {
        h_a[i] = i;
        h_b[i] = i * 2;
    }

    // 设备内存指针
    float *d_a, *d_b, *d_c;

    // 分配设备内存
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);

    // 将数据从主机复制到设备
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    // 配置内核启动参数
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    // 启动核函数
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);

    // 等待 GPU 完成计算
    cudaDeviceSynchronize();

    // 将结果复制回主机
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // 验证结果
    for(int i = 0; i < 10; i++) {
        printf("%f + %f = %f\n", h_a[i], h_b[i], h_c[i]);
    }

    // 释放设备内存
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    // 释放主机内存
    free(h_a);
    free(h_b);
    free(h_c);

    // 重置设备
    cudaDeviceReset();

    return 0;
}
```

要编译和运行此代码，您需要：

1. 支持 CUDA 的 NVIDIA GPU
2. 已安装 CUDA Toolkit
3. 使用命令编译：`nvcc vector_add.cu -o vector_add`

此示例展示了最基本的 CUDA 操作：

- `__global__` 核函数定义
- 使用 `cudaMalloc` 手动分配内存
- 使用 `cudaMemcpy` 进行显式内存传输
- 使用 `<<<blocks, threads>>>` 配置内核启动参数
- 设备同步
- 内存清理

关键的底层特性：

1. 不使用 CUDA 运行时辅助函数直接管理内存
2. 手动配置线程/块
3. 显式设备同步
4. 原始指针操作
5. 无高级抽象或库

核函数使用基础的 CUDA 线程层次结构：

- `blockIdx.x`：块索引
- `blockDim.x`：每个块的线程数
- `threadIdx.x`：块内的线程索引

这为每个元素计算唯一的线程 ID，并在边界内执行加法操作。该示例保持简洁，但展示了 CUDA 编程在底层级的核心概念。

输出将显示前 10 个结果，例如：

```
0.000000 + 0.000000 = 0.000000
1.000000 + 2.000000 = 3.000000
2.000000 + 4.000000 = 6.000000
...
```
