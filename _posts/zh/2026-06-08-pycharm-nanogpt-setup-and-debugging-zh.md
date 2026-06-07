---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyCharm NanoGPT 设置与调试
translated: true
type: note
---

以下是在 PyCharm 中配置的方法：

1. 打开项目：File → Open → ~/projects/nanoGPT

2. 设置 Python 解释器：PyCharm → Settings → Project → Python Interpreter → Add → Existing → `/opt/homebrew/bin/python3.14`

3. 为 sample.py 创建运行配置：
   - Run → Edit Configurations → + → Python
   - 名称：`sample-gpt2`
   - 脚本路径：`sample.py`
   - 参数：
     ```
     --init_from=gpt2 --device=mps --dtype=float32 --num_samples=1 --max_new_tokens=150 --start="Hello world"
     ```
   - 工作目录：`/Users/lzwjava/projects/nanoGPT`

4. 为 Shakespeare 模型创建另一个配置：
   - 名称：`sample-shakespeare`
   - 脚本路径：`sample.py`
   - 参数：
     ```
     --out_dir=out-shakespeare-char --device=mps --dtype=float32 --num_samples=1 --max_new_tokens=200 --start="ROMEO:"
     ```

5. 设置断点 — 好的起始位置：
   - `model.py` 约第175行：在 `CausalSelfAttention` 的 `forward()` 内部 — 观察 q、k、v 的形状
   - `model.py` 约第210行：在 `MLP` 的 `forward()` 内部 — 观察 4 倍扩展
   - `sample.py` 第87行：`model.generate()` 调用 — 单步进入以查看自回归循环
   - `model.py` 约第245行：`GPT.generate()` — 观察 token 如何逐个被追加

6. 调试：点击调试图标（Shift+F9）而不是运行。使用：
   - F7：Step Into（进入函数内部）
   - F8：Step Over（单步跳过）
   - F9：Resume（运行到下一个断点）
   - Alt+单击变量：求值表达式

对于 `train.py`，创建如下配置：
   - 脚本路径：`train.py`
   - 参数：`config/train_shakespeare_char.py --device=mps`
   - 这会训练字符级模型 — 在训练循环的 `train.py` 约第175行（`for X, Y in loader:`）设置断点，以逐步观察损失下降。

就是这样。PyCharm 的调试器配合 MPS 张量可以正常工作 — 你可以在 Variables 面板中检查形状、数值和梯度。