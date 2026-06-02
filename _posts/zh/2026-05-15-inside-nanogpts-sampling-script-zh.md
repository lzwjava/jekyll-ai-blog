---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NanoGPT采样脚本内部解析
translated: true
type: note
---

这是一个89行的脚本，它做三件事：构建模型、编码提示、逐个生成token。让我逐一讲解每个部分。

## 1. 配置与设置（`sample.py:11–32`）

第12-22行将默认值声明为普通的模块级变量（`init_from`, `start`, `num_samples`, `temperature`, `top_k`等）。然后第23行执行魔法：
```python
exec(open('configurator.py').read())   # 从命令行覆盖
```
这会运行`configurator.py`，它遍历`sys.argv`并用你的`--init_from=gpt2-xl --start="Hello, my name is" ...`标志覆盖那些全局变量。这就是你在日志中看到`Overriding: init_from = gpt2-xl`的原因。

第26-32行设置RNG种子，启用TF32矩阵乘法（免费加速），并设置`autocast(bfloat16)`上下文——所有在`with ctx:`内的前向传播都以bf16运行，同时保留主权重为fp32。

## 2. 构建模型（`sample.py:35–54`）

根据`init_from`有两种路径：

- `resume` → 加载`out/ckpt.pt`（你自己训练的检查点）。
- `gpt2*` → 在第49行调用`GPT.from_pretrained('gpt2-xl', dict(dropout=0.0))`。

第二个路径位于`model.py:228–283`。它：
1. 从硬编码的字典（`model.py:238–243`）中选择正确的`n_layer/n_head/n_embd`。对于`gpt2-xl`：**48层，25个头，1600嵌入维度，1.5B参数**。
2. 用这些维度构建一个**空的nanoGPT**。
3. 下载HuggingFace的`GPT2LMHeadModel.from_pretrained('gpt2-xl')`权重（这就是你刚刚下载的6.5 GB）。
4. 逐个将张量复制到nanoGPT的state_dict中。四个权重矩阵被转置，因为OpenAI的原始代码使用了`Conv1D`层，而nanoGPT使用`nn.Linear`（`model.py:267`，`274–276`）。

然后`model.eval()`（禁用dropout）和`model.to(device)`——完成。

## 3. 分词器（`sample.py:56–74`）

由于你使用了`gpt2-xl`（而不是`resume`），它进入第70行的`else`分支：
```python
enc = tiktoken.get_encoding("gpt2")
encode = lambda s: enc.encode(s, ...)
decode = lambda l: enc.decode(l)
```
`tiktoken`是OpenAI的快速Rust BPE分词器。`"Hello, my name is"` → `[15496, 11, 616, 1438, 318]`（5个token）。

## 4. 编码提示（`sample.py:77–81`）

```python
start_ids = encode(start)
x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])
```
形状：`(1, 5)` — 一个批次，序列长度为5个token。这被送入GPU。

## 5. 生成循环（`sample.py:84–89` → `model.py:327–352`）

```python
for k in range(num_samples):          # 3个外部样本
    y = model.generate(x, max_new_tokens=200, temperature=0.8, top_k=200)
    print(decode(y[0].tolist()))
```

实际的采样位于`model.py:generate()`中。对于200个新token中的每一个：

```python
idx_cond = idx if idx.size(1) <= block_size else idx[:, -block_size:]  # 裁剪到1024
logits, _ = self(idx_cond)             # 完整前向传播（第338行）
logits = logits[:, -1, :] / temperature  # 只取最后一个位置，缩放
if top_k is not None:
    v, _ = torch.topk(logits, k=top_k)
    logits[logits < v[:, [-1]]] = -float('Inf')  # 屏蔽top-200之外的所有内容
probs = F.softmax(logits, dim=-1)
idx_next = torch.multinomial(probs, num_samples=1)  # 采样一个token
idx = torch.cat((idx, idx_next), dim=1)              # 追加，重复
```

这是**自回归采样（autoregressive sampling）**：每一步，模型看到到目前为止生成的所有内容，为*下一个*token预测一个覆盖约50K词汇token的分布，采样一个，追加，重复。

两个重要的调节旋钮：
- **`temperature=0.8`** — 在softmax之前除以logits。小于1.0使分布更尖锐（更保守）；大于1.0使分布更平坦（更随机）。
- **`top_k=200`** — 每一步只保留概率最高的200个token，其余置零。防止采样到低概率的垃圾。

200步之后，`y`是一个形状为`(1, 205)`的token ID张量。`decode(y[0].tolist())`将其转换回文本。

## 为什么输出看起来不错

这**不是**因为nanoGPT做了什么聪明的事——`sample.py`是一个教科书式的生成循环。质量完全来自两个事实：

**1. GPT-2 XL在其时代确实很强。** 它有1.5B参数，训练在约40GB的网络文本（WebText）上，约300B token。它学会了英语语法、几百个token内的主题连贯性，以及大量世界知识。你的提示`"Hello, my name is"`落在模型已经见过*数百万*次的分布区域——个人博客文章、论坛介绍、个人简介——因此它有非常自信、形状良好的续写。

**2. 你的采样设置调得很好。**
- `temperature=0.8`是最佳点。在1.0时模型会变得疯狂；在0.5时会变得重复。0.8在保持有趣的同时也连贯。
- `top_k=200`过滤掉了无意义token的尾部，同时不强制贪婪。
- 这就是为什么每个样本是*不同的*（它是随机的），但每个样本都*保持连贯*（没有随机词沙拉）。

你所看到的**并不是推理**——模型不知道Esteban Galaviz是否存在或不存在，它只知道“教授名字听起来像X”和“智利大学与西班牙语名字搭配”。这是高质量的模式完成。幻觉（Haverford College在宾夕法尼亚州，不在智利；Kainos Dental可能不存在）就是证据。

## 整个脚本用一段话概括

读取配置，构建一个从头开始的GPT或一个从HuggingFace预训练的GPT-2（转换为nanoGPT的结构），用tiktoken对提示进行分词，运行一个自回归循环，该循环对每个新token执行*一次完整的穿过所有48个transformer块的前向传播*，并以温度0.8从概率最高的200个下一token中采样，然后将得到的ID解码回文本。运行3次得到3个样本。每个新token都需要重新计算整个增长中上下文的注意力——这就是为什么生成随着序列变长而变慢，以及为什么`block_size=1024`是一个硬上限（第336行如果超过则会裁剪）。
