---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MoE实现与验证
translated: true
type: note
---

完成 — MoE 已实现并完成端到端验证（训练 → 检查点 → 恢复/采样）。

## 在 `train.py` 中新增的内容

**`MoE` + `Expert` 模块**（位于 `MLP` 之后）：
- **Router**：一个线性门控为每个词元生成 `n_experts` 个 logits；每个词元被路由到其 **top-k** 个专家，并对所选 logits 应用 softmax 权重（GShard/Mixtral 风格）。
- **Dispatch**：词元按专家分组，每个专家（一个与稠密 MLP 具有相同 `c_fc`/`c_proj` 形状的 `Expert` MLP，因此 GPT-2 缩放的 `c_proj` 初始化仍然适用）仅对其分配到的词元运行，输出通过 `index_add` 合并——未选中的专家不浪费计算。
- **负载均衡**：来自 Switch-Transformer 的辅助损失 `E · Σᵢ fᵢ·Pᵢ`，基于分配密度与路由器平均概率计算，从而激励路由器均匀使用所有专家。

**`Block`**：当 `config.use_moe` 设置时，使用 `MoE` 替代 `MLP`。

**`GPT`**：
- `forward` 方法对每个块的辅助损失求和，并将 `moe_aux_loss_coef * aux` 添加到交叉熵损失中（确保在 DDP/梯度累积中正确流动）。
- `get_num_params_active()` 报告每个词元实际触及的参数数量（仅 top-k 专家激活）。
- `get_aux_loss()` 暴露最后的辅助损失用于日志记录。

**CLI**（检查点配置通过 `asdict` 自动往返，旧稠密检查点仍可恢复，因为新字段默认关闭）：
- `--moe`、`--n_experts 8`、`--n_experts_active 2`、`--moe_expert_dim 4`、`--moe_aux_loss_coef 0.01`

## 验证

```
use_moe=False: loss=4.1965 params=104,256   active=104,256
use_moe=True:  loss=4.2058 aux=1.3167 params=303,296 active=170,944  (top-2/4)
```

实际运行（在 tiny shakespeare 上使用 `--moe`，CPU）：
```
model: 31.95M parameters
model: MoE top-2/4, 17.77M active parameters per token
iter 8: loss 3.5274 | aux 1.8717 | ...
```
所有参数都接收梯度，生成功能正常，每次迭代的日志现在包含辅助损失（当路由均衡时，该值应接近每层 `k` ≈ n_experts_active；如果上升，则说明专家正在坍缩）。

用法：`python train.py --moe --n_experts 8 --n_experts_active 2`