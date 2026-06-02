---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust在快速排序中性能超越Python
translated: true
type: note
---

**结果：Rust ~0.75毫秒 vs Python ~7.9毫秒 —— 约快10倍。**

---

以下是帖子内容：

---

**Rust与Python中的快速排序：对10,000个数字进行排序**

我用Rust和Python分别从头实现了相同的快速排序算法——都使用完全相同的Lomuto分区逻辑——并对10,000个随机整数进行了计时测试。

**结果：**

- Rust（发布版本）：**~0.75毫秒**
- Python：**~7.9毫秒**

对于相同的算法、相同的逻辑、没有使用任何技巧，Rust大约快了**10倍**。

代码几乎是1:1直接翻译的。Python的元组交换（`a, b = b, a`）可以说比Rust的`arr.swap(i, j)`更优雅，但Rust编译成了原生机器码，而Python每一步都需要经过解释器并承担动态类型化的开销。

有趣的是，这里的差距“仅仅”是10倍。Python虽然名声不佳，但对于中等数据规模的算法任务来说，其表现并非灾难性的。如果将数据量推到100万，或者在热循环中运行此算法，差距会迅速拉大。

真正的启示是：在较小规模下，算法比编程语言更重要。两种实现都具有O(n log n)的平均时间复杂度。但当你需要争分夺秒时，Rust的零成本抽象就能展现出威力。

代码：`src/main.rs`（Rust）和`quicksort.py`（Python）——相同的算法，差异巨大的运行时间。

---

是否需要我提交并推送此更改？
