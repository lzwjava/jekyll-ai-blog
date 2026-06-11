---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU硬件学习的开源项目
translated: true
type: note
---

**问题：** 有哪些优秀的开源项目适合学习 HBM 内存、GPU 芯片及相关硬件的工作原理？

**回答：**

关键在于从三个层面入手：**RTL（实际芯片逻辑）**、**周期精确模拟器（HBM 时序所在）** 以及**软件/驱动栈（你已有硬件——MI300X 和 RTX 4070）**。以下是按学习性价比排序的进阶路径。

## 第1层：GPU RTL——阅读真实的 Verilog

**[tiny-gpu](https://github.com/adam-maj/tiny-gpu)** —— 从这里开始，周末即可完成。这是一个用 Verilog 实现的最小 GPU，专为从零学习 GPU 工作原理而优化，因为像 MIAOW 和 VeriGPU 这样的完整项目过于复杂，不适合学习。包含约 15 个 Verilog 文件：一个调度器、带有取指/译码/调度/ALU/LSU 的计算核心，以及一个内存控制器。你将看到 SIMD 执行和内存延迟隐藏最原始的形式。

```bash
git clone https://github.com/adam-maj/tiny-gpu && cd tiny-gpu
pip install cocotb  # 测试平台是 Python，非常易于上手
make test_matadd    # 观察矩阵加法内核逐周期执行
```

**[Vortex](https://github.com/vortexgpgpu/vortex)** —— 严肃的项目。一个开源的基于 RISC-V 的 GPGPU 硬件和软件，支持 OpenCL/CUDA，可在 FPGA 上运行，并附带完整的开源编译器、驱动和运行时栈。这个项目现在更有意思了：Vortex 3.0（本周发布）增加了固定功能 3D 图形管线（含光栅化器和纹理单元）、张量核心结构化稀疏、线程束组级矩阵乘法、硬件内核调度器，以及 Mesa Vulkan 后端和通过 chipStar 实现的 HIP 支持。它还增加了针对 ASAP7（7nm）和 SAED14 预测工艺节点的 ASIC 综合流程——因此你可以将相同的 RTL 从 FPGA 带到无需任何许可的综合流程中。

关键的学习特性：开发者在进行 RTL 实现之前先在 `simx`（一个周期级 C++ 模拟器）中设计原型——因此你可以*两次阅读相同的微架构*，一次是可读的 C++，一次是 SystemVerilog。研究缓存子系统（`hw/rtl/cache/`）和内存互连，了解 GPU 如何实际为带宽饥渴的核心提供数据。

值得一提的还有：**Ventus**（清华大学的基于 RISC-V 向量的 GPGPU——鉴于你的位置/网络，这很相关）、**MIAOW**（AMD Southern Islands ISA 克隆）、**Nyuzi**。

## 第2层：HBM——模拟器才是学习的关键

没有开源的 HBM PHY/RTL（PHY + 中介层 IP 是 Synopsys/Rambus 的皇冠明珠）。但开放的是时序模型和内存控制器逻辑，这对于理解 MI300X 性能来说占了 90%。

**[Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2)**（CMU SAFARI / Onur Mutlu 团队）—— 学习 DRAM/HBM 内部结构的最佳代码库。一个模块化、可扩展、周期精确的 DRAM 模拟器，采用 MIT 许可证，包含 DDR3/4/5、LPDDR5、GDDR6 和 HBM/HBM2/HBM3 模型。HBM3 模型是一个单一的可读文件，编码了完整的 JEDEC 状态机——bank、bank 组、伪通道、tRCD/tRP/tFAW 时序约束：

```bash
git clone https://github.com/CMU-SAFARI/ramulator2 && cd ramulator2
mkdir build && cd build && cmake .. && make -j
# 然后阅读：src/dram/impl/HBM3.cpp  ← 整个 HBM3 规范以代码形式呈现
./ramulator2 -f ../example_config.yaml  # 将 DRAM 类型切换为 HBM3，重放 trace
```

对相同的内存 trace 运行 DDR5 与 HBM3 配置对比，观察为什么 HBM 在带宽上胜出（32 个伪通道）但在延迟上并非如此。这一单个实验比任何数据手册都更有教育意义。

**[DRAMsim3](https://github.com/umd-memsys/DRAMsim3)**—— 周期精确，同时包含热建模和性能建模，专门为模拟 3D 堆叠 DRAM 而构建——这与 HBM 的热行为（中介层上的堆叠芯片）是 MI300X 的真实约束相关。

**[gem5](https://gem5.org)**—— 当你需要全系统模拟时：CPU + GPU（它有一个 GCN3/Vega GPU 模型）+ HBM，全部一起模拟。Ramulator 2.0 可与 gem5 集成。较重量级，第三个学习。

**[LiteDRAM](https://github.com/enjoy-digital/litedram)**—— 一个用 Migen（Python 生成的 HDL）编写的 DRAM *控制器*。不是 HBM，但它是现存最可读的开源内存控制器，而且是 Python 的——非常适合你的工作流程。

## 第3层：软件栈——你拥有 MI300X 的使用时间，好好利用

**[ROCm](https://github.com/ROCm/ROCm)** + `amdkfd` 内核驱动——AMD 的整个栈都是开放的。追踪 `hipMalloc` 如何变成 HBM 页面：HIP 运行时 → ROCr → KFD ioctls → GPU 页表。然后测量你的实际 HBM3：

```cpp
// hbm_bw.cpp —— MI300X 上的 STREAM triad，测量实际 HBM3 带宽
#include <hip/hip_runtime.h>
#include <cstdio>
__global__ void triad(float* a, const float* b, const float* c, float s, size_t n) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) a[i] = b[i] + s * c[i];
}
int main() {
    size_t n = 1ULL << 30;  // 每个数组 4 GB，总共 12 GB —— 对于 192GB 来说微不足道
    float *a, *b, *c;
    hipMalloc(&a, n*4); hipMalloc(&b, n*4); hipMalloc(&c, n*4);
    hipEvent_t t0, t1; hipEventCreate(&t0); hipEventCreate(&t1);
    hipEventRecord(t0);
    for (int i = 0; i < 10; i++)
        triad<<<(n+255)/256, 256>>>(a, b, c, 2.0f, n);
    hipEventRecord(t1); hipEventSynchronize(t1);
    float ms; hipEventElapsedTime(&ms, t0, t1);
    printf("HBM BW: %.1f GB/s (理论值 MI300X: 5300)\n",
           10.0 * 3 * n * 4 / (ms * 1e6));
}
// hipcc hbm_bw.cpp -o hbm_bw && ./hbm_bw
```

你应该会看到约 3.5–4 TB/s 的实际值，而理论值为 5.3 TB/s——然后问题“剩下的带宽去哪了？”会将你引回 Ramulator 的 bank 冲突和刷新建模。这个循环（在实际硬件上测量 → 在模拟器中解释）是建立真正直觉的最快方式。

**[tinygrad](https://github.com/tinygrad/tinygrad)**—— 拥有自己的 AMD 驱动，可以在 PM4 包/ioctl 级别与 GPU 通信，绕过 ROCm。阅读 `tinygrad/runtime/ops_amd.py` 是理解 GPU 驱动*到底是什么*的最短路径。还有针对你的 4070 的 **NVIDIA 的 [open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules)**。

## 第4层（可选）：RTL → 硅片

**[OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD)** / **[OpenLane](https://github.com/efabless/openlane2)** 用于综合/布局布线，**[Verilator](https://github.com/verilator/verilator)** 用于快速 RTL 仿真，**[Tiny Tapeout](https://tinytapeout.com)** 如果你想要实际硅片（约 $300）。

## 推荐计划

1. **第1周：** 在 MacBook Air 上完整运行 tiny-gpu（cocotb 仿真很轻量）。
2. **第2–4周：** Ramulator2 —— 阅读 `HBM3.cpp`，运行 DDR5 与 HBM3 的 trace 实验。这相当于内存系统领域的 nanoGPT：小巧、完整、可修改。
3. **并行进行：** 在你的 AMD 云实例上线时，运行 HIP 带宽基准测试 + `rocprof` —— 将模拟器数字与硅片结果联系起来。
4. **第2个月及以后：** Vortex `simx` → RTL，重点关注缓存/内存层次结构。这直接服务于你的推理优化目标：一旦你在 RTL 中看到 GPU LSU 如何合并访问，KV-cache 布局和内存受限内核优化就不再是传说了。

**参考资料：**

- [tiny-gpu](https://github.com/adam-maj/tiny-gpu)
- [Vortex GPGPU](https://github.com/vortexgpgpu/vortex)
- [Vortex 3.0 发布报道 — Phoronix](https://www.phoronix.com/news/Vortex-3.0-RISC-V-GPGPU)
- [Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2) / [论文](https://people.inf.ethz.ch/omutlu/pub/Ramulator2_arxiv23.pdf)
- [DRAMsim3](https://github.com/umd-memsys/DRAMsim3)
- [LiteDRAM](https://github.com/enjoy-digital/litedram)
- [tinygrad](https://github.com/tinygrad/tinygrad)
- [NVIDIA 开源 GPU 内核模块](https://github.com/NVIDIA/open-gpu-kernel-modules)
