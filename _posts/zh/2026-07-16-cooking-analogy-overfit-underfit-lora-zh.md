---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 烹饪类比：过拟合、欠拟合与LoRA
translated: true
type: note
---

问题：烹饪类比是否成立——牛排熟度/火候 ≈ 数据分布效果，干烤 vs 蒸 ≈ 导致过拟合/欠拟合的不同训练策略，而预训练后的“酱油”微调 ≈ 训练后调整？

答案：基本正确，但微调比喻需要一处修正。

**过拟合/欠拟合 ≈ 烹饪方法不匹配——正确。**

蒸（湿加热）vs 干烤（无水）改变了热量向组织内部传递的方式——水分过多会使蔬菜变得糊烂（过拟合到水中的噪声），热量/时间不足则会夹生（欠拟合）。这正是偏差-方差的故事：

```python
import numpy as np

def fit_poly(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    return np.poly1d(coeffs)

np.random.seed(0)
x = np.linspace(0, 1, 15)
y_true = np.sin(2 * np.pi * x)
y = y_true + np.random.normal(0, 0.2, size=x.shape)  # 带噪声的“潮湿”数据

for deg, label in [(1, "欠拟合"), (3, "拟合良好"), (14, "过拟合")]:
    f = fit_poly(x, y, deg)
    train_err = np.mean((f(x) - y) ** 2)
    print(f"degree={deg:2d} ({label:9s}) train_mse={train_err:.4f}")
```

1 次多项式无法捕捉正弦形状（欠拟合——未煮熟，结构从未形成）。14 次多项式精确拟合每一个噪声点，包括噪声本身（过拟合——蔬菜吸收了调味水变得软烂，记住了无关的波动）。3 次多项式追踪真实的 `sin` 形状而不追逐噪声——这就是“烹饪得当”的模型，低偏差且低方差。

**酱油微调 ≈ 预训练后调整——部分正确，需要修正。**

“酱油”暗示*表面*调味：基础食材的内部结构保持不变，只在表面增加风味层。完整微调并非如此温和——它更新所有权重，可能导致灾难性遗忘（基础的“风味”部分被煮掉，而非只添加）。真正匹配“酱油”（轻涂表面，基础不变）的比喻是 **LoRA / 适配器微调**——你冻结预训练权重（已煮熟的基础）并在其上添加一个小的低秩增量（酱料）：

```python
# 概念上：W' = W_frozen + BA   (B, A 低秩，W 冻结)
# 完整微调：W' = W - lr * grad(W)   -> 基础本身发生变化
```

因此：
- 预训练 = 烹饪基础食材（结构/风味已烤制进去，成本高、速度慢，对你而言约每月 2B token 的规模）
- 完整微调 = 用新的调味料重新烹饪，直接混入食材本身——改变了基础
- LoRA/适配器微调 = 字面意义上的酱油——廉价、可逆、不触及基础权重
- 蒸馏 = 通过教师模型的输出将风味传递给更小的锅（学生模型）

Karpathy 自己的“配方”文章正是用这个烹饪框架来描述训练动态——鉴于你正在自行训练 GPT-2 760M，值得重读一遍。

参考：
- [《训练神经网络的配方》—— Karpathy](http://karpathy.github.io/2019/04/25/recipe/)
- [LoRA：大型语言模型的低秩适配](https://arxiv.org/abs/2106.09685)
- [偏差-方差权衡——过拟合/欠拟合形式化描述](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff)