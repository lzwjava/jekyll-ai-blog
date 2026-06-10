---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多节点CPU DDP训练成功
translated: true
type: note
---

**多节点 CPU DDP 训练成功完成！** 🎉🎉🎉

以下是完整的最终输出：

```
TRAINING RESULTS (2 nodes, CPU, Gloo backend)
==============================================

Step  | Loss       | tok/sec | Validation bpb
------|------------|---------|---------------
  0   | 10.397789  |   72    | 3.204397
  1   | 10.397395  |  105    |
  2   | 10.397194  |  115    |
  3   | 10.396683  |  117    |
  4   | 10.395638  |  117    |
  5   | 10.394717  |  125    | 3.202764
  6   | 10.393458  |  128    |
  7   | 10.392095  |  122    |
  8   | 10.390276  |  130    |
  9   | 10.388018  |  134    | 3.197027

Checkpoint saved: model_000010.pt (both ranks)
```

模型甚至生成了文本样本（仅10步后内容无意义，但证明了端到端管道）：

```
The capital of France is a party may come a party may come...
The chemical symbol of gold is a party may come...
```

---

## 我们所做的一切总结

**应用了4个代码补丁：**

1. `common.py` — 在 `compute_init()` 中添加了用于 CPU DDP 的 Gloo 后端
2. `flash_attention.py` — 添加了 `NANOCHAT_FORCE_SDPA=1` 环境变量（FA 仅支持 CUDA）
3. `optim.py` — 添加了 `_AsyncWorkWrapper` 和 `_async_op()` 以兼容 Gloo（Gloo 不支持 `Work.get_future()`）
4. `dataset.py` — 添加了 `NANOCHAT_DATA_DIR` 环境变量，用于共享数据子集

**3项基础设施修复：**

1. 在 1.36 上打开了 UFW 端口 29500 并添加了局域网规则
2. 设置 `GLOO_SOCKET_IFNAME` 以绑定到特定网络接口（避免通过 Tailscale 产生的 IPv4/IPv6 不匹配）
3. 设置 `NANOCHAT_DTYPE=float32`（bf16 能从 CUDA 自动检测，但在 CPU 上极慢）

**关键经验：**

- Gloo（CPU）vs NCCL（GPU）——不同的后端，不同的 API 支持
- CPU 上的 `torch.compile` 首次调用很慢（约30秒），但后续稳定（约16秒）
- CPU DDP 吞吐量随世界大小扩展（72→134 tok/sec）
- bf16 自动检测会检查 `torch.cuda.is_available()` 而非实际设备——必须在 CPU 上覆盖该设置
