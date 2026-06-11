---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rust Word2vec实现细节
translated: true
type: note
---

以下是完整的技术解析：

---

**架构：Skip-gram + CBOW 与负采样**

忠实移植了 Mikolov 原始 C 语言版 word2vec。两种模型架构（Skip-gram 预测中心词→上下文，CBOW 平均上下文→中心词）均使用负采样训练（每对正样本使用 N 个噪声样本，sigmoid 交叉熵损失）。不使用 softmax 或层次 softmax——仅采用后来成为主流的 SGNS 变体。

**词汇构建器**

读取语料 → 统计词频（小写化）→ 按 `min_count` 过滤 → 按频率降序排序 → 分配索引。存储为并行的 `Vec<String>`、`Vec<u64>` 计数和 `HashMap<String, usize>` 用于查找。排序顺序对负采样表至关重要。

**负采样表**

预计算包含 1 亿条目的表，其中条目 `i` 映射到与 `count^0.75` 成正比的词索引。通过累积分布构建：对每个词计算 `count^0.75 / sum`，遍历表填充条目。`^0.75` 平滑（相比原始频率）可防止常见词主导负样本——与原始方案相同。通过 `(rng >> 16) % TABLE_SIZE` 索引（LCG 的高位比低位分布更均匀，匹配原始 C 代码的位移操作）。

**Sigmoid 近似**

预计算包含 1000 条目的查找表，覆盖 `[-MAX_EXP, MAX_EXP]`。`sigmoid(x) = table[((x + 6.0) / 12.0) * 1000]`。避免在热循环中调用 `exp()`——原始代码同样如此。

**高频词子采样**

原始公式：`ran = (sqrt(f/t) + 1) * (t/f)`，其中 `f = count/total`，`t = threshold`。如果 `ran < random_uniform`，则丢弃该词。这会降低高频词（如 "the", "a"）的采样率，同时保留罕见词。匹配原始 C 代码中的精确公式，而非教程中常引用的简化版 `1 - sqrt(t/f)`。

**动态窗口缩减**

每个词位置：`b = rng % window`，上下文范围为 `[pos - window + b, pos + window - b]`。因此每侧有效窗口为 `window - b`（均匀随机，范围 1 到 `window`）。这为每个词提供了更多样的上下文大小——原始代码正是如此，而非固定窗口。

**LCG 伪随机数生成器**

`next_random = next_random * 25214903917 + 11` — 采用 Park-Miller LCG，与原始 C 代码完全一致。线程局部状态（无共享 RNG，无锁）。相同的种子序列意味着单线程模式下结果可重现。

**单线程训练路径**

语料读入内存为 `&[u8]`，按 `\n` 和空格分割。每个词小写化后通过 HashMap 查找、子采样，累积到句子缓冲区（最多 1000 个词）。缓冲区满时对其进行训练。学习率根据 `word_count / total_target` 从 `lr0` 线性衰减至 `lr0 * 0.0001`。循环结构与原始代码完全相同。

**多线程训练：TrainPtrs**

核心 Rust 难点。`std::thread::scope::spawn` 要求 `F: Send`。原始指针（`*mut f32`）是 `!Send`。尝试过的方案：

1. `SendPtr<T>(*mut T)` + `unsafe impl Send` — 结构体是 Send，但 Rust 闭包的自动解构会破坏它：`move || { let x = ptr.0; }` 使闭包捕获 `*mut f32`（而非 `SendPtr`），因为编译器在 `move` 闭包内访问字段时会解构 `Copy` 结构体。

2. 在闭包前提取 `.0` — 直接捕获原始指针，同样的问题。

3. **可行方案：** `TrainPtrs` 结构体加上 `unsafe impl Send + Copy`。不在闭包内部访问 `.0`。而是在 `TrainPtrs` 上添加 `run()` 方法和 `word_count()` 方法。闭包捕获 `TrainPtrs`（它是 `Send`），并调用其方法。原始指针仅存在于方法体内（未被捕获）。编译器将捕获的类型视为 `TrainPtrs`，而非 `*mut f32`。

**多线程训练：语料分割**

语料一次性加载到内存中作为 `Vec<u8>`。分割为 `N` 个字节范围（每个线程一个）。每个线程从单词边界开始（向前扫描到下一个空格/换行）。线程独立处理自己的块——无需句子边界协调。

**多线程训练：权重共享**

所有线程通过原始指针共享 `syn0`（输入嵌入）和 `syn1`（输出嵌入）。这是有意的数据竞争——与原始 C 代码中使用 pthreads 的方式相同。在 ARM/x86 上，浮点数写入在硬件层面是原子的（32 位对齐写入）。部分梯度更新会丢失，但 SGD 对此噪声具有鲁棒性。无锁、无原子操作、无争用。

**多线程训练：epoch 循环**

并行路径最初缺少 epoch 循环（单线程有）。在 `std::thread::scope` 周围添加了 `for epoch in 0..cfg.epochs { ... }`。每个 epoch 重新生成线程，再次处理整个语料。每个 epoch 的学习率衰减。

**多线程训练：每个线程的词汇查找**

线程无法访问 `HashMap`（当从 `&mut self` 借用时不是 `Send`）。解决方案：在生成线程之前预先构建排序后的 `Vec<(Vec<u8>, usize)>`（小写单词字节 → 词汇索引）。每个线程在此排序数组上执行 `binary_search_by`。对于 71k 个单词，每次约 17 次比较——速度足够快，不会成为瓶颈。

**原始指针训练函数**

`train_sg_raw` 和 `train_cbow_raw` 是独立函数（非 `Model` 的方法），接受原始指针。它们复制了精确的梯度更新逻辑：

- 对于每个上下文词（Skip-gram）或平均上下文（CBOW）：
  - 正样本：目标=中心词，标签=1
  - N 个负样本：目标=neg_table[sample]，标签=0
  - `f = dot(syn0[input], syn1[target])`
  - `g = (label - sigmoid(f)) * alpha`
  - `neu1e += g * syn1[target]`（累积输入的错误）
  - `syn1[target] += g * syn0[input]`（更新输出）
  - 所有样本后：`syn0[input] += neu1e`（更新输入）

**向量相似度（训练后）**

`Vectors::load` 读取文本和二进制格式（通过是否存在空字节自动检测）。加载时对所有向量进行 L2 归一化。`most_similar` 执行暴力余弦扫描。`analogy` 计算 `vec(a) - vec(b) + vec(c)`，归一化后找到最近邻（排除 a, b, c）。两者均支持交互式 REPL 模式。

**文件格式**

二进制（默认）：`vocab_size dim\n` 头，然后每行 `word\0<float32_le × dim>`。文本：每行 `word f0 f1 ...\n`。两种格式均与原始 C 语言 word2vec 输出格式兼容——可以加载由 C 工具训练的向量，反之亦然。

**CLI 结构**

作为 `ll word2vec <子命令>` 集成到现有的 `ll` 项目中。子命令：`train`、`distance`、`analogy`、`accuracy`。参数使用 `-flag value` 风格，与原始代码匹配（而非 `--flag=value`）。