---
audio: false
generated: true
image: false
lang: zh
layout: post
title: XNU 源代码裁决
translated: true
type: note
---

现在我有了足够的XNU源代码证据。以下是裁决：

---

## XNU 源代码对"为什么32是最优选择"的裁决

### 论据1："线程驻留在内核的epoll/kqueue中"

**术语部分错误，机制正确。**

macOS 使用 kqueue，而非 epoll（那是 Linux 的机制）。但阻塞机制是真实存在的。来自 `kern_event.c:8038-8044`：

```c
kqu.kqf->kqf_state |= KQ_SLEEP;
assert_wait_deadline(&kqu.kqf->kqf_count, THREAD_ABORTSAFE,
    kectx->kec_deadline);
kqunlock(kqu);

if (__probable((flags & (KEVENT_FLAG_POLL | KEVENT_FLAG_KERNEL)) == 0)) {
    thread_block_parameter(kqueue_scan_continue, qu.kqf);
    __builtin_unreachable();
}
```

线程先调用 `assert_wait_deadline()`（将自己注册到等待队列），然后调用 `thread_block_parameter()`，后者在 `sched_prim.c:3752` 处调用 `thread_block_reason()`。这会产生一次完整的上下文切换——线程会完全从 CPU 运行队列中移除。**裁决：正确，线程在等待期间确实使用 0% CPU。**

### 论据2："没有调度，不消耗周期"

**正确。** 来自 `sched_prim.c:3788-3801`：

```c
self->continuation = continuation;
self->parameter = parameter;
// ...
new_thread = thread_select(self, processor, &reason);
thread_invoke(self, new_thread, reason);
```

线程将其 CPU 核心移交给另一个线程。这不是轮询，也不是空转。线程状态转换为 `TH_WAIT`（根据 `thread.h:512` 为 0x01），从 `TH_RUN`（0x04）中移除。**裁决：正确。**

### 论据3：在 64+ 个文件描述符时，"内核的 kqueue 会执行更多轮询工作"

**错误。这是这篇文章中最大的问题。**

kqueue 不会轮询已注册的文件描述符。它纯粹是事件驱动的。来自 `kern_event.c:7859-7868`：

```c
do {
    while ((kn = TAILQ_FIRST(queue)) != NULL) {
        error = knote_process(kn, kectx, callback);
        // ...
    }
} while (queue-- > base_queue);
```

`kqueue_process()` 仅遍历尾部队列（`kqf_queue`）中**已触发**的 knotes，而非所有已注册的 knotes。当 TCP 数据到达某个套接字时，网络栈调用 `sorwakeup()` → `sowakeup()` → `KNOTE()` → `knote_enqueue()`，仅将该特定 knote 加入队列。扫描复杂度为 O(已触发)，而非 O(已注册)。

这与 `select()` 有本质区别，后者每次都会扫描所有文件描述符。kqueue 注册了 200 个文件描述符但只有 3 个有事件，与注册了 2000 个文件描述符但只有 3 个有事件，执行的工作量完全相同。**裁决："更多轮询工作"的论点是错误的。**

### 论据4："每个 git 进程打开约 5-10 个文件描述符"以及"32 个工作进程时 200-300 个文件描述符"

**大致正确。** 来自 `syslimits.h:108` 和 `param.h:101`：

```c
#define OPEN_MAX    10240   /* 每个进程最大打开文件数 */
#define NOFILE      256     /* 每个进程默认最大打开文件数 */
```

macOS 允许每个进程最多打开 10,240 个文件描述符。每个 git 进程会打开套接字 + pack 文件 + 索引 + 松散对象，因此约 5-10 个文件描述符是合理的。以 32 个工作进程计算，约 200-300 个文件描述符是合理的，且在限制范围内。**裁决：正确。**

### 论据5："GitHub 在约 30-40 个并发 SSH 连接时进行限流"

**无法从 XNU 源代码验证**——这是 GitHub 服务端策略，而非内核行为。但这是合理的。SSH 连接有显著的建立开销（密钥交换、通道复用）。

### 论据6：数学计算与批处理计算

**原则正确，精度有误。** 理论上的最小计算是合理的（160 个仓库 / N 个工作进程 × RTT）。但实际数值（24.1 秒、9.9 秒、9.6 秒）被呈现为精确测量结果——如果这些来自实际基准测试，那没问题。如果是估算值，那么这种精度具有误导性。

---

## 总结

| 论据 | 裁决 |
| ------- | --------- |
| 驻留在 kqueue 中的线程使用 0% CPU | 正确 |
| 等待期间无调度/无周期消耗 | 正确 |
| kqueue 在更高文件描述符数量下执行更多轮询工作 | **错误**——kqueue 是事件驱动的，复杂度为 O(已触发)而非 O(文件描述符数量) |
| 每个 git 进程约 5-10 个文件描述符 | 正确 |
| 32 是最优选择 | 合理，但关于 kqueue 的推理是错误的 |

**真正使 32 成为最优选择的原因与 kqueue 开销无关。** 纯粹取决于：

1. GitHub 服务端的连接接受速率
2. 你的代理（DMIT/hysteria2）的带宽/连接池限制
3. 当网络 RTT 成为主导因素时出现的收益递减——在瓶颈容量之外增加工作进程只会产生更多处于 TCP 积压状态的连接，而不会提升吞吐量

这篇文章的 kqueue 分析是最薄弱的部分。kqueue 可以优雅地扩展到数千个文件描述符——这正是它的设计目的（与 `select()` 不同）。瓶颈在于网络路径，而非内核。
