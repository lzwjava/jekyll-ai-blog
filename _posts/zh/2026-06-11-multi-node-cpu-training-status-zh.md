---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多节点CPU训练状态
translated: true
type: note
---

以下是我们的进展总结和当前状态：

---

## 多节点CPU分布式训练设置 — 状态报告

### 我们发现的内容

**机器清单：**

```
192.168.1.36 (lzw@) — 主节点
  CPU:  i9-13900KF, 24核/32线程
  内存: 62 GB
  GPU:  RTX 4070 12GB (CUDA)
  Torch: 2.9.1+cu128

192.168.1.47 (xiaoxin@xx) — 工作节点
  CPU:  i5-12450H, 8核/12线程
  内存: 16 GB
  GPU:  Intel UHD (集成显卡，无CUDA)
  Torch: 2.9.1+cpu (刚安装)
```

**关键架构洞察：** Nanochat 并未使用 PyTorch 的 DDP 封装器。相反，它有一个自定义的 `DistMuonAdamW` 优化器，直接使用 `dist.all_reduce` / `dist.reduce_scatter_tensor` / `dist.all_gather_into_tensor` 处理梯度同步 —— 这是一种 ZeRO-2 风格的方法。

### 已应用的代码补丁（3个文件）

**1. `nanochat/common.py` — compute_init()**
为 CPU DDP 添加了 Gloo 后端支持：

```python
elif is_ddp_requested and device_type == "cpu":
    device = torch.device("cpu")
    dist.init_process_group(backend="gloo")
    dist.barrier()
```

**2. `nanochat/flash_attention.py` — _resolve_impl()**
添加了 `NANOCHAT_FORCE_SDPA=1` 环境变量覆盖。Flash Attention 仅适用于 CUDA；CPU 训练必须使用 PyTorch SDPA 回退方案。

**3. `nanochat/optim.py` — DistMuonAdamW**
添加了 `_AsyncWorkWrapper` + `_async_op()` 辅助函数，因为 Gloo 不支持 `Work.get_future()`（NCCL 支持）。所有 5 个 `.get_future()` 调用均被封装：

```python
class _AsyncWorkWrapper:
    def __init__(self, work):
        self._work = work
    def wait(self):
        self._work.wait()

def _async_op(work):
    try:
        return work.get_future()
    except RuntimeError:
        return _AsyncWorkWrapper(work)
```

**4. `nanochat/dataset.py`**
添加了 `NANOCHAT_DATA_DIR` 环境变量覆盖，使两台机器能使用共享的数据分片子集。

### 已生效的部分

**在 1.36 上单进程 CPU 训练：** ✅

```
step 00001 | loss: 10.397800 | tok/sec: 45
```

**在 1.36 上单节点双进程 CPU DDP（Gloo）：** ✅

```
step 00001 | loss: 10.397759 | tok/sec: 89  (2倍加速!)
```

Gloo 连接成功，梯度同步正常，检查点保存正常。

### 仍需完成的部分

**1. 数据一致性：**两台机器需要相同的 parquet 文件。当前状态：

- 1.36：`~/.cache/nanochat/base_data_climbmix/` 中有 201 个分片（18GB）
- 1.47：`~/.cache/nanochat/base_data_climbmix/` 中有 4 个分片（352MB）
- 已在 1.36 上创建了包含 4 个分片的 `base_data_small/` 符号链接目录
- 需要在两台机器上都以 `NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small` 运行

**2. 端口 29500 访问：**主节点（1.36）需要确保 1.47 能访问端口 29500。已验证网络连接正常（SSH 端口 22 可达）。

**3. 最终多节点测试尚未运行。**所有补丁已在两台机器上同步。

### 如何运行多节点训练

**在 1.36（主节点）—— 终端 1：**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
export NANOCHAT_BASE_DIR=~/.cache/nanochat
export NANOCHAT_DATA_DIR=~/.cache/nanochat/base_data_small
export NANOCHAT_FORCE_SDPA=1
export OMP_NUM_THREADS=8
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=0 \
    --master_addr=192.168.1.36 --master_port=29500 \
    -m scripts.base_train -- \
    --device-type cpu --depth 4 --max-seq-len 512 \
    --device-batch-size 2 --total-batch-size 2048 \
    --num-iterations 20 --eval-every 10 --tracker none --run dist-cpu-2node
```

**在 1.47（工作节点）—— 终端 2：**

```bash
cd ~/projects/nanochat && source .venv/bin/activate
export NANOCHAT_BASE_DIR=~/.cache/nanochat
export NANOCHAT_FORCE_SDPA=1
export OMP_NUM_THREADS=4
torchrun --nnodes=2 --nproc_per_node=1 --node_rank=1 \
    --master_addr=192.168.1.36 --master_port=29500 \
    -m scripts.base_train -- \
    --device-type cpu --depth 4 --max-seq-len 512 \
    --device-batch-size 2 --total-batch-size 2048 \
    --num-iterations 20 --eval-every 10 --tracker none --run dist-cpu-2node
```

**启动脚本也已保存：**

- 1.36 上的 `/mnt/data/nanochat/run_dist_cpu_master.sh`
- 1.47 上的 `~/projects/nanochat/run_dist_cpu_worker.sh`

### 关键要点

1. **后端选择：** NCCL（GPU 到 GPU，高带宽） vs Gloo（CPU 到 CPU，基于 TCP 网络）
2. **无需 DDP 封装器：** Nanochat 使用自定义优化器级别的梯度同步（ZeRO-2 风格）
3. **异步操作：** NCCL 支持 `get_future()` 实现异步通信；Gloo 需要同步回退方案
4. **Flash Attention 仅限 CUDA：** CPU 训练必须强制使用 SDPA 回退方案
5. **torchrun 的 `--` 分隔符：** 脚本参数中的 `--run` 与 torchrun 的 `--run-path` 冲突；使用 `--` 进行分隔
6. **批次大小计算：** `total_batch_size` 必须能被 `device_batch_size × seq_len × world_size` 整除
