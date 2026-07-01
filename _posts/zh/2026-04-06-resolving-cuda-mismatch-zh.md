---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决CUDA版本不匹配问题
translated: true
type: note
---

## 🦞 驱动程序升级回顾：570 → 580

### 问题

llama.cpp 编译时针对 CUDA 13.2 工具包，但驱动程序 570 仅支持 CUDA 12.8。每次 GPU 初始化调用均失败，报错如下：

```
ggml_cuda_init: failed to initialize CUDA: CUDA driver version is insufficient for CUDA runtime version
```

### 我的操作

**1. 诊断版本不匹配**

- `nvidia-smi` → 驱动程序 570.211.01，CUDA 12.8
- `nvcc --version` → CUDA 13.2.51
- 运行时（`libcudart.so.13`）在 `cuInit()` 时检查驱动程序版本并中止，因为驱动程序 570 的 `libcuda.so` 不支持 13.x 版本的 ABI

**2. 尝试链接时变通方案（失败）**

- **LD_PRELOAD** 使用 CUDA 12.2 的 `libcudart.so.12` — 无效，因为 `libggml-cuda.so` 文件内硬编码了针对 `libcudart.so.13`、`libcublas.so.13`、`libcublasLt.so.13` 的 `NEEDED` 条目。动态链接器会先解析这些依赖，然后才检查 LD_PRELOAD
- **patchelf** 将 `*.so.13` 替换为 `*.so.12` — 通过了 soname 检查，但遇到 `version 'libcudart.so.13' not found` 错误，因为二进制文件绑定了来自 13.x ABI 的符号版本，而这些版本在 12.x 中不存在。这是编译时 ABI 不匹配，无法通过补丁解决

**3. 彻底修复：升级驱动程序**

- 检查 `apt-cache search` — 仓库中提供了 `nvidia-driver-580`
- 试运行显示有干净的升级路径，可以替换所有 570 软件包
- 遇到一个文件冲突：`libnvidia-extra-570` 拥有 `/usr/lib/x86_64-linux-gnu/gbm/nvidia-drm_gbm.so` 文件，而 580 的 `libnvidia-gl-580` 也需要该文件。清除了残留的 570 软件包，运行 `apt install -f` 完成安装
- DKMS 为内核 6.8.0-107 构建了内核模块

**4. 准备重启**

- 驱动程序 580 支持 CUDA 13.x → 不再有版本不匹配问题
- llama.cpp 需要在重启后进行一次干净的重新构建（cmake 配置已完成）
- 执行一次 `make -j$(nproc) llama-server` 并使用 `-ngl 99` 启动

### 为何选择升级到 580 而非使用 CUDA 12 重新构建？

- 系统中存在 CUDA 12.2 运行时库，但**没有 nvcc 12.2 编译器** — 仅安装了 nvcc 13.2
- 安装 nvcc 12.2 需要 `cuda-nvcc-12-2` 软件包并进行完整重建，并且我们长期来看仍将停留在一个较旧的工具包版本上
- 驱动程序升级是一次性的修复，可以使现有的 CUDA 13.2 工具包永久正常工作

### 当前状态

| 项目 | 状态 |
| ------ | -------- |
| nvidia-driver-580 软件包 | ✅ 已安装 |
| DKMS 模块（6.8.0-107） | ✅ 已构建 |
| CMake 配置 | ✅ 完成 |
| 内核模块加载 | ⏳ 需重启 |
| llama-server 构建完成 | ⏳ 重启后 |
| GPU 推理 | ⏳ 重启后 |
