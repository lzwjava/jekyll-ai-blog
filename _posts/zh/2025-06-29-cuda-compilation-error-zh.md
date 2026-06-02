---
audio: false
generated: true
lang: zh
layout: post
title: 修复nvcc的CUDA编译错误
translated: true
type: note
---

该错误表明CUDA工具包未安装或配置不当，因为编译器无法找到 `cuda.h`。此外，您的代码是CUDA源文件（`.cu`），但尝试使用 `gcc` 编译，而 `gcc` 并不适用于CUDA代码。您需要使用NVIDIA CUDA编译器 `nvcc`。以下是解决方法：

### 解决步骤

1. **安装CUDA工具包**：
   - 确保系统已安装NVIDIA CUDA工具包。可从 [NVIDIA CUDA工具包官网](https://developer.nvidia.com/cuda-downloads) 下载。
   - 根据操作系统（根据提示信息应为Linux）按照安装说明进行操作。
   - 安装后通过以下命令验证：
     ```bash
     nvcc --version
     ```
     若安装正确，将显示CUDA版本信息。

2. **使用 `nvcc` 编译**：
   - 由于文件是CUDA源文件（`.cu`），应使用 `nvcc` 替代 `gcc` 编译。将：
     ```bash
     gcc scripts/benchmark/cudamark.c
     ```
     替换为：
     ```bash
     nvcc scripts/benchmark/cudamark.cu
     ```
   - 注意：确保文件扩展名与实际文件匹配（代码中为 `.cu`，而非错误提示中的 `.c`）。

3. **配置CUDA环境**：
   - 确保环境变量包含CUDA工具包路径。将以下内容添加到 `~/.bashrc` 或等效的shell配置文件中：
     ```bash
     export PATH=/usr/local/cuda/bin:$PATH
     export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
     ```
     随后执行：
     ```bash
     source ~/.bashrc
     ```

4. **链接Thrust库**：
   - 代码使用的Thrust库已包含在CUDA工具包中，无需显式链接额外库。但请确保CUDA版本兼容（CUDA 7.0及以上版本包含Thrust）。

5. **修复代码问题**：
   - 代码中引用了 `thread_counts` 但未在 `benchmark` 函数中使用。`parallel_sort_gpu` 函数使用Thrust库，其内部自动管理并行性，因此 `main` 函数中的 `thread_counts` 循环存在误导。若需测试不同线程配置，需注意Thrust的排序函数不支持直接控制线程数。建议澄清该逻辑或移除未使用的 `thread_counts`。
   - 为提升时序测量准确性，可修改代码对同一列表尺寸进行多次基准测试：

     ```cuda
     #include <stdio.h>
     #include <stdlib.h>
     #include <cuda.h>
     #include <thrust/device_vector.h>
     #include <thrust/sort.h>
     #include <time.h>

     void parallel_sort_gpu(int *arr, int n) {
         thrust::device_vector<int> d_vec(arr, arr + n);
         thrust::sort(d_vec.begin(), d_vec.end());
         thrust::copy(d_vec.begin(), d_vec.end(), arr);
     }

     double benchmark(int list_size) {
         int *arr = (int*)malloc(list_size * sizeof(int));
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
         int list_size = 50000000;
         int num_runs = 8; // 用于计算平均值的运行次数

         printf("Run,TimeTakenSeconds\n");
         for (int i = 0; i < num_runs; ++i) {
             double t = benchmark(list_size);
             printf("%d,%.6f\n", i + 1, t);
         }
         return 0;
     }
     ```

6. **编译更新后的代码**：
   - 将代码保存为 `cudamark.cu` 后编译：
     ```bash
     nvcc -o cudamark scripts/benchmark/cudamark.cu
     ```
   - 若出现链接错误，请确认CUDA库路径可访问（参考步骤3）。

7. **运行程序**：
   - 执行编译后的二进制文件：
     ```bash
     ./cudamark
     ```

8. **补充说明**：
   - **文件扩展名**：确保文件扩展名为 `.cu`，这是 `nvcc` 正确处理CUDA文件的必要条件。
   - **GPU可用性**：确保具备支持CUDA的GPU并安装正确驱动。可通过以下命令检查：
     ```bash
     nvidia-smi
     ```
   - **Thrust与CUDA版本**：确认CUDA版本支持Thrust。建议使用CUDA 11.x或更高版本以获得现代Thrust功能支持。
   - **计时精度**：`clock()` 函数测量的是CPU时间，而非GPU执行时间。如需更精确的GPU计时，建议使用CUDA事件：
     ```cuda
     cudaEvent_t start, stop;
     cudaEventCreate(&start);
     cudaEventCreate(&stop);
     cudaEventRecord(start);
     parallel_sort_gpu(arr, list_size);
     cudaEventRecord(stop);
     cudaEventSynchronize(stop);
     float milliseconds = 0;
     cudaEventElapsedTime(&milliseconds, start, stop);
     return milliseconds / 1000.0; // 转换为秒
     ```

9. **若问题仍存在**：
   - 若仍提示找不到 `cuda.h`，请验证CUDA工具包安装路径（例如 `/usr/local/cuda/include`）。可能需要显式指定包含路径：
     ```bash
     nvcc -I/usr/local/cuda/include -o cudamark scripts/benchmark/cudamark.cu
     ```
   - 确保文件路径 `scripts/benchmark/cudamark.cu` 相对于当前目录正确。

### 更新后的编译命令
```bash
nvcc -o cudamark scripts/benchmark/cudamark.cu
```

### 预期输出
解决问题后，运行 `./cudamark` 应输出类似以下内容：
```
Run,TimeTakenSeconds
1,0.123456
2,0.124567
...
```

如需进一步协助或遇到具体错误，请随时分享！
