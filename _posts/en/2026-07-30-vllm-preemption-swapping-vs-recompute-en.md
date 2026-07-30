---
audio: false
generated: true
image: false
lang: en
layout: post
title: "vLLM Preemption: Swapping vs Recompute"
translated: false
type: note
---

Question: What does preemption mean in vLLM's scheduler?

Answer: When KV cache blocks run out because too many sequences are running concurrently, vLLM has to kick a sequence out of the running batch to free GPU memory for others. That's preemption — it's the scheduler's answer to the fact that you can't know upfront how many tokens a generation will need, so admission control alone can't prevent overcommitment.

Two recovery modes, set via `--preemption-mode`:

```python
# vllm/core/scheduler.py (V0) — simplified logic
class PreemptionMode(Enum):
    SWAP = "swap"
    RECOMPUTE = "recompute"

def _preempt(self, seq_group, blocks_to_swap_out):
    if self.user_specified_preemption_mode is None:
        # beam search / multi-seq groups can't just redo prefill
        # cleanly -> use swap; otherwise recompute is cheaper
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

- **Recompute**: drop the victim's KV blocks entirely, put the sequence back at the front of the WAITING queue, and when it's re-admitted it re-runs the full prefill (prompt + everything generated so far) from scratch. Zero PCIe cost, but you pay quadratic-ish prefill compute again for a long context. Recompute: dropped sequences rerun prefill from scratch when re-admitted, zero PCIe bandwidth cost but higher GPU compute on restore.
- **Swap**: serialize the victim's physical KV blocks out to CPU DRAM, then DMA them back over PCIe when it's rescheduled. Restoring a long-context sequence on Llama-3-70B over a PCIe 4.0 x16 link can take hundreds of milliseconds.

Which one is default depends on version: In vLLM V1, the default preemption mode is RECOMPUTE rather than SWAP, since recomputation has lower overhead in the V1 architecture. V0 defaulted to recompute for single-sequence groups but fell back to swap for beam search / multi-seq groups where recompute isn't valid. If not specified, recomputation is used by default since it incurs lower overhead than swapping — but when the sequence group has multiple sequences (e.g., beam search), recomputation is not supported, so swapping is used instead.

Which sequence gets picked as victim: vLLM typically enforces a LIFO policy and selects the most recently scheduled request as the victim, and the preempted request is prepended to the front of the WAITING queue rather than discarded — so it doesn't lose its place in line, just re-pays prefill cost.

When it fires, you'll see this in logs:
```
WARNING scheduler.py:1057 Sequence group 0 is preempted by PreemptionMode.RECOMPUTE
mode because there is not enough KV cache space.
```
This can affect end-to-end performance; increasing gpu_memory_utilization or tensor_parallel_size provides more KV cache memory. Track it via the Prometheus vllm:num_preemptions_total counter — if it grows steadily under nominal load, reduce --max-model-len, raise --gpu-memory-utilization, or add capacity.

Practically for your setup: if you're serving long-context requests on MI300X and see preemption thrashing, first check `gpu_memory_utilization` (raise it), then consider `--enable-chunked-prefill` (prioritizes decode over new prefill so running sequences aren't starved), and if you have adversarial/bursty traffic mixing short+long requests, that's exactly the DoS pattern in that DoS paper — attacker keeps nudging memory over the threshold to force expensive recompute thrashing on victims.

References:
- [vLLM Scheduler API docs](https://docs.vllm.ai/en/v0.10.1/api/vllm/core/scheduler.html)
- [Optimization and Tuning — vLLM](https://docs.vllm.ai/en/stable/configuration/optimization/)
- [vLLM Explained: PagedAttention and Continuous Batching](https://www.runpod.io/articles/guides/vllm-pagedattention-continuous-batching)
- [Rethinking Latency DoS: Attacking the LLM Serving Framework](https://arxiv.org/pdf/2602.07878)