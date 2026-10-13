---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 仅限 Python 和 Java 的快速排序 Runnable
translated: true
type: note
---

目前只有 Python 和 Java 版本可以运行——**`src/` 中没有 quicksort**，所以无法通过 `cargo run` 调用任何东西（README 声称可以，但已过时）。

## 当前可用的命令

**Python：**

```bash
cd /home/lzw/projects/ll
python3 quicksort.py
```

输出类似于：

```
Before: [...] 
After:  [...] 
Sorted 10000 numbers in X.XXX ms
```

**Java：**

```bash
javac Quicksort.java
java Quicksort
```

（只需要 PATH 中有 `javac`/`java`；无需构建工具。）

**Rust：**不可用——`main.rs` 中没有接入 `bench`/`quicksort` 子命令。

## 想要一个 Rust 子命令吗？

我可以添加一个，让三者运行相同的基准测试：

```bash
cargo run --release -- bench   # Rust quicksort：对 10,000 个整数排序
```

实现方式：在 `main.rs` 的 `match` 中加入一个 `bench` 分支，添加一个 `quicksort` 模块，使用相同的 Lomuto 分区和 10,000 个元素的输入，并用 `std::time::Instant` 计时——让这个三方对比真正是同类比较（我也会把 README 的相关部分改到一致）。你说一声，我就加上。
