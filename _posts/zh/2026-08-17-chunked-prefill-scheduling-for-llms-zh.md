---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向大语言模型的分块预填充调度
translated: true
type: note
---

此文件为 `mini-sglang` 实现了 **prefill 调度**——即 LLM 推理中"处理提示词"的阶段，该阶段必须先于逐 token 的 decode 进行。它是 SGLang 调度器的精简版本，核心是 **分块 prefill**：较长的提示词会被切成适合当前 token 预算的块，未完成的请求会在后续调度轮次中恢复。

## 两个类

### 1. `ChunkedReq`（第 24–30 行）
一个 `Req` 子类，用于禁用采样/解码：

- `append_host` 会抛出异常——分块请求尚未完成其提示词，因此绝不能进行采样。
- `can_decode` 返回 `False`——解码管理器的 `filter_reqs` 会跳过它，因此部分 prefill 的请求会留在 prefill 流程中。

### 2. `PrefillAdder`（第 33–97 行）——准入控制
核心逻辑：尝试将一个待处理请求适配到当前预算中。

**`_try_allocate_one`**（第 41–59 行）在提交 *之前* 预留资源：
1. 如果表管理器（请求槽位）已满，则退出。
2. 向缓存管理器查询 **前缀匹配**（`match_req` → 前缀缓存：如果提示词的一部分已在 KV 缓存中，则重复使用；`cached_len` 是已缓存的 token 数）。
3. 估算所需的总 token 数：`extend_len + output_len`（要 prefill 的新 token + 响应将消耗的 token），并对照可用缓存进行检查——**考虑了 `reserved_size`**（正在进行的 decode token，见下文）。
4. `lock` 缓存句柄，重新检查（竞态安全性），并分配一个表槽位。
5. 如果有缓存前缀，将缓存的 token ID 和匹配的页表条目复制到新槽位中——这将预先存在的 KV 页链接到此请求的页表。

**`_add_one_req`**（第 63–84 行）执行实际的添加操作：
- 计算块大小：`min(token_budget, remain_len)`。如果整个剩余的提示词放不下，则将请求包装在 `ChunkedReq` 中。
- 减少预算，并 **将 `reserved_size` 增加** 剩余的提示词 + 输出 token，以便此批次中的后续请求不会过度承诺。
- 仅将块中的 token ID 复制到 token 池中（页面稍后由调度器分配）。
- 返回一个带有部分提示词（`input_ids[:cached_len + chunk_size]`）及其资源句柄的 `Req`。

**`try_add_one`**（第 86–97 行）是入口点，有两条路径：
- **恢复路径：** 如果待处理请求已有 `chunked_req`，则完全跳过分配——复用其缓存句柄/表槽位，只需 prefill 下一个块。这就是使分块 prefill 易于继续的原因。
- **新路径：** 分配新资源，然后添加。

当预算不足时返回 `None`——由于待处理列表是 FIFO 排序的，调用者将 `None` 视为"停止，没有更多可容纳的。"

### 3. `PrefillManager`（第 100–141 行）——调度器

**`add_one_req`** —— 新的用户请求成为队列中的 `PendingReq`（提示词 token + 采样参数）。

**`schedule_next_batch`**（第 108–134 行）——构建下一个 prefill 批次：
- 创建一个 `adder`，其 `reserved_size` 以 `decode_manager.inflight_tokens` 为种子——即，解码请求当前正在生成的 token 被视为已消耗的缓存，因此 prefill 永远不会从正在进行的解码中窃取页面。这是两个阶段之间关键的内存协调点。
- 迭代待处理列表，贪心地添加请求，直到预算耗尽（在 `None` 时 `break`）。
- 保持顺序：`pending_list = chunked_list + self.pending_list[len(reqs):]`——可恢复的分块请求保持在前面（它们将在下一轮首先被调度），后跟未适配的请求。
- 返回 `Batch(phase="prefill")`，如果无法调度任何内容，则返回 `None`。

**`abort_req`** —— 从队列中移除请求并返回其进行中的 `ChunkedReq`（以便调用者释放其资源）。

**`runnable`** —— 队列是否非空（由主调度循环用于决定是否需要 prefill 步骤）。

## 如何协同工作

```
UserMsg → PrefillManager.add_one_req → PendingReq 队列
              │
              └─ schedule_next_batch (prefill_budget tokens)
                   ├─ DecodeManager.inflight_tokens  → 保留缓存（不从解码中窃取）
                   ├─ CacheManager.match_req         → 前缀缓存复用
                   ├─ 如果 prompt > budget 则分块    → ChunkedReq，将 PendingReq 保持在队列头部
                   └─ Batch(phase="prefill") → 调度器分配页面，运行模型
```

简而言之：此文件是 **prefill 阶段的资源准入和批处理逻辑**——它平衡提示词处理与解码的缓存需求，复用缓存前缀，并透明地将长提示词分块到多个调度轮次中。