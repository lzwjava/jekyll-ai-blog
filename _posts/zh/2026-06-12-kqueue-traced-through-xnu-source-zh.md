---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过XNU源码追踪Kqueue
translated: true
type: note
---

以下是通过XNU源码对kqueue的追踪：

## kqueue是什么

kqueue 是 macOS/BSD 的**事件通知机制**——一个内核子系统，让进程能够说“当这个文件描述符/进程/定时器/Mach端口上发生某些事件时叫醒我”，而无需轮询。

### 核心数据结构

**1. kqueue 本身**（`bsd/sys/eventvar.h:156`）：

```c
struct kqueue {
    lck_spin_t      kq_lock;      // 保护所有字段
    kq_state_t      kq_state;     // KQ_WORKQ | KQ_WORKLOOP | flags
    uint16_t        kq_level;     // 嵌套层级
    uint32_t        kq_count;     // 已触发（已排队）的事件数量
    struct proc    *kq_p;         // 拥有进程
};
```

`kq_count` 字段是关键——它只跟踪**已触发**的事件，而不是所有注册的事件。这正是 kqueue 的时间复杂度为 O(已触发) 而非 O(已注册) 的原因。

**2. kqfile**——文件描述符形式（`eventvar.h:172`）：

```c
struct kqfile {
    struct kqueue   kqf_kqueue;     // 核心 kqueue
    struct kqtailq  kqf_queue;      // 已触发的 knotes 队列
    struct kqtailq  kqf_suppressed; // 抑制队列
    struct selinfo  kqf_sel;        // 用于 select() 兼容
};
```

**3. knote**——事件注册（`event_private.h:428`）：

```c
struct knote {
    TAILQ_ENTRY(knote)  kn_tqe;        // 在 kqueue 的触发队列中的链接
    SLIST_ENTRY(knote)  kn_link;        // 用于 fd 搜索列表的链接
    SLIST_ENTRY(knote)  kn_selnext;     // klist 元素链（位于被监视对象上）
    kn_status_t         kn_status : 12; // KN_ACTIVE, KN_QUEUED, KN_DISABLED 等
    // ...
    struct kevent_internal_s kn_kevent;  // filter, ident, flags, data, udata
};
```

knote 是 kqueue 和被监视对象之间的**桥梁**。它同时存在于两个列表中：

- `kn_selnext`——链接到被监视对象的 `klist`（例如，套接字的 `sb_sel.si_note`）
- `kn_tqe`——触发时链接到 kqueue 的 `kqf_queue`

**4. filterops**——事件源抽象（`event_private.h:727`）：

```c
struct filterops {
    bool f_isfd;                          // 如果 ident 是文件描述符则为 true
    int  (*f_attach)(struct knote *kn, ...);   // 注册关注
    void (*f_detach)(struct knote *kn);        // 取消注册
    int  (*f_event)(struct knote *kn, long hint);  // 事件是否活跃？
    int  (*f_process)(struct knote *kn, ...);  // 快照事件数据
};
```

每个事件源（套接字、vnode、进程、定时器、Mach端口）都提供自己的 filterops。对于套接字，它们在 `uipc_socket.c` 中分别是 `filt_sockattach`、`filt_sockev`、`filt_sockprocess`。

### 生命周期

**步骤1：创建 kqueue**——`kqueue()` 系统调用（`kern_event.c:3092`）：

```c
kqueue(struct proc *p, ...) {
    return kqueue_internal(p, NULL, NULL, retval);
}
```

→ `kqueue_internal()` → `kqueue_alloc()` → 返回一个文件描述符。

**步骤2：注册关注**——带 `EV_ADD` 标志的 `kevent()`（`kern_event.c:4006`）：

```c
kevent_register(struct kqueue *kq, struct kevent_qos_s *kev, ...) {
    // 查找或创建此 filter+ident 的 knote
    kn = kq_find_knote_and_kq_lock(kq, kev, ...);
    if (kn == NULL && (kev->flags & EV_ADD)) {
        // 分配新的 knote，调用 filter 的 f_attach()
        kn = knote_alloc(kq);
        result = filter_call(fops, f_attach(kn, kev));
        // 将 knote 链接到被监视对象的 klist 上
        knote_attach(&fdp->fd_knlist[fd], kn);
    }
}
```

这会创建一个 knote，并将其同时链接到 kqueue 和文件描述符的 knote 列表。

**步骤3：等待事件**——不带变更的 `kevent()`（`kern_event.c:8017`）：

