---
audio: false
generated: true
lang: en
layout: post
title: Metal Vector Addition Example
translated: false
type: note
---

If you're using macOS and want to program the GPU using Metal (Apple's low-level graphics and compute API), you can achieve similar functionality to the CUDA example I provided earlier. Metal is designed to give you direct access to the GPU on Apple devices, including Macs, and it supports both graphics and compute operations. Below is a basic Metal example that performs vector addition (similar to the CUDA example) using low-level Metal constructs in C++.

### Metal Vector Addition Example

This example uses Metal to add two arrays on the GPU. It avoids high-level abstractions and sticks to the core Metal API for a low-level approach.

```cpp
#include <iostream>
#include <Metal/Metal.hpp>
#include <Foundation/Foundation.hpp>

int main() {
    // Initialize Metal device
    NS::SharedPtr<MTL::Device> device = NS::TransferPtr(MTL::CreateSystemDefaultDevice());
    if (!device) {
        std::cerr << "Failed to create Metal device" << std::endl;
        return 1;
    }

    // Vector size
    const int n = 1024;
    const size_t bufferSize = n * sizeof(float);

    // Host data
    float* h_a = new float[n];
    float* h_b = new float[n];
    float* h_c = new float[n];

    // Initialize host arrays
    for (int i = 0; i < n; i++) {
        h_a[i] = static_cast<float>(i);
        h_b[i] = static_cast<float>(i * 2);
    }

    // Create Metal buffers
    NS::SharedPtr<MTL::Buffer> d_a = NS::TransferPtr(device->newBuffer(h_a, bufferSize, MTL::ResourceStorageModeShared));
    NS::SharedPtr<MTL::Buffer> d_b = NS::TransferPtr(device->newBuffer(h_b, bufferSize, MTL::ResourceStorageModeShared));
    NS::SharedPtr<MTL::Buffer> d_c = NS::TransferPtr(device->newBuffer(bufferSize, MTL::ResourceStorageModeShared));

    // Create command queue
    NS::SharedPtr<MTL::CommandQueue> queue = NS::TransferPtr(device->newCommandQueue());

    // Load Metal shader source (vector addition kernel)
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

    // Create Metal library and function
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

    // Create compute pipeline state
    NS::SharedPtr<MTL::ComputePipelineState> pipeline = NS::TransferPtr(device->newComputePipelineState(function.get(), &error));
    if (!pipeline) {
        std::cerr << "Failed to create pipeline: " << error->localizedDescription()->utf8String() << std::endl;
        return 1;
    }

    // Create command buffer and encoder
    NS::SharedPtr<MTL::CommandBuffer> commandBuffer = NS::TransferPtr(queue->commandBuffer());
    NS::SharedPtr<MTL::ComputeCommandEncoder> encoder = NS::TransferPtr(commandBuffer->computeCommandEncoder());

    // Set pipeline and buffers
    encoder->setComputePipelineState(pipeline.get());
    encoder->setBuffer(d_a.get(), 0, 0);
    encoder->setBuffer(d_b.get(), 0, 1);
    encoder->setBuffer(d_c.get(), 0, 2);

    // Configure thread groups
    MTL::Size gridSize = MTL::Size(n, 1, 1);
    int threadsPerGroup = pipeline->maxTotalThreadsPerThreadgroup();
    if (threadsPerGroup > n) threadsPerGroup = n;
    MTL::Size threadgroupSize = MTL::Size(threadsPerGroup, 1, 1);

    // Dispatch compute kernel
    encoder->dispatchThreads(gridSize, threadgroupSize);
    encoder->endEncoding();

    // Execute and wait
    commandBuffer->commit();
    commandBuffer->waitUntilCompleted();

    // Get results
    float* results = static_cast<float*>(d_c->contents());
    for (int i = 0; i < 10; i++) {
        std::cout << h_a[i] << " + " << h_b[i] << " = " << results[i] << std::endl;
    }

    // Cleanup
    delete[] h_a;
    delete[] h_b;
    delete[] h_c;

    return 0;
}
```

### Prerequisites
1. **macOS**: This code runs on macOS with a compatible GPU (any modern Mac should work).
2. **Xcode**: Install Xcode to get the Metal framework and command-line tools.
3. **Compile**: Use `clang++` with Metal frameworks:
   ```bash
   clang++ -framework Metal -framework Foundation vector_add.mm -o vector_add
   ```
   Note: Save the file with a `.mm` extension since it uses Objective-C++ (Metal requires Objective-C runtime).

### Key Low-Level Aspects
1. **Manual Resource Management**: Explicitly creating buffers with `newBuffer` and managing memory without high-level wrappers.
2. **Direct Shader Definition**: The Metal Shading Language (MSL) kernel is defined inline as a string, compiled at runtime.
3. **Thread Configuration**: Manually calculating grid and threadgroup sizes, similar to CUDA's blocks and threads.
4. **Command Buffer Control**: Explicitly creating and committing command buffers for GPU execution.
5. **No Abstractions**: Avoids MetalKit or other high-level frameworks, sticking to core Metal APIs.

### Output
Running this will produce something like:
```
0 + 0 = 0
1 + 2 = 3
2 + 4 = 6
3 + 6 = 9
...
```

### Differences from CUDA
- **API Style**: Metal uses an Objective-C++-based API with `NS::` objects, unlike CUDA's C-style API.
- **Memory Model**: Metal's shared storage mode (`MTL::ResourceStorageModeShared`) allows CPU/GPU access to the same memory, simplifying transfers compared to CUDA's explicit `cudaMemcpy`.
- **Thread Model**: Metal uses `dispatchThreads` with grid/threadgroup sizes, conceptually similar to CUDA's grid/block model but with different terminology and configuration.

### Tips for Metal on macOS
- **Debugging**: Use Xcode's Metal debugger to inspect GPU execution.
- **Documentation**: Check Apple's Metal documentation for deeper details (available in Xcode or online at developer.apple.com).
- **Performance**: For larger datasets, optimize threadgroup sizes based on `maxTotalThreadsPerThreadgroup`.

This is a starting point for low-level Metal programming on macOS. You can extend it for more complex compute tasks or graphics rendering as needed!
