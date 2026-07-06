---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国AI系统训练营
translated: true
type: note
---

问题：在中国为高中生/大学生开办AI训练营（模型训练、智能体等）是个好主意吗？

答案：

是的——但前提是你*不要将其定位为“AI教育”*。那个市场已经被教程式课程饱和了。可行的版本是：

> **“AI系统训练营：在2-4周内构建并部署真实的智能体和小型模型。”**

你不是在教理论。而是将实际生产工作流（比如你已经用GPU训练+CLI智能体做的事情）压缩成动手交付的实践。

---

## 1. 真正的机会在哪里

中国大多数训练营：

* 教Python基础
* 包装HuggingFace管道
* 止步于笔记本级别的演示

你可以利用的差距：

* **端到端的系统思维**
  * 数据 → 训练 → 评估 → 部署 → 智能体循环
* **真实的基础设施接触**
  * 多GPU训练，而不是Colab玩具
* **智能体工程**
  * 工具使用、记忆、规划、CLI优先的工作流

这更接近：

* “迷你OpenAI应用实验室”
* 而不是“AI课程”

---

## 2. 教什么（紧凑、生产优先）

### 第1周 — LLM与推理核心

* 分词、注意力机制（仅直觉层面的数学）
* 运行本地LLM（vLLM / llama.cpp）
* 构建CLI聊天界面

```bash
python chat.py --model Qwen2.5-7B
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B")

prompt = "设计一个交易智能体架构"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=200)
print(tok.decode(out[0]))
```

---

### 第2周 — 微调小模型

* LoRA / QLoRA
* 数据集构建（大多数忽略的关键技能）
* 评估循环

```bash
accelerate launch train_lora.py \
  --model meta-llama/Llama-3-8B \
  --dataset data.jsonl
```

关键思路：学生学习**数据质量 > 模型选择**

---

### 第3周 — 智能体（核心差异化）

* 工具调用
* 记忆（向量数据库）
* 规划循环

最小智能体循环：

```python
while True:
    obs = env.observe()
    action = llm(f"Obs: {obs}\n下一步该做什么？")
    env.step(action)
```

增加：

* 网络工具
* 代码执行
* 文件系统工具

---

### 第4周 — 毕业设计系统

例子：

* 研究智能体（论文 → 摘要 → 仓库）
* 交易模拟智能体
* 微信内容生成管道
* GitHub仓库的代码审查机器人

必须部署：

* FastAPI后端
* 简单Web UI或CLI（如果追求工程纯粹性，CLI更优）

---

## 3. 技术栈（保持现实）

* 训练：PyTorch + HF + DeepSpeed（可选）
* 推理：vLLM / llama.cpp
* 智能体：纯Python循环（先避免框架）
* 向量数据库：FAISS（不要过度设计）
* 部署：Docker + 简单VPS

避免：

* “无代码AI平台”
* 重量级SaaS抽象

---

## 4. 中国的商业现实

### 强信号

* 家长愿意为“面向未来的技能”付费
* 大学需要“AI实践培训”
* 对智能体和LLM应用兴趣浓厚

### 弱点

* 监管敏感性（内容+未成年人）
* 除非产出可见（项目），否则流失率高

### 定价结构

* 2-4周密集型：3000-10000元/学生
* 分组制（20-50人）
* 如果展示GitHub产出则杠杆效应强

---

## 5. 你真正的护城河

鉴于你的背景（训练模型、GPU基础设施、智能体CLI工具），你的优势是：

* 你可以展示*真实的训练过程*，而不是幻灯片
* 你可以教“系统在生产中如何崩溃”
* 你可以从第一性原理设计课程

这很少见。大多数讲师离真实基础设施有两层距离。

---

## 6. 失败模式（重要）

1. **变成教程工厂**
   * 学生复制笔记本 → 没有留存
2. **理论过多**
   * 迅速扼杀感知价值
3. **没有产出**
   * 必须每周强制提交GitHub仓库
4. **过度框架化智能体**
   * 过早引入LangChain式抽象 → 混乱

---

## 7. MVP建议

不要从学校开始。

从以下开始：

* 1个组（10-15人）
* 2周“智能体冲刺”
* 目标：每个人交付1个可工作的智能体仓库

如果留存率和产出质量高 → 扩展。

---

参考资料：

* [https://github.com/karpathy/minGPT](https://github.com/karpathy/minGPT)
* [https://github.com/huggingface/transformers](https://github.com/huggingface/transformers)
* [https://course.fast.ai](https://course.fast.ai)
* [https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)
