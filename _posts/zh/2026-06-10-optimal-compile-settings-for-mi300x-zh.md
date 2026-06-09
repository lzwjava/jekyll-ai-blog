---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X的最佳编译设置
translated: true
type: note
---

问题：已知环境是 AMD AI Developer Cloud 实例（`snapshots-gpu-mi300x1-192gb-devcloud-atl1`），最佳编译设置是什么？

答案：在标准 **AMD Developer Cloud** 实例（`snapshots-gpu-mi300x1-192gb-devcloud-atl1`）上运行，明确了确切的主机系统硬件规格。

单个 AMD Instinct MI300X 实例在 AMD Developer Cloud 上的配置为：

* **vCPU：** 20 核
* **系统 RAM：** 240 GB DDR5

---

## 结论：你可以安全地提高 `MAX_JOBS`

拥有 **240 GB 系统 RAM**，你的实例有足够的内存余量。按照重型 HIP/C++ 编译的基线内存规则（每个编译器实例约 6 GB 到 8 GB）：

$$\frac{240\text{ GB RAM}}{8\text{ GB/作业}} = 30\text{ 个最大并发作业}$$

由于系统上限为 **20 vCPU**，总 CPU 线程数是主要限制因素，而非 RAM。

你可以积极扩展配置以最大化硬件利用率。将 `MAX_JOBS` 设置为 **16** 大约使用了可用处理能力的 80%，同时为操作系统和后台任务保留了充足的缓冲，完全避免了内存不足（OOM）崩溃的风险。

---

## 推荐的快速构建脚本

在终端中运行以下序列，以清理环境并使用 16 个并行线程重新启动编译过程。这将把编译时间从将近一小时缩短到大约 **12 到 18 分钟**：

```bash
# 1. 清理之前的慢速/部分构建
cd /tmp/flash-attention && rm -rf build/ dist/ *.egg-info

# 2. 重新激活并导出针对该实例的最佳设置
source /root/nanochat/.venv/bin/activate
export ROCM_PATH=/opt/rocm-7.2.0
export HIP_PATH=$ROCM_PATH
export PATH=$ROCM_PATH/bin:$PATH
export GPU_ARCHS="gfx942"

# 设置为 16 个作业（完美适配你的 20 vCPU / 240GB RAM 云配置）
export MAX_JOBS=16

# 3. 重新运行并记录日志
echo "=== 开始优化后的 16 作业 FlashAttention 构建 ==="
python setup.py install 2>&1 | tee /tmp/flash_attn_build_fast.log

```