```c
kqueue_scan(kqueue_t kqu, int flags, ...) {
    for (;;) {
        kqlock(kqu);
        error = kqueue_process(kqu, flags, kectx, callback);  // 处理触发的事件
        if (error || (flags & KEVENT_FLAG_IMMEDIATE)) {
            return error;
        }
        // 尚无事件——阻塞线程
        kqu.kqf->kqf_state |= KQ_SLEEP;
        assert_wait_deadline(&kqu.kqf->kqf_count, THREAD_ABORTSAFE, deadline);
        kqunlock(kqu);
        thread_block_parameter(kqueue_scan_continue, kqu.kqf);  // 上下文切换走
    }
}
```

线程被从 CPU 运行队列中移除，CPU 占用为零。

**步骤4：事件触发**——例如，TCP 数据到达套接字：

网络栈调用 `sorwakeup()` → `sowakeup()`（`uipc_socket2.c:625`）：

```c
sowakeup(struct socket *so, struct sockbuf *sb, ...) {
    selwakeup(&sb->sb_sel);           // 唤醒 select() 等待者
    sbwakeup(sb);                     // 唤醒 msleep() 等待者
    if (sb->sb_flags & SB_KNOTE) {
        KNOTE(&sb->sb_sel.si_note, SO_FILT_HINT_LOCKED);  // 触发 kqueue knotes
    }
}
```

`KNOTE()` 展开为 `knote()`（`kern_event.c:6590`）：

```c
knote(struct klist *list, long hint, ...) {
    SLIST_FOREACH_SAFE(kn, list, kn_selnext, tmp_kn) {
        knote_post(kn, hint);  // 检查 filter，如果就绪则激活
    }
}
```

`knote_post()` → 调用 filter 的 `f_event()` → 如果 `FILTER_ACTIVE` → `knote_activate()` → `knote_enqueue()`：

```c
knote_enqueue(kqueue_t kqu, struct knote *kn) {
    struct kqtailq *queue = knote_get_tailq(kqu, kn);
    TAILQ_INSERT_TAIL(queue, kn, kn_tqe);  // 加入触发队列
    kn->kn_status |= KN_QUEUED;
    kqu.kq->kq_count++;                    // 增加触发计数
    // 唤醒阻塞在 kqueue_scan() 中的线程
    kqfile_wakeup(kqu.kqf, 0, THREAD_AWAKENED);
}
```

**步骤5：线程唤醒**——`kqueue_scan` 继续执行，`kqueue_process()` 仅遍历触发队列：

```c
do {
    while ((kn = TAILQ_FIRST(queue)) != NULL) {
        knote_process(kn, kectx, callback);  // 调用 filter 的 f_process()，复制到用户空间
    }
} while (queue-- > base_queue);
```

### 存在哪些事件源

来自 `bsd/sys/event.h:70-84`：

```c
#define EVFILT_READ      (-1)   // 文件描述符可读（套接字有数据，文件有字节）
#define EVFILT_WRITE     (-2)   // 文件描述符可写（套接字缓冲区有空间）
#define EVFILT_AIO       (-3)   // 异步 I/O 完成
#define EVFILT_VNODE     (-4)   // 文件改变（写入、删除、重命名、属性）
#define EVFILT_PROC      (-5)   // 进程状态变化（fork、exec、exit、signal）
#define EVFILT_SIGNAL    (-6)   // 信号送达
#define EVFILT_TIMER     (-7)   // 周期性/一次性定时器
#define EVFILT_MACHPORT  (-8)   // Mach 端口消息到达
#define EVFILT_FS        (-9)   // 文件系统事件
#define EVFILT_USER      (-10)  // 用户触发的事件（手动唤醒）
#define EVFILT_VM        (-12)  // 虚拟内存事件
#define EVFILT_EXCEPT    (-15)  // 异常事件
```

### 三种 kqueue 变体

XNU 有三种 kqueue 类型：

1. **kqfile**——经典的 `kqueue()` 系统调用结果。一个队列，与 `kevent()`/`select()` 配合使用。（`eventvar.h:172`）

2. **kqworkq**——用于 GCD/libdispatch 的私有 per-process kqueue。具有 per-QoS 桶（`KQWQ_NBUCKETS` = 6）。事件按优先级隔离，因此高 QoS 事件优先得到服务。（`eventvar.h:211`）

3. **kqworkloop**——现代演进。支持绑定线程（线程永久驻留在 workloop 上）、线程移交和 QoS 感知处理。用于 Swift 并发和现代 GCD。具有 `KQWL_NBUCKETS` = 5 个优先级级别。（`eventvar.h:234+`）

### kqueue vs select/poll

关键区别：`select()` 每次都会扫描**所有**注册的文件描述符来检查就绪状态。而 kqueue 只处理被事件源**显式触发**的 knotes。被监视对象（套接字、vnode 等）在事件发生时调用 `KNOTE()`——kqueue 从不轮询。

这就是为什么 kqueue 能高效扩展到数千个文件描述符：代价与实际触发的事件数量成正比，而非与被监视的事物数量成正比。