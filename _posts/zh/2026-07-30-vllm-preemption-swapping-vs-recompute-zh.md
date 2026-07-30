---
audio: false
generated: true
image: false
lang: zh
layout: post
title: vLLM抢占：交换 vs 重计算
translated: true
type: note
---

问题：vLLM 调度器中的 preemption 是什么意思？

答案：当同时运行的序列过多导致 KV 缓存块耗尽时，vLLM 必须将某个序列从运行批次中踢出，以释放 GPU 内存供其他序列使用。这就是 preemption（抢占）——它是调度器应对无法预先知道一个生成过程需要多少 token 这一事实的机制，因此仅靠准入控制无法防止资源超额分配。

两种恢复模式，通过 `--preemption-mode` 设置：

```python
# vllm/core/scheduler.py (V0) — 简化逻辑
class PreemptionMode(Enum):
    SWAP = "swap"
    RECOMPUTE = "recompute"

def _preempt(self, seq_group, blocks_to_swap_out):
    if self.user_specified_preemption_mode is None:
        # beam search / 多序列组无法干净地重做 prefill
        # -> 使用 swap；否则 recompute 更便宜
        preemption_mode = (PreemptionMode.RECOMPUTE
                            if seq_group.get_max_num_running_seqs() == 1
                            else PreemptionMode.SWAP)
    else:
        preemption_mode = self.user_specified_preemption_mode

    if preemption_mode == PreemptionMode.RECOMPUTE:
        self._preempt_by_recompute(seq_group)
    else:
        self._preempt_by_swap(seq_group, blocks_to_swap_out)
```

- **Recompute**：完全丢弃被牺牲序列的 KV 块，将该序列放回 WAITING 队列的前端，当它被重新接纳时，从头开始重新运行完整的 prefill（提示词 + 迄今为止生成的所有内容）。PCIe 开销为零，但对于长上下文，需要再次支付近似二次的 prefill 计算成本。Recompute：被丢弃的序列在重新接纳时从头开始重新运行 prefill，PCIe 带宽成本为零，但恢复时 GPU 计算成本更高。
- **Swap**：将被牺牲序列的物理 KV 块序列化到 CPU DRAM，然后当它被重新调度时通过 PCIe DMA 传回。在 Llama-3-70B 上通过 PCIe 4.0 x16 链路恢复长上下文序列可能需要数百毫秒。

默认使用哪一种取决于版本：在 vLLM V1 中，默认抢占模式是 RECOMPUTE 而非 SWAP，因为在 V1 架构中重算开销更低。V0 默认对单序列组使用重算，但在 beam search / 多序列组（重算不适用）时回退到 swap。如果未指定，默认使用重算，因其开销低于 swap——但当序列组包含多个序列（例如 beam search）时，不支持重算，因此改用 swap。

哪个序列会被选为牺牲者：vLLM 通常采用 LIFO 策略，选择最近调度的请求作为牺牲者，被抢占的请求被追加到 WAITING 队列的前端而非丢弃——因此它不会失去排队位置，只是重新付出 prefill 成本。

触发时，日志中会出现如下信息：
```
WARNING scheduler.py:1057 Sequence group 0 is preempted by PreemptionMode.RECOMPUTE
mode because there is not enough KV cache space.
```
这可能影响端到端性能；增加 `gpu_memory_utilization` 或 `tensor_parallel_size` 可提供更多 KV 缓存内存。通过 Prometheus 指标 `vllm:num_preemptions_total` 进行跟踪——如果在额定负载下该指标稳步增长，请降低 `--max-model-len`、提高 `--gpu-memory-utilization` 或增加容量。

对你的实际部署来说：如果你在 MI300X 上服务长上下文请求并看到抢占抖动，首先检查 `gpu_memory_utilization`（提高它），然后考虑 `--enable-chunked-prefill`（优先处理解码而非新的 prefill，以免正在运行的序列被饿死）。如果你遇到对抗性/突发性流量混合短请求和长请求，那正是那篇 DoS 论文中描述的攻击模式——攻击者不断推动内存越过阈值，迫使受害者陷入昂贵的重算抖动。

参考资料：
- [vLLM Scheduler API docs](https://docs.vllm.ai/en/v0.10.1/api/vllm/core/scheduler.html)
- [Optimization and Tuning — vLLM](https://docs.vllm.ai/en/stable/configuration/optimization/)
- [vLLM Explained: PagedAttention and Continuous Batching](https://www.runpod.io/articles/guides/vllm-pagedattention-continuous-batching)
- [Rethinking Latency DoS: Attacking the LLM Serving Framework](https://arxiv.org/pdf/2602.07878)