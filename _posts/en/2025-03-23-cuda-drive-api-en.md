---
audio: false
generated: true
lang: en
layout: post
title: CUDA Driver API
translated: false
type: note
---

The `<cuda.h>` header is part of the **CUDA Driver API**, a lower-level API compared to the higher-level CUDA Runtime API (e.g., `cudaMalloc`, `cudaMemcpy`). The Driver API provides finer control over GPU resources (e.g., contexts, modules, streams) and is often used in advanced scenarios like multi-GPU programming, dynamic kernel loading, or low-level optimizations.

### Common CUDA Driver API Functions

Here are some key functions and their purposes:

| Function | Description |
| ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| **`cuInit(unsigned int flags)`** | Initializes the CUDA driver. Must be called before any other Driver API function. |
| **`cuDeviceGet(CUdevice *dev, int ordinal)`** | Gets a handle to the GPU device with the specified ordinal (e.g., `0` for the first GPU). |
| **`cuCtxCreate(CUcontext *ctx, unsigned int flags, CUdevice dev)`** | Creates a CUDA context on the specified device. |
| **`cuModuleLoad(CUmodule *mod, const char *fname)`** | Loads a PTX or cubin file into the current context as a module. |
| **`cuModuleGetFunction(CUfunction *func, CUmodule mod, const char *name)`** | Retrieves a kernel function from a loaded module. |
| **`cuMemAlloc(CUdeviceptr *dptr, size_t bytesize)`** | Allocates memory on the GPU. |
| **`cuMemcpyHtoD(CUdeviceptr dst, const void *src, size_t bytes)`** | Copies data from host (CPU) to device (GPU). |
| **`cuMemcpyDtoH(void *dst, CUdeviceptr src, size_t bytes)`** | Copies data from device (GPU) to host (CPU). |
| **`cuLaunchKernel(CUfunction f, ...)`** | Launches a kernel function with specified grid/block dimensions and parameters. |

---

### Example Workflow

Below is a simplified example using the CUDA Driver API to:

1. Initialize the driver.
2. Allocate GPU memory.
3. Copy data to/from the GPU.
4. Load a kernel from a PTX file and execute it.

```cpp
#include <cuda.h>
#include <stdio.h>

int main() {
    CUdevice dev;
    CUcontext ctx;
    CUmodule mod;
    CUfunction kernel;
    CUresult err;

    // 1. Initialize the CUDA driver
    cuInit(0);

    // 2. Get handle to device 0 (first GPU)
    cuDeviceGet(&dev, 0);

    // 3. Create a context on the device
    cuCtxCreate(&ctx, 0, dev);

    // 4. Load a PTX module (e.g., generated from a .cu file)
    cuModuleLoad(&mod, "my_kernel.ptx");

    // 5. Get the kernel function from the module
    cuModuleGetFunction(&kernel, mod, "my_kernel");

    // 6. Allocate GPU memory
    size_t N = 1024;
    CUdeviceptr d_data;
    cuMemAlloc(&d_data, N * sizeof(float));

    // 7. Copy data from host to device
    float h_data[N] = {1.0f};
    cuMemcpyHtoD(d_data, h_data, N * sizeof(float));

    // 8. Configure kernel parameters
    void *args[] = { &d_data, &N };
    int blockSize = 256;
    int gridSize = (N + blockSize - 1) / blockSize;

    // 9. Launch the kernel
    cuLaunchKernel(
        kernel,
        gridSize, 1, 1,    // Grid dimensions
        blockSize, 1, 1,   // Block dimensions
        0, NULL,           // Shared memory and stream
        args, NULL         // Kernel arguments
    );

    // 10. Copy results back to host
    cuMemcpyDtoH(h_data, d_data, N * sizeof(float));

    // 11. Cleanup
    cuMemFree(d_data);
    cuModuleUnload(mod);
    cuCtxDestroy(ctx);

    return 0;
}
```

---

### Key Notes

1. **Error Handling**: Always check the return value (e.g., `CUresult err = cuSomeFunction(...);`). Use `cuGetErrorString(err)` to decode errors.
2. **Kernel Parameters**: For `cuLaunchKernel`, parameters are passed as an array of pointers to arguments. Ensure the order matches the kernel's expected parameters.
3. **PTX Files**: Kernels must be compiled to PTX (e.g., `nvcc --ptx my_kernel.cu -o my_kernel.ptx`).
4. **Context Management**: Contexts are analogous to CPU processes—they manage resources for a GPU. Use `cuCtxPushCurrent`/`cuCtxPopCurrent` for multi-threaded code.

---

### When to Use the Driver API?

- **Dynamic Kernel Loading**: Loading PTX at runtime.
- **Multi-GPU Control**: Explicitly managing multiple GPUs.
- **Low-Level Optimizations**: Fine-grained control over contexts, streams, or memory.

For most applications, the higher-level **Runtime API** (e.g., `cudaMalloc`, `cudaMemcpy`) is sufficient and simpler. Use the Driver API when you need its advanced features.
