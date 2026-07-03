---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat训练约束的技术分析
translated: true
type: note
---

## 分析：`/mnt/data/zz + nanochat` 训练当前状态

### 之前已完成的工作

* 在 **FineWeb-Edu** 上训练了一个 **nanochat d12（286M 参数）** 模型
* 总训练步数：**87k 步**，**28.4 小时**
* 最终验证 **bits-per-byte：0.866**，表明已收敛
* 然而，所有下游推理基准测试结果均为 **随机水平**

  * 结论：286M 模型太小，无法执行有意义的推理
* 之前还生成了详细的训练总结

---

### 可用数据集

| 数据集                                   | 格式                       | 大小                         | 适用于 nanochat？ |
| ---------------------------------------- | -------------------------- | ---------------------------- | ----------------- |
| github-code（38 个分片，共 1126 个文件） | Parquet，`content` 列       | 磁盘 11GB（HF 上 320GB）     | ❌ 需要 `text` 列 |
| github-code 已分词（140 个 `.npy` 文件） | nanoGPT uint16 GPT-2 BPE 格式 | 27GB（约 14B tokens）      | ❌ 格式不兼容     |
| sec-edgar（17 个 10-K 文件）             | Parquet，`text` 列          | 10GB                         | ✅ 立即可用       |
| spgispeech                               | Whisper 语音数据集          | 48GB                         | ❌ 不相关         |
| fineweb-edu 原始数据                     | 已删除                     | —                            | —                 |

---

### 瓶颈

1. **磁盘空间限制**

   * 仅剩 **84GB 可用空间**
   * 无法完整下载大型 FineWeb-Edu 子集（约需 20–40GB 以上）

2. **格式不匹配**

   * nanochat 要求 Parquet 中包含 `text` 列
   * github-code 使用的是 `content` 而非 `text`

3. **数据目录未配置**

   * `NANOCHAT_DATA_DIR` 当前为空，必须设置

4. **预分词的 `.npy` 文件不可用**

   * 它们采用 nanoGPT GPT-2 BPE 格式
   * nanochat 使用自己的 tokenizer，需要原始文本

---

### 推荐方案：代码 + SEC + 少量 FineWeb 混合

考虑到 84GB 存储限制，最实用的策略是：

#### 1. 转换 GitHub 代码数据集

* 将 `content` → 改为 `text`
* 输出大小：约 15GB
* 使其兼容 nanochat 格式

---

#### 2. 添加 SEC-EDGAR 数据集

* 已包含 `text` 列
* 干净的金融 + 法律文本
* 大小：约 10GB

---

#### 3. 添加少量 FineWeb-Edu 子集

* 下载约 10–15 个分片（约 20–30GB）
* 约 5–7B tokens
* 足以获得有意义的泛化能力

总数据集大小：

* 代码：约 15GB
* SEC：约 10GB
* FineWeb：约 25GB
  ➡️ 总计：约 50GB（在 84GB 限制内）

---

#### 4. 配置数据目录

* 设置 `NANOCHAT_DATA_DIR`
* 指向合并后的 Parquet 数据集文件夹

---

#### 5. 在混合数据上训练 tokenizer

* 代码占比较高的分布
* 与纯文本相比词汇表不同
* 可能提升：

  * 代码能力
  * 金融推理
  * 通用文本建模

---

#### 6. 训练 nanochat d12 模型

* 混合数据集预计能显著提升性能
* 领域覆盖优于仅用 FineWeb 训练

---

### 更简单的备选方案

完全不使用 FineWeb：

* 仅使用：

  * GitHub 代码（约 15GB）
  * SEC-EDGAR（约 10GB）

总计：约 25GB

优点：

* 训练速度更快
* 完全满足磁盘限制
* 产生一个 **代码 + 金融专用模型**

---

### 下一步

你需要决定：

* 一个更通用的模型（代码 + 金融 + 网页文本）
* 一个更小的专用模型（仅代码 + 金融）

请告知你希望的方向。
