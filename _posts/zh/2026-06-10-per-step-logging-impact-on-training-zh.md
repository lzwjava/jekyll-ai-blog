---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 每步日志对训练的影响
translated: true
type: note
---

**问题：** 在 nanochat 中，每步的日志打印（`step ... | loss ... | tok/sec ...`）会拖慢或影响训练吗？

**回答：**

简短版：它完全不会影响训练动态（损失、梯度、收敛都不受影响——日志是只读的），且其吞吐量开销约为每步 0.01–0.1%。在你 `dt ≈ 1170ms` 的场景下，这可以忽略不计。

下面根据 `scripts/base_train.py` 的代码，拆解一下这一行日志的实际开销：

**1. `print` 本身：微秒级。** 向缓冲 stdout 写入约 150 个字符大约需要 10–50µs。相对于 1170ms 的步长，这只有 0.003%。（注意：如果 stdout 是一个阻塞的慢速管道——例如通过 SSH 连接到一个延迟很高的终端，或者用 `tee` 写入 NFS——print 可能会被阻塞。若担心这一点，可将输出重定向到本地文件：`python -m scripts.base_train > train.log 2>&1`。）

**2. `loss.item()` / EMA 记账：每步一次 GPU→CPU 同步。** 这是唯一“真正”的开销。`.item()` 强制 CPU 等待 GPU 完成该步之后才能读取标量值。但 nanochat 本身就有意这样做——它定义了 `synchronize = torch.cuda.synchronize` 并在每一步进行同步，以便获得精确的 `dt` 用于计时/MFU 计算。同步本身的开销并不大（~µs），真正的代价是失去了将 CPU 工作（如下一批数据准备、优化器宿主端逻辑）与 GPU 重叠的机会。在使用预取数据加载器和 1.17s 步长的情况下，这种重叠损失远小于每步 1ms。

**3. wandb 日志记录：** 缓冲且异步，可忽略。使用 `--run dummy` 时，它实际上是一个 `DummyWandb()` 空操作。

真正消耗墙钟时间（但同样不影响训练动态）的是那些周期性的重量级操作，而非每步的打印：每 250 步的验证 bpb 评估、每 2000 步的 CORE 指标、每 2000 步的采样以及检查点保存。这些操作每次会暂停训练数秒到数分钟。如果你想在自己的硬件上运行更快，应该从这里着手削减（`--eval-every -1 --core-metric-every -1 --sample-every -1`），而不是日志打印。

如果你想通过实验验证，可以将日志进行门控并做 A/B 测试：

```python
# 在训练循环中
LOG_EVERY = 10
if step % LOG_EVERY == 0 and master_process:
    lossf = smooth_train_loss  # 已经计算好
    print0(f"step {step:05d} | loss: {lossf:.6f} | dt: {dt*1000:.2f}ms | tok/sec: {tok_per_sec:,}")
```

分别以 `LOG_EVERY=1` 和 `LOG_EVERY=10000` 运行 200 步，比较平均 `dt`。你会发现它们在统计上没有显著差异。（如果你修改循环，有一点需要*避免*：在梯度累积的微步骤循环内部对中间张量调用 `.item()`——这会在每个微批次中插入一次同步，当步长较短时确实会带来性能损失。）

关于你的日志，附带说明一下：`bf16_mfu: 0.00` 意味着 `get_peak_flops()` 没有识别出你的 GPU 名称，因此 `gpu_peak_flops` 会回退到一个使 MFU 计算归零的值——在 CPU/MPS 上它被显式设置为 `float('inf')`，因为“MFU 无意义”，未知的 CUDA 设备也会进入类似路径。查找表是为 H100/A100 类名称调优的；在你的 MI300X（ROCm 报告了不同的设备名称字符串）或 RTX 4070 上，你需要在 `nanochat/common.py:get_peak_flops` 中添加一个条目，填入你显卡的峰值 BF16 FLOPS（MI300X：约 1307 TFLOPS 密集 BF16；RTX 4070：约 29 TFLOPS 非稀疏 BF16）才能得到真实的 MFU 数值。你日志中的 `pq`/`rg` 字段（来自数据加载器的预取队列 / 不规则批次统计）在当前主分支的格式字符串中并不存在，所以你是在一个 fork 或不同的 commit 上运行——不过结论同样适用。

**参考：**

- [nanochat scripts/base_train.py](https://github.com/karpathy/nanochat/blob/master/scripts/base_train.py)
- [nanochat run1000.sh — 8×H100 上的参考步长时间](https://github.com/karpathy/nanochat/blob/master/run1000.sh)
- [DeepWiki: nanochat base pretraining — MFU 公式和日志指标](https://deepwiki.com/karpathy/nanochat/3-base-model-pretraining)
