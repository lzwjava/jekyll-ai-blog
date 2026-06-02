---
audio: false
generated: true
lang: zh
layout: post
title: 解决Thrust CUDA内存分配错误
translated: true
type: note
---

错误 `thrust::system::detail::bad_alloc` 伴随 `cudaErrorUnknown: unknown error` 及随后的 `Aborted (core dumped)` 表明您的 CUDA 程序在运行时出现问题，很可能与使用 Thrust 进行排序时的内存分配或 GPU 兼容性有关。该错误通常出现在 CUDA 运行时遇到问题时，例如 GPU 内存不足、GPU 不兼容或 CUDA 环境配置错误。下面，我将根据提供的代码和错误信息，列出诊断和修复问题的步骤。

### 修复步骤

1. **检查 GPU 内存可用性**：
   - 您的程序使用 Thrust 的 `device_vector` 在 GPU 上分配了一个大型数组（`list_size = 50,000,000` 个整数，约 200 MB）。如果您的 GPU 内存有限或其他进程正在使用内存，则可能导致 `bad_alloc` 错误。
   - 运行 `nvidia-smi` 检查 GPU 内存使用情况：

     ```bash
     nvidia-smi
     ```

   - 确保 GPU 上有足够的空闲内存。如果其他进程正在占用内存，请终止它们或重启以释放资源。
   - **修复**：减少 `list_size` 以测试问题是否与内存相关。在 `main` 中尝试设置 `list_size = 10,000,000`（40 MB）：

     ```cuda
     int list_size = 10000000;
     ```

2. **验证 CUDA 安装和 GPU 兼容性**：
   - `cudaErrorUnknown` 表明可能存在 CUDA 驱动程序、运行时或 GPU 兼容性问题。请验证您的 CUDA 设置：

     ```bash
     nvcc --version
     nvidia-smi
     ```

   - 确保 CUDA 工具包版本与驱动程序版本匹配。例如，CUDA 11.x 需要兼容的 NVIDIA 驱动程序（请查阅 [NVIDIA 兼容性表](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)）。
   - **修复**：将您的 NVIDIA 驱动程序和 CUDA 工具包更新到最新版本。对于 Ubuntu，您可以使用以下命令更新驱动程序：

     ```bash
     sudo apt update
     sudo apt install nvidia-driver-<version> nvidia-cuda-toolkit
     ```

     将 `<version>` 替换为与您的 GPU 兼容的最新驱动程序版本。

3. **检查 CUDA 错误处理**：
   - 代码缺乏显式的 CUDA 错误检查，这有助于精确定位问题。修改 `parallel_sort_gpu` 以包含对 CUDA 操作的错误检查：

     ```cuda
     #include <cuda_runtime.h>
     #include <stdio.h>
     #include <stdlib.h>
     #include <thrust/device_vector.h>
     #include <thrust/sort.h>
     #include <time.h>

     void checkCudaError(cudaError_t err, const char *msg) {
         if (err != cudaSuccess) {
             fprintf(stderr, "CUDA Error: %s: %s\n", msg, cudaGetErrorString(err));
             exit(EXIT_FAILURE);
         }
     }

     void parallel_sort_gpu(int *arr, int n) {
         cudaError_t err;
         thrust::device_vector<int> d_vec(arr, arr + n);
         err = cudaGetLastError();
         checkCudaError(err, "After device_vector allocation");

         thrust::sort(d_vec.begin(), d_vec.end());
         err = cudaGetLastError();
         checkCudaError(err, "After thrust::sort");

         thrust::copy(d_vec.begin(), d_vec.end(), arr);
         err = cudaGetLastError();
         checkCudaError(err, "After thrust::copy");
     }

     double benchmark(int list_size) {
         int *arr = (int*)malloc(list_size * sizeof(int));
         if (!arr) {
             fprintf(stderr, "Host memory allocation failed\n");
             exit(EXIT_FAILURE);
         }
         for (int i = 0; i < list_size; ++i) {
             arr[i] = rand() % 1000001;
         }

         clock_t start = clock();
         parallel_sort_gpu(arr, list_size);
         clock_t end = clock();

         free(arr);
         return (double)(end - start) / CLOCKS_PER_SEC;
     }

     int main() {
         int list_size = 10000000; // 为测试而减小
         int num_runs = 8;

         printf("Run,TimeTakenSeconds\n");
         for (int i = 0; i < num_runs; ++i) {
             double t = benchmark(list_size);
             printf("%d,%.6f\n", i + 1, t);
         }
         return 0;
     }
     ```

   - **修复**：重新编译并运行修改后的代码以获取详细的错误信息：

     ```bash
     nvcc -o cudamark scripts/benchmark/cudamark.cu
     ./cudamark
     ```

