---
audio: false
generated: true
lang: en
layout: post
title: Basic CUDA Example
translated: false
type: note
---

Here's a basic CUDA example that demonstrates low-level GPU programming using CUDA C. This example performs a simple vector addition on the GPU using the most fundamental CUDA constructs:

```c
#include <stdio.h>
#include <cuda.h>

// CUDA kernel for vector addition
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

int main() {
    int n = 1024;  // vector size
    size_t size = n * sizeof(float);

    // Host memory allocation
    float *h_a = (float*)malloc(size);
    float *h_b = (float*)malloc(size);
    float *h_c = (float*)malloc(size);

    // Initialize host arrays
    for(int i = 0; i < n; i++) {
        h_a[i] = i;
        h_b[i] = i * 2;
    }

    // Device memory pointers
    float *d_a, *d_b, *d_c;

    // Allocate device memory
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);

    // Copy data from host to device
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    // Configure kernel launch parameters
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    // Launch kernel
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_a, d_b, d_c, n);

    // Wait for GPU to finish
    cudaDeviceSynchronize();

    // Copy result back to host
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // Verify results
    for(int i = 0; i < 10; i++) {
        printf("%f + %f = %f\n", h_a[i], h_b[i], h_c[i]);
    }

    // Free device memory
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);

    // Free host memory
    free(h_a);
    free(h_b);
    free(h_c);

    // Reset device
    cudaDeviceReset();

    return 0;
}
```

To compile and run this code, you'll need:
1. NVIDIA GPU with CUDA support
2. CUDA Toolkit installed
3. Compile with: `nvcc vector_add.cu -o vector_add`

This example demonstrates the most fundamental CUDA operations:
- `__global__` kernel definition
- Manual memory allocation with `cudaMalloc`
- Explicit memory transfers with `cudaMemcpy`
- Kernel launch configuration with `<<<blocks, threads>>>`
- Device synchronization
- Memory cleanup

Key low-level aspects:
1. Direct memory management without using CUDA runtime helpers
2. Manual thread/block configuration
3. Explicit device synchronization
4. Raw pointer operations
5. No high-level abstractions or libraries

The kernel uses the basic CUDA thread hierarchy:
- `blockIdx.x`: Block index
- `blockDim.x`: Threads per block
- `threadIdx.x`: Thread index within block

This calculates a unique thread ID for each element and performs the addition only if within bounds. The example keeps it simple but shows the core concepts of CUDA programming at a low level.

Output will show the first 10 results, like:
```
0.000000 + 0.000000 = 0.000000
1.000000 + 2.000000 = 3.000000
2.000000 + 4.000000 = 6.000000
...
```
