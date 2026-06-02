---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X GPU服务器分析与测试
translated: true
type: note
---

以下是关于该服务器的完整详细信息：

---

## 服务器配置：165.245.137.138

| 属性 | 值 |
|---|---|
| 主机名 | `7` (Ubuntu 24.04) |
| 内核 | `6.8.0-106-generic` |
| CPU 架构 | x86_64 |
| 内存 | 235 GB 总量（230 GB 空闲） |
| 磁盘 | 697 GB（611 GB 空闲） |
| SSH 认证 | 公钥（无密码） |

---

## GPU：AMD Instinct MI300X（虚拟功能）

| 属性 | 值 |
|---|---|
| PCI 设备 | `0000:83:00.0` |
| 设备 ID | `0x74b5` (MI300X VF) |
| GFX 版本 | `gfx942` |
| HBM3 显存 | 256 GB（BAR 位于 `0x4000000000`） |
| PCIe 链路 | 5.0 x16 @ 32 GT/s |
| NUMA 节点 | 0 |
| 分区 | 0（完整 GPU） |
| ROCm | **7.2.0** 已安装于 `/opt/rocm-7.2.0` |
| GPU 固件 | 已加载（内核内 amdgpu v6.16.13） |
| RAS | GFX+SDMA+UMC 均已启用 |
| 电源状态 | D0（活动状态，首次使用前处于低功耗状态） |

---

## ROCm 堆栈健康状态

| 组件 | 状态 |
|---|---|
| `amdgpu` 内核模块 | 已加载（内核内） |
| `rocm-smi` | 正常工作 — 正确识别 GPU |
| `rocminfo` | 位于 `/opt/rocm-7.2.0/bin/rocminfo` |
| `hipcc` | 可用（`/opt/rocm-7.2.0/bin/hipcc`） |
| KFD 拓扑 | 节点 0 和 1 均存在（GPU 已枚举） |
| KFD simd | GPU 可通过 KFD 可见（非盲 VF） |

---

## llama.cpp 构建详情

| 属性 | 值 |
|---|---|
| 源码 | `https://github.com/ggerganov/llama.cpp.git` |
| 提交 | `b39a7bf` (v0.12.0) |
| 构建目录 | `/root/llama.cpp/build/` |
| CMake 标志 | `-DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942` |
| 后端 | CPU + HIP/ROCm |
| HIP 编译器 | Clang 22.0.0 (ROCm) |
| 输出二进制 | `/root/llama.cpp/build/bin/llama-cli` |
| 下载的模型 | Qwen2.5-0.5B-Instruct Q4_K_M (469 MB) |

---

## 烟雾测试结果

运行 Qwen2.5-0.5B，所有层卸载至 GPU（`-ngl 99`）：

```
提示： "Hello, could you introduce yourself briefly?"

回复： Of course! I am Qwen, a large language model created by Alibaba Cloud...

性能：
  提示处理：  748.7 令牌/秒
  文本生成：  484.2 令牌/秒
```

提示词输入和令牌生成均在 MI300X 上通过 HIP 后端运行 — 确认功能完全正常。

---

## 快速参考命令（供后续使用）

```bash
# 重新构建（如需）
cd /root/llama.cpp
export ROCM_PATH=/opt/rocm-7.2.0 && export HIP_PATH=$ROCM_PATH && export PATH=$ROCM_PATH/bin:$PATH
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx942
cmake --build build -j$(nproc) --target llama-cli

# 运行推理
./build/bin/llama-cli -m models/tiny-model.gguf -ngl 99 -p "Your prompt" -n 200
```

一切就绪。你可以在那 256 GB HBM3 上运行更大的模型——它几乎可以处理你投入的任何开源权重模型。