4. **提高计时精度**：
   - `clock()` 函数测量的是 CPU 时间，而非 GPU 执行时间，这可能无法准确反映 GPU 排序性能。使用 CUDA 事件进行精确计时：

     ```cuda
     double benchmark(int list_size) {
         int *arr = (int*)malloc(list_size * sizeof(int));
         if (!arr) {
             fprintf(stderr, "Host memory allocation failed\n");
             exit(EXIT_FAILURE);
         }
         for (int i = 0; i < list_size; ++i) {
             arr[i] = rand() % 1000001;
         }

         cudaEvent_t start, stop;
         cudaEventCreate(&start);
         cudaEventCreate(&stop);
         cudaEventRecord(start);
         parallel_sort_gpu(arr, list_size);
         cudaEventRecord(stop);
         cudaEventSynchronize(stop);
         float milliseconds = 0;
         cudaEventElapsedTime(&milliseconds, start, stop);
         cudaEventDestroy(start);
         cudaEventDestroy(stop);

         free(arr);
         return milliseconds / 1000.0; // 转换为秒
     }
     ```

5. **确保 GPU 初始化**：
   - 如果 CUDA 上下文未正确初始化，Thrust 可能会失败。在 `main` 开头添加 `cudaSetDevice` 以确保 GPU 已初始化：

     ```cuda
     int main() {
         cudaError_t err = cudaSetDevice(0);
         checkCudaError(err, "cudaSetDevice failed");
         int list_size = 10000000;
         int num_runs = 8;

         printf("Run,TimeTakenSeconds\n");
         for (int i = 0; i < num_runs; ++i) {
             double t = benchmark(list_size);
             printf("%d,%.6f\n", i + 1, t);
         }
         return 0;
     }
     ```

6. **重新编译和测试**：
   - 将更新后的代码保存为 `cudamark.cu` 并编译：

     ```bash
     nvcc -o cudamark scripts/benchmark/cudamark.cu
     ```

   - 运行程序：

     ```bash
     ./cudamark
     ```

7. **处理 Thrust 异常**：
   - Thrust 可能因各种原因（例如无效内存访问）抛出异常。使用 try-catch 块包装 Thrust 操作以捕获更多详细信息：

     ```cuda
     void parallel_sort_gpu(int *arr, int n) {
         try {
             thrust::device_vector<int> d_vec(arr, arr + n);
             thrust::sort(d_vec.begin(), d_vec.end());
             thrust::copy(d_vec.begin(), d_vec.end(), arr);
         } catch (thrust::system_error &e) {
             fprintf(stderr, "Thrust error: %s\n", e.what());
             exit(EXIT_FAILURE);
         }
     }
     ```

8. **额外检查**：
   - **GPU 支持**：确保您的 GPU 支持 CUDA 和 Thrust。较旧的 GPU 可能不支持新的 CUDA 功能。请根据 NVIDIA 的 CUDA GPU 支持列表检查您的 GPU 型号。
   - **系统资源**：验证您的系统是否有足够的主机内存用于大型数组（50M 整数需要约 `200 MB`）。使用 `free -h` 检查可用 RAM。
   - **文件路径**：确认您正在运行正确的二进制文件。错误信息中提到 `./test/cudamark`，但编译的是 `scripts/benchmark/cudamark.c`。确保二进制文件是最新的且位于正确的目录中：

     ```bash
     nvcc -o test/cudamark scripts/benchmark/cudamark.cu
     ./test/cudamark
     ```

9. **如果问题仍然存在**：
   - **使用较小输入进行调试**：设置 `list_size = 1000` 以排除内存问题。
   - **检查 CUDA 日志**：在系统日志中查找详细错误，或使用 `cuda-memcheck`：

     ```bash
     cuda-memcheck ./cudamark
     ```

   - **重新安装 CUDA**：如果 CUDA 安装已损坏，请重新安装：

     ```bash
     sudo apt purge nvidia* cuda*
     sudo apt install nvidia-cuda-toolkit
     ```

### 预期结果

应用这些修复后，程序应不再出现 `bad_alloc` 或 `cudaErrorUnknown` 错误，并产生类似以下的输出：

```
Run,TimeTakenSeconds
1,0.123456
2,0.124567
...
```

### 如果遇到其他错误

- 请分享 `nvcc --version`、`nvidia-smi` 的输出以及更新代码后的任何新错误信息。
- 提供您的 GPU 型号和 CUDA 版本，以便获得针对性的建议。

如果您在某个具体步骤需要帮助，请告知我！
