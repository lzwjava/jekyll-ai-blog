---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X Qwen GGUF 推理设置
translated: true
type: note
---

问题：如何使用AMD MI300X GPU通过`llama.cpp`对36GB的Qwen GGUF格式模型进行推理？

答案：

在AMD MI300X GPU上通过`llama.cpp`运行36GB的大型Qwen GGUF格式模型，需要几个步骤，因为`llama.cpp`最初针对CPU推理，但对包括ROCm（AMD）在内的GPU后端提供实验性支持。以下是详细方法：

---

### 1. 准备环境

1. **安装ROCm**
   MI300X使用ROCm（AMD的GPU计算栈）。你需要一个兼容ROCm的Linux系统。按照官方说明安装ROCm：

   ```bash
   sudo apt update
   sudo apt install rocm-dkms rocm-dev rocm-utils
   ```

   确认GPU被识别：

   ```bash
   /opt/rocm/bin/rocminfo
   ```

2. **安装依赖**
   `llama.cpp`需要CMake和编译器支持C++17。安装：

   ```bash
   sudo apt install build-essential cmake git
   ```

---

### 2. 构建支持ROCm的`llama.cpp`

`llama.cpp`通过ROCm后端（`--gpu-roc`）支持AMD GPU。

1. 克隆仓库：

   ```bash
   git clone https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   ```

2. 构建并启用ROCm GPU支持：

   ```bash
   make clean
   make ROCM=1
   ```

   你可以检查`Makefile`以确保`ROCM=1`启用了HIP/ROCm编译。

---

### 3. 准备Qwen GGUF模型

1. **下载Qwen模型**（GGUF格式，36GB）。确保模型兼容`llama.cpp`的GGUF支持。
2. 将其放置在你的推理脚本可访问的目录中。

> ⚠️ 对于36GB的模型，如果尝试完全在内存中运行，GPU VRAM可能不够。MI300X拥有巨大的HBM（跨芯片总计约128GB），但需检查软件是否能高效利用多个计算单元和内存。

---

### 4. 使用`llama.cpp`运行推理

1. 使用`--model`指定GGUF路径：

   ```bash
   ./main -m /path/to/qwen-36B.gguf -p "你的提示语" --gpu-roc
   ```

2. 可选的性能参数：

   * `-c`：上下文大小（例如8192或更大）
   * `-n`：生成的token数量
   * `--threads`：用于混合GPU/CPU的CPU回退线程数
   * `--memory-f16` 或 `--memory-q4_0`：如果支持，优化内存使用

---

### 5. 提示与说明

* **内存管理：** 对于如此大的模型，如果GPU内存不足，考虑将部分层卸载到CPU。
* **批处理：** 大型模型可以通过批处理提示来优化吞吐量。
* **调试：** `llama.cpp`对ROCm的支持是实验性的。可能需要一些试错；日志和详细模式会有所帮助。
* **替代方案：** 如果MI300X连接到AMD开发者云或MI300系列工作站，可以使用预置`llama.cpp`的ROCm就绪Docker镜像，节省设置时间。

---

这种方法可以让你利用MI300X的高内存带宽和ROCm计算能力进行大型模型推理，同时仍然使用像`llama.cpp`这样的轻量级C++推理框架。

---

参考：

* [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
* [AMD ROCm 文档](https://rocmdocs.amd.com)
* [Qwen 模型 GGUF 格式信息](https://github.com/qwen-models/qwen)

---

如果你需要，我可以为你草拟一个**可直接运行的shell命令模板**，用于在MI300X上以最佳内存设置立即启动对36GB Qwen GGUF模型的推理。这将节省你反复试错的时间。
