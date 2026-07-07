---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 先快速运行，后验证
translated: true
type: note
---

问题：给定 H200 上 1.45B 参数模型的吞吐量估算（约 40-45K token/秒）与 760M 参数 MI300X 参考数据（约 68K token/秒），我应该选择哪种训练时长——完整的 Chinchilla 最优方案（290 亿 token，约 7.5 天）、半程方案（145 亿 token，约 3.7 天），还是快速方案（72.5 亿 token，约 1.9 天）？

回答：

**先执行快速运行。不要盲目投入 7.5 天。**

**原因如下：**

1.  **你尚未在 H200 上验证整个流程。** 不同 GPU（Hopper 架构 vs CDNA3 架构）、不同 FA 内核路径（FA3 与 ROCm 所用方案）。吞吐量估算值源于外推，而非实际测量。如果你的实际 MFU 只有 25% 而非 35%，那么你原本预计的 7.5 天将变成 10 天以上，而你将在第三天才发现这个问题，白白浪费租赁成本。

2.  **在信任 Hermes 的数据之前，先验证 FLOPs 计算的合理性。** 粗略交叉验证：

```python
# 基于计算的吞吐量合理性检查（Kaplan/Chinchilla 近似）
def est_tok_per_sec(params, peak_tflops, mfu):
    flops_per_token = 6 * params  # 前向+反向，稠密 Transformer
    achieved_flops = peak_tflops * 1e12 * mfu
    return achieved_flops / flops_per_token

# MI300X, 760M 模型
print(est_tok_per_sec(760e6, peak_tflops=1307, mfu=0.24))  # ~413K...
# 等等 —— 对照他们报告的 68K tok/s 反推隐含 MFU：
def implied_mfu(params, tok_per_sec, peak_tflops):
    flops_per_token = 6 * params
    return (flops_per_token * tok_per_sec) / (peak_tflops * 1e12)

print(implied_mfu(760e6, 68_000, 1307))   # MI300X bf16 峰值约 1307 TFLOPS
print(implied_mfu(1.45e9, 42_000, 989))   # H200 bf16 稠密峰值约 989 TFLOPS
```

运行这两行代码 —— MI300X 的 MFU 约为 24%，H200 的估算值 MFU 约为 36%。这在理论上是可行的（H200 的软件栈加上 FA3 在处理小型稠密模型时确实比当前的 ROCm 能获得更高的 MFU），但这本质上是**估算值叠加估算值**。真正训练的前 30 分钟将告诉你实际数值 —— 直接从训练循环中测量 `tokens/sec`，不要相信预测值。

3.  **在当前阶段，机会成本比计算最优性更重要。** 你尚未实现稳定营收，仍在构建服务管线，一个 760M/1.45B 的稠密模型并非你的护城河 —— 对 nanochat/DeepSeek v4 MoE 的理解才是。一次持续一周、仅生成一个检查点的单次运行，相比于验证管线、撰写博文、将 H200 预算释放给真正前沿学习所在的 MoE 实验，是一次糟糕的取舍。

**建议的执行顺序：**

| 步骤 | Token 数量 | 时间 | 目的 |
|------|------------|------|------|
| 1. 烟雾测试 | 1 亿 | 约 10 分钟 | 确认无 NaN、检查点/恢复功能正常、测量实际 tok/s |
| 2. 快速基线（5 倍） | 72.5 亿 | 约 1.9 天 | 获取真实损失曲线、真实检查点、可发表的结果 |
| 3. 决策 | — | — | 如果损失曲线和评估结果合理，并有信心，再扩展到半程或完整 Chinchilla 方案 |

只有在你已经拥有一个可用的检查点/恢复框架，并且准备好应对因抢占、内存溢出或驱动程序故障而导致运行失败、一无所获的情况下，才应直接跳过，投入 7.5 天的运行。

**最小检查点/恢复框架**（如果你没有 —— 在租赁计算资源上进行任何超过 1 天的运行，这是强制要求）：

```python
import torch, os, time

def save_ckpt(model, opt, step, path="ckpt.pt"):
    torch.save({
        "model": model.state_dict(),
        "opt": opt.state_dict(),
        "step": step,
    }, path + ".tmp")
    os.replace(path + ".tmp", path)  # 原子写入，可在保存中途崩溃时幸存

def load_ckpt(model, opt, path="ckpt.pt"):
    if not os.path.exists(path):
        return 0
    ck = torch.load(path, map_location="cuda")
    model.load_state_dict(ck["model"])
    opt.load_state_dict(ck["opt"])
    return ck["step"]

# 在训练循环中
step = load_ckpt(model, opt)
last_save = time.time()
for step in range(step, total_steps):
    train_step(...)
    if time.time() - last_save > 600:  # 每 10 分钟
        save_ckpt(model, opt, step)
        last_save = time.time()
```

同时，在每个检查点记录 `tokens/sec` 和每十亿 token 的成本 —— 在涉及训练基础设施建议的咨询项目中，你会需要这个数字；"我实际测量过 H200 与 MI300X 的 $/token 成本" 是让你区别于那些 API 封装顾问的真正差异点。

**总结：** 先运行 1.9 天的快速基线，在第一个小时内测量真实吞吐量，然后根据实际数据（而非外推表格）来决定是否进行完整的 Chinchilla 方案运行。