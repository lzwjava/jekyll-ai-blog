---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Qwen GGUF Inference Setup
translated: false
type: note
---

Question: How can I use an AMD MI300X GPU to run inference on a 36GB Qwen model in GGUF format using `llama.cpp`?

Answer:

Running a large 36 GB Qwen model in GGUF format on an AMD MI300X GPU via `llama.cpp` involves several steps, because `llama.cpp` originally targets CPU inference but has experimental support for GPU backends including ROCm (AMD). Here's a detailed approach:

---

### 1. Prepare the Environment

1. **Install ROCm**
   MI300X uses ROCm (AMD’s GPU compute stack). You need a ROCm-compatible Linux system. Install ROCm following the official instructions:

   ```bash
   sudo apt update
   sudo apt install rocm-dkms rocm-dev rocm-utils
   ```

   Verify the GPU is recognized:

   ```bash
   /opt/rocm/bin/rocminfo
   ```

2. **Install Dependencies**
   `llama.cpp` requires CMake and a compiler supporting C++17. Install:

   ```bash
   sudo apt install build-essential cmake git
   ```

---

### 2. Build `llama.cpp` with ROCm Support

`llama.cpp` supports AMD GPUs through the ROCm backend (`--gpu-roc`).

1. Clone the repo:

   ```bash
   git clone https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   ```

2. Build with ROCm GPU support:

   ```bash
   make clean
   make ROCM=1
   ```

   You can check the `Makefile` to ensure `ROCM=1` enables HIP/ROCm compilation.

---

### 3. Prepare the Qwen GGUF Model

1. **Download the Qwen model** in GGUF format (36 GB). Ensure the model is compatible with `llama.cpp` GGUF support.
2. Place it in a directory accessible to your inference script.

> ⚠️ For a 36 GB model, GPU VRAM alone may not suffice if trying fully in-memory. The MI300X has massive HBM (~128 GB total across chips), but check if the software can utilize multiple compute units and memory efficiently.

---

### 4. Run Inference with `llama.cpp`

1. Use the GGUF path with `--model`:

   ```bash
   ./main -m /path/to/qwen-36B.gguf -p "Your prompt here" --gpu-roc
   ```

2. Optional flags for performance:

   * `-c` : context size (e.g., 8192 or more)
   * `-n` : number of tokens to generate
   * `--threads` : CPU fallback threads for mixing GPU/CPU
   * `--memory-f16` or `--memory-q4_0` : optimize memory if supported

---

### 5. Tips and Notes

* **Memory Management:** For such a large model, consider offloading layers to CPU if GPU memory is exceeded.
* **Batching:** Large models can benefit from batching prompts to optimize throughput.
* **Debugging:** ROCm support in `llama.cpp` is experimental. Expect some trial and error; logs and verbose mode help.
* **Alternative:** If MI300X is connected to AMD Developer Cloud or MI300 series workstation, ROCm-ready docker images with `llama.cpp` prebuilt can save setup time.

---

This approach lets you leverage the MI300X’s high memory bandwidth and ROCm compute for large model inference, while still using a lightweight C++ inference framework like `llama.cpp`.

---

References:

* [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
* [AMD ROCm Documentation](https://rocmdocs.amd.com)
* [Qwen Model GGUF Format Info](https://github.com/qwen-models/qwen)

---

If you want, I can draft a **ready-to-run shell command template** for MI300X to immediately launch inference on your 36 GB Qwen GGUF model with optimal memory settings. It’ll save you trial-and-error time.
