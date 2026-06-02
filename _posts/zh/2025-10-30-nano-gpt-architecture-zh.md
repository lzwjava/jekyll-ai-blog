---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: NanoGPT模型架构解析
translated: true
type: note
---

### NanoGPT 模型架构概览

NanoGPT 在 PyTorch 中实现了一个类似 GPT-2 的仅解码器 Transformer 模型。架构定义在 `model.py` 文件中，通过可配置的 `GPTConfig` 设置超参数。默认配置（例如用于 "gpt2" 变体）使用：

- **Transformer 块数量**：12（`n_layer = 12`）
- **嵌入维度（层大小）**：768（`n_embd = 768`）
- **注意力头数量**：12（`n_head = 12`）
- **MLP 中间层大小**：3072（`n_embd * 4`，扩展因子为 4）

每个 Transformer 块（`Block` 类）是一个标准的解码器块，包含残差连接和层归一化。它包括：

- **层归一化 1**（`ln1`）：在自注意力之前应用。
- **多头自注意力**（`attn`）：因果（掩码）注意力，防止向前看。
- 注意力后的残差加法。
- **层归一化 2**（`ln2`）：在 MLP 之前应用。
- **MLP**（`mlp`）：一个简单的前馈网络。
- MLP 后的残差加法。

整体模型（`GPT` 类）在词元和位置嵌入之后堆叠了这 12 个块，然后是最终的层归一化（`ln_f`）和一个线性投影到词汇表大小。

#### MLP 结构

MLP（`Block` 内的 `MLP` 类）是一个两层前馈网络：

- 第一线性层（`c_fc`）：从 `n_embd`（768）投影到中间大小（3072）。
- GELU 激活：在第一投影后逐元素应用。
- 第二线性层（`c_proj`）：从 3072 投影回 `n_embd`（768）。

这遵循您提到的 "fc -> gelu -> projection" 模式。

#### 前向传播流程

前向传播是残差风格的，采用预归一化（子层之前的 LayerNorm）。以下是高级分解：

1. **主前向传播（GPT.forward）**：
   - 词元嵌入：输入词元（形状 `[B, T]`）→ 嵌入（形状 `[B, T, n_embd]`）。
   - 位置嵌入：添加到词元嵌入。
   - 通过 `n_layer`（12）个 Transformer 块堆栈：每个块执行 `x = block(x)`。
   - 最终层归一化：`x = self.ln_f(x)`。
   - 线性投影：`logits = self.lm_head(x)` → 输出形状 `[B, T, vocab_size]`。

   代码片段（简化）：

   ```python
   def forward(self, idx, targets=None):
       # ... 嵌入 + 位置
       for block in self.blocks:
           x = block(x)
       x = self.ln_head(x)
       logits = self.head(x)
       # ... 如果有目标则计算损失
       return logits
   ```

2. **Transformer 块中的前向传播（Block.forward）**：
   - 对输入 `x` 应用 `ln1`。
   - 自注意力：`x = x + attn(ln1(x))`（残差）。
   - 对结果应用 `ln2`。
   - MLP：`x = x + mlp(ln2(x))`（残差）。

   代码片段（简化）：

   ```python
   def forward(self, x):
       x = x + self.attn(self.ln1(x))
       x = x + self.mlp(self.ln2(x))
       return x
   ```

3. **自注意力中的前向传播（MultiheadAttention.forward）**：
   - 层归一化输入 → 计算 Q、K、V 投影（线性层 `c_attn`）。
   - 分割成头，应用因果掩码，缩放点积注意力。
   - 拼接头，使用 `c_proj` 投影回来。
   - 残差加法（但在块中，加法在外部进行）。

   关键点：因果掩码确保忽略未来词元。输出形状保持为 `[B, T, n_embd]`。

   代码片段（核心注意力计算，简化）：

   ```python
   def forward(self, x):
       B, T, C = x.shape
       qkv = self.c_attn(x).split(self.n_embd, dim=2)  # Q,K,V
       # ... 重塑为头，掩码，attn = q @ k.transpose / sqrt
       # attn = attn.masked_fill(mask == 0, -1e9)
       # y = attn @ v
       # ... 拼接和投影
       return self.c_proj(y.reshape(B, T, C))
   ```

4. **MLP 中的前向传播（MLP.forward）**：
   - 第一投影：`x = self.c_fc(x)` → 到中间大小。
   - GELU：`x = F.gelu(x)`。
   - 第二投影：`x = self.c_proj(x)` → 回到 `n_embd`。

   代码片段：

   ```python
   def forward(self, x):
       x = self.c_fc(x)
       x = F.gelu(x)
       x = self.c_proj(x)
       return x
   ```

此设置紧密镜像 GPT-2 的架构，默认配置下约有 1.24 亿参数。具体代码请查看代码库。

[model.py 源代码](https://github.com/karpathy/nanoGPT/blob/master/model.py)
