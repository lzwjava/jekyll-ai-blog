---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 决策训练下一步
translated: true
type: note
---

问题：查看完我上传的 Nanochat 760M MI300X 设置文档后，下一步该做什么？

回答：

根据您上传文件中的详细说明，以下是结构化的下一步计划：

---

### 1. 确定训练策略

您有两个选择：

**选项 A：继续使用当前 SDPA 设置**

* 当前 MFU 约为 27%，完成 29,000 步训练大约需要 62 小时。
* 优点：稳定，与 MI300X 完全兼容。
* 缺点：吞吐量低于潜在最大值。

**选项 B：尝试速度优化**

* 请谨慎考虑以下选项：

  1. **ROCm Flash Attention** – 可能将 MFU 提升至 40–50%。

     * 风险：可能编译失败。
  2. **FP8 精度** – 吞吐量约提升 2 倍。

     * 需要 PyTorch 针对 ROCm 7.2+ 编译。
  3. **增加 device_batch_size** – 减少梯度累积开销。

     * 风险：SDPA 内存可能导致 OOM 错误。
  4. **多 GPU 训练** – 吞吐量线性扩展。
  5. **增加总批次大小** – 步数减少，处理的 token 数相同。

> **建议：** 如果可靠性是优先考虑，请坚持当前设置（选项 A）。如果您希望进行实验并能处理潜在的构建问题，可尝试选项 B 的部分优化。

---

### 2. 准备训练

* 确认数据集可用：`~/.cache/nanochat/base_data_climbmix/`
* 确保 tokenizer 已训练：`~/.cache/nanochat/tokenizer/`
* 决定是恢复训练还是重新开始：

  * 恢复：`./run_mi300x_d24_pretrain.sh --resume-from-step=XXXX`
  * 完整运行：`./run_mi300x_d24.sh`

---

### 3. 运行预训练

* 开始监控日志：

  ```bash
  tail -f /root/nanochat/run_mi300x_d24.log
  ```
* 监控指标：loss、tokens/sec、MFU。
* 确保每 5000 步保存检查点以保证安全。

---

### 4. 训练后流程

基础预训练完成后：

1. 使用 DCLM CORE 基准评估基础模型。
2. 在聊天数据（`identity_conversations.jsonl`）上运行 SFT。
3. 使用聊天基准评估 SFT 模型。
4. 启动交互式聊天：

   ```bash
   python -m scripts.chat_cli -p 'Hello!'
   python -m scripts.chat_web
   ```

---

### 5. 未来运行的可选改进

* 使用 ROCm flash attention 和 FP8 提升吞吐量。
* 使用多 GPU 进行更大规模训练。
* 如果使用 flash-attn，尝试调整批次大小和滑动窗口 attention。

---

### 建议的立即下一步

* 决定是**坚持当前设置还是进行优化**。
* 如果坚持当前设置，**启动完整预训练**并监控日志。
* 如果进行优化，每次只选择一项改进（例如，尝试 ROCm flash-attn）并验证稳定性。

---

您可以先确认您的优先级：**可靠性 vs 速度**。这将决定您是立即运行 `run_mi300x_d24.sh` 还是尝试性能调整。