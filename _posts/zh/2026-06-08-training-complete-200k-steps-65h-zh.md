---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练完成：20万步，65小时
translated: true
type: note
---

🎉🎉🎉 训练完成！ 🎉🎉🎉

最终统计：
- 步骤：**200,000 / 200,000** — 完成！
- 总时长：**3,921.91 分钟**（约 65.4 小时，约 2.7 天）
- 最小验证 bpb：**0.780026**
- CORE 指标：**0.1987**
- 峰值内存：**9,435 MiB**

评估结果（值得关注）：
- hellaswag（10-shot）：**41.6%**
- winograd（0-shot）：**59.0%**
- winogrande（0-shot）：**54.2%**
- boolq（10-shot）：**54.8%**
- lambada_openai（0-shot）：**34.4%**
- bigbench_cs_algorithms（10-shot）：**45.8%**

样本生成显示模型可以生成连贯的文本（“法国的首都是巴黎……”），但在数学推理方面存在困难（“5*x + 3 = 13”循环）。检查点已保存至 `/home/lzw/.cache/nanochat/base_checkpoints/d12/model_200000.pt`。

模型已准备好用于下游微调或部署。