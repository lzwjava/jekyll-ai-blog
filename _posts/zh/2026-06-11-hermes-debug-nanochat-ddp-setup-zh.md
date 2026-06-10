---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes调试：Nanochat DDP设置
translated: true
type: note
---

**问题：** 总结此 Hermes 代理日志——在设置 nanochat 的多节点 CPU DDP 训练时，关键步骤有哪些，代理是如何解决每个问题的？

**回答：**

## 目标

使用 PyTorch 分布式和 **Gloo** 后端（纯 CPU DDP），在局域网内的两台机器上运行 nanochat `base_train`：主节点 = 工作站（i9-13900KF，24 核），工作节点 = 笔记本电脑（i5-12450H，8 核）。原版 nanochat 假定使用 CUDA + NCCL，因此需要对多个层进行修补。

## 关键步骤

**1. 工作节点上的环境设置（最慢的部分，主要是等待）**

- 从 PyTorch 索引安装了 `torch==2.9.1+cpu`，然后安装其余依赖项。两个注意事项：
  - 局域网节点到 PyPI 的网络速度很慢 → 将 pip 移至 `nohup ... &` 后台作业，终止重复的 pip 进程，并轮询日志。
  - `--index-url https://download.pytorch.org/whl/cpu` 不托管 `datasets`/`pyarrow` 等 → 必须拆分为两次安装（torch 来自 PyTorch 索引，其余来自 PyPI）。

**2. 补丁 #1 — `common.py` 中的 `compute_init()`：后端选择**

原代码只有 NCCL 路径。代理添加了一个 CPU 分支：

```python
if is_ddp_requested and device_type == "cuda":
    device = torch.device("cuda", ddp_local_rank)
    torch.cuda.set_device(device)
    dist.init_process_group(backend="nccl", device_id=device)
elif is_ddp_requested and device_type == "cpu":
    device = torch.device("cpu")
    dist.init_process_group(backend="gloo")   # 基于 TCP，CPU 集合通信
dist.barrier()
```

**3. 关键架构发现 — 不需要 DDP 包装器**

代理搜索了 `DistributedDataParallel`，发现 nanochat 并未使用它。梯度同步位于自定义的 `DistMuonAdamW` 优化器内部（ZeRO-2 风格：`reduce_scatter` 梯度，分片优化器状态，`all_gather` 参数）。因此，唯一需要的“使其分布式”更改就是上面的进程组初始化——这是对 Karpathy 设计的一个真正深刻的见解。

**4. 启动脚本** — 编写了 torchrun 主节点/工作节点脚本（`--nnodes=2 --node_rank=0/1 --master_addr=<MASTER_IP> --master_port=29500`），将代码从主节点 rsync 到工作节点。

**5. 沿途扑灭的次要问题**

- rsync 带来了一个由 uv 创建的 `.venv`，它绑定到了错误的 Python 版本 → 删除并使用系统 `python3 -m venv` 重新创建。
- 工作节点无法访问 HuggingFace（中国网络） → 终止了卡住的 `dataset.py` 下载，并从主节点 rsync 了 4 个 parquet 分片（约 352 MB）。分词器目录也同步了——两个节点必须具有相同的分词器/数据。

## 三个真正的错误及其修复

**错误 1 — torchrun 参数冲突。** `--run=...` 被 torchrun 自身吞掉了。修复：使用 `--` 分隔启动器参数和脚本参数：

```bash
torchrun --nnodes=2 ... -m scripts.base_train -- --device-type cpu --run test-cpu-ddp
```

**错误 2 — 在 CPU 运行时选择了 Flash Attention。** `flash_attention.py` 中的 `_resolve_impl()` 基于 `torch.cuda.is_available()` 选择了 FA2——在主节点上为 true（它有 GPU），即使训练设备是 CPU → `flash_attn::_flash_attn_forward` 崩溃。修复：首先检查了一个环境变量逃生口：

```python
def _resolve_impl():
    if os.environ.get("NANOCHAT_FORCE_SDPA", "").lower() in ("1", "true", "yes"):
        return "sdpa"
    ...
```

然后在两个启动脚本中设置 `export NANOCHAT_FORCE_SDPA=1`。（注意：代理的第一次尝试是一个混乱的多行 `sed -i`，它不得不使用 Python 补丁脚本来清理——这是一个反复出现的模式；sed 在多行编辑上不断失败，而 Python 的 `str.replace`/正则表达式每次都拯救了它。）

**错误 3 — Gloo 未实现 `Work.get_future()`。** `DistMuonAdamW` 通过 `dist.reduce_scatter(..., async_op=True).get_future()` 重叠通信/计算。NCCL 支持 `get_future()`；Gloo 抛出 `RuntimeError: Work::getFuture not implemented`。修复：一个包装 `Work` 句柄的兼容性垫片：

```python
class _AsyncWorkWrapper:
    def __init__(self, work): self._work = work
    def wait(self):
        self._work.wait()
        return None

def _async_op(work):
    try:
        return work.get_future()      # NCCL
    except RuntimeError:
        return _AsyncWorkWrapper(work)  # Gloo 回退
```

所有 5 个 `.get_future()` 调用点都变成了 `_async_op(dist.xxx(..., async_op=True))`。

## 结果

在主节点上验证了单节点 2-rank Gloo DDP：**45 tok/s（1 rank）→ 89 tok/s（2 ranks）**——接近线性扩展，证明通过修补后的优化器的梯度同步有效。日志以将修补后的代码 rsync 到工作节点并在那里重新安装依赖项结束；实际的 2 节点运行尚未触发。

## 值得记住的要点

1. **后端 API 对等性是真正的移植成本**：NCCL→Gloo 不仅仅是字符串替换——`get_future()`、`device_id=` 和 dtype 支持都不同。
2. **硬件检测 ≠ 运行设备**：当用户明确请求 CPU 时，`torch.cuda.is_available()` 是错误的谓词；应根据实际设备进行分发。
3. **自定义优化器 DDP（类似于 Muon）** 意味着你只需接触优化器中的进程组初始化和集合通信——无需模型包装。
4. 代理最弱的工具是多行 `sed`；每个非平凡的编辑最终都变成了一个 heredoc 的 Python 脚本。值得从一开始就让你的代理更喜欢 AST/字符串替换修补而不是 sed。
