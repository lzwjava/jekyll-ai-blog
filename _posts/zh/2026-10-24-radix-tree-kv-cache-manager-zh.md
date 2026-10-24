---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基数树KV缓存管理器
translated: true
type: note
---

这是一个**基于 radix tree（前缀树）的 KV 缓存管理器**——它将 KV 条目缓存到*共享 token 前缀*下，这样重复的提示前缀就可以被重用而无需重新计算。以下是它的完整工作原理：

## 树结构（`RadixTreeNode`）

每个节点存储：
- `key` / `value`：`(page_size, num_kv_heads, head_dim)` 块——一个 token 序列及其支持的 KV 索引
- `children`：从 `key_fn(key)` 指纹映射到子节点的字典
- `ref_count`：引用该节点的活跃请求数（refcount > 0 = **受保护**，不可被驱逐）
- `timestamp`：最后访问时间（用于通过堆实现 LRU 驱逐）

节点形成一棵树，其中**每个祖先的 key 都是其后代 key 的前缀**。根节点是一个 dummy 节点，`ref_count = 1`（始终受保护，从不被驱逐）。

路由 key `key_fn` 是一页中的第一个 token：如果 `page_size == 1` 则为 `x[0].item()`，否则为 `tuple(x[:page_size].tolist())`。这意味着每个节点的 key 正好是一页（或分裂后对齐的余数）。

## 树遍历（`_tree_walk`）

```
while prefix_len < seq_len:
    child = node.children[key_fn(input_ids[prefix_len:])]   # 按下一页的第一个 token 下降
    match_len = align_down(fast_compare_key(child.key, rest), page_size)  # 计算匹配的 token 数
    prefix_len += match_len
    if match_len != node.length:      # 部分页面匹配 → 分裂节点
        node = node.split_at(match_len)
        return node, prefix_len
    node.timestamp = tic              # LRU 触达
```

`fast_compare_key`（`kernel/csrc/src/radix.cpp` 中的一个 TVM/CUDA 内核）比较节点的 key 张量与输入，并返回第一个不同的位置。

## 分裂（`split_at`）

当仅匹配一个节点页面的一部分时，该节点会被原地分裂：一个新的父节点占用前 `pos` 个 token 并继承 refcount，而原节点保留剩余部分作为其子节点。这使得可以缓存/重用现有节点的*部分*前缀，而不破坏树的不变量。

## 公开 API

- **`match_prefix(input_ids)`** → 遍历树，返回一个包裹最深匹配节点的 `RadixCacheHandle`。该 handle 的 `get_matched_indices()` 向上回溯到根节点，拼接 `node.value` 块——即整个匹配前缀的物理 KV 索引。
- **`insert_prefix(input_ids, indices)`** → 将两者对齐到 `page_size`，遍历树，如果新前缀不完全存在，则为 `(prefix_len, insert_len]` 尾部创建一个新节点，并将其挂在匹配节点下。返回 `InsertResult(cached_len, handle)`。
- **`lock_handle(handle, unlock)`** → 向上遍历节点直到根，递增/递减 `ref_count`，并在 `evictable_size` / `protected_size` 之间移动字节。在使用匹配值之前必须锁定 handle，否则其他请求的 `evict` 可能会释放它们。
- **`evict(size)`** → 将所有 `ref_count == 0` 的叶节点收集到按 `timestamp`（LRU）排序的最小堆中，弹出叶节点，将其从父节点的 `children` 中移除，并推入新成为孤儿的叶节点。返回拼接后的 `value` 张量（被释放的 KV 槽）。根节点从不被收集。

## 追踪

`size_info` 报告 `evictable_size`（refcount 为 0 的节点中的字节数）与 `protected_size`（活跃引用的节点中的字节数），`RadixTreeNode` 上的 `counter` 为每个节点赋予一个唯一的 `uuid`。

**简而言之**：请求重用共享前缀的缓存注意力 KV（匹配 + 锁定），新的尾部被插入为节点，当 KV 池不足时，最久未使用的无引用叶节点被驱逐，分裂使得细粒度重用成为可能。这是标准的 SGLang radix 缓存设计（使用 GPU 端 key 比较和页级别粒度）。