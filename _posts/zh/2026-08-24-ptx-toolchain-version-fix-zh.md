---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PTX工具链版本修复
translated: true
type: note
---

已修复。`GPU 0: OK`，退出码 0。

## 问题原因

这是两层问题，都涉及 **PTX 工具链版本** 与你的驱动：

1. **捆绑的 `compare.fatbin` 使用 CUDA 9.2**（PTX ISA 6.0，架构 sm_75）编译。你的驱动 580.178.04 对应 CUDA 13.0，现代驱动拒绝 JIT 编译来自如此旧工具链的 PTX → "所提供的 PTX 使用了不支持的编译工具链"。
2. **使用默认的 nvcc (13.2) 重新编译也失败了**——nvcc 13.2 生成的 PTX ISA 9.2，比 CUDA 13.0 驱动的 JIT 支持版本*更新*。同样的错误信息。

## 修复方法

改用已安装的 **CUDA 12.8** 工具包构建 fatbin（PTX ISA 8.7，在 13.0 驱动支持范围内），目标架构为你的 RTX 4070 的原生架构 **sm_89**：

```bash
cd ~/projects/gpu-burn
/usr/local/cuda-12.8/bin/nvcc -I/usr/local/cuda-12.8/include \
  -arch=compute_89 -fatbin compare.cu -o compare.fatbin
make
```

验证结果：`./gpu_burn 5` → `Tested 1 GPUs: GPU 0: OK`，运行约 20 Tflop/s，0 错误，温度 37→60 °C。

## 未来重建注意事项

单独执行 `make clean && make` 会恢复到损坏的 13.2 fatbin。要正确重建：

```bash
make clean
make CUDAPATH=/usr/local/cuda-12.8 COMPUTE=89
```

（`COMPUTE=89` 是可选的，但会为 4070 生成原生 SASS/PTX，而不是从 sm_75 进行 JIT 编译。）