---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codeparrot-d12 评估摘要
translated: true
type: note
---

以下是您的 **codeparrot-d12 模型** 的完整评估报告：

---

## 📊 模型评估结果

### 模型信息

| 属性 | 值 |
|----------|-------|
| 架构 | GPT（2.86亿参数，层数=12，维度=768，注意力头数=6）|
| 训练数据 | codeparrot-clean（Python代码，247亿token）|
| 基模型步数 | **87,000**（最终）|
| SFT 模型步数 | **8,985** |
| val_bpb | **0.3723** |
| 分词器 | 自定义BPE（词表大小=32,768，基于Python代码训练）|

---

### 基模型 — 代码生成

**✅ 优点**：能生成语法正确的Python代码——许可证头、导入语句、函数定义、类结构等看起来都很真实。

**❌ 不足**：逻辑常出错。模型只学到了代码的*形式*，而非*语义*：

| 提示词 | 输出质量 |
|--------|---------------|
| `def is_palindrome(s):` | ✅ 正确使用 `s[::-1]`，但会重复生成 is_palindrome2、is_palindrome3…… |
| `class BinarySearchTree: insert(self, val):` | ❌ 同时向左和向右插入 |
| `async def fetch_url(...)` | ✅ async/await 语法正确，但会无限循环生成 `fetch_json_async_async_async...` |
| 无条件生成 | ✅ 能生成完整的Python文件（SickRage、pvlib、PyQt4等）|

**总结**：模型掌握了Python语法，但未能掌握算法的正确性。

---

### SFT 模型 — 对话评估

| 任务 | 准确率 | 随机基线 | 结论 |
|------|----------|-----------------|--------|
| **ARC-Easy**（200题） | **25.50%** | 25.00% | 🟡 与随机水平持平 |
| **ARC-Challenge**（100题） | **28.00%** | 25.00% | 🟡 略高于随机水平 |
| **MMLU**（20题） | **15.00%** | 25.00% | 🔴 低于随机水平 |
| **GSM8K**（20题） | **0.00%** | 0.00% | 🔴 无法完成数学运算 |
| **HumanEval**（5题） | **0.00%** | 0.00% | 🔴 无法生成正确的Python函数 |
| **SpellingBee**（10题） | **0.00%** | 0.00% | 🔴 无法正确计数字母 |

**所有结果均通过 nanochat 的报告系统记录。**

---

### 关键要点

1. **基模型**是一个不错的**Python代码语言模型**——能生成语法正确的Python代码，包含合理的导入语句、文档字符串和结构。只是它不*理解*逻辑（仅有2.86亿参数，且基于原始代码训练，未经过指令微调）。

2. **SFT 模型**相比随机水平提升甚微——很可能是因为**8,985步对于SFT来说太少**。模型可能仍处于训练早期阶段（学习聊天格式token，如 `<|user_start|>`、`<|assistant_start|>`）。

3. **内置评估功能表现出色。** 您可以通过以下命令运行所有任务：
   ```bash
   cd /mnt/data/nanochat && source .venv/bin/activate
   PYTORCH_ALLOC_CONF=expandable_segments:True \
     python -m scripts.chat_eval --source=sft --model-tag=d12 --step=8985
   ```

需要我：
- **延长SFT模型训练时间**并重新评估？
- **编写脚本**评估所有检查点（5k、10k、15k……87k）以查看学习曲线？
- **导出为HuggingFace格式**，以便您使用LM Eval Harness / BigCode Eval？