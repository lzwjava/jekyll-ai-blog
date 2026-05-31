---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MiMo V2.5 与 Pro 功能对比
translated: true
type: note
---

**问题：** 小米MiMo-V2.5 Pro是否具备多模态能力？它是否支持图像理解、OCR以及从截图中提取文本/代码？

**回答：**

以下是详细说明——V2.5系列中的两个模型在能力上其实存在显著差异：

---

## MiMo-V2.5与MiMo-V2.5-Pro：多模态能力分化

| 特性 | MiMo-V2.5 | MiMo-V2.5-Pro |
|---|---|---|
| 多模态（图像/视频/音频） | ✅ 是 | ❌ 否——仅支持文本/代码 |
| 参数规模 | 310B总参/15B激活 | 1.02T总参/42B激活 |
| 侧重方向 | 全模态感知 + 智能体 | 高级编码 + 长周期智能体 |
| OCR / 截图解析 | ✅（通过ViT编码器） | ❌ |

关键区别：V2-Pro仅支持文本和代码。多模态能力原本存在于另一个独立模型（MiMo-V2-Omni）中。MiMo-V2.5将所有能力整合为一个模型，原生内置图像、视频和音频理解功能。但**V2.5-Pro仍然仅支持文本**，专注于提升编码和智能体性能。

---

## MiMo-V2.5多模态架构

MiMo-V2.5配备了一个**729M参数的视觉Transformer（ViT）**，采用混合窗口注意力机制，并拥有专用音频编码器。该ViT使用滑动窗口注意力实现高效视觉编码。

语言骨干网络继承了MiMo-V2-Flash的混合滑动窗口注意力，并通过轻量级投影仪连接专用视觉和音频编码器（均为内部预训练）。训练分为五个阶段：文本预训练 → 投影仪预热 → 多模态预训练 → SFT + 智能体后训练 → RL + MOPD。

因此，对于基础版V2.5模型，OCR和截图转文本/代码提取完全在其能力范围内。ViT编码器负责图像令牌化，而MoE LLM骨干网络负责推理/提取。

---

## OCR / 截图使用场景

在图像和视频理解基准测试中，MiMo-V2.5与前沿闭源模型水平相当——在视频任务上与Gemini 3 Pro持平，在多模态智能体工作上与Claude Sonnet 4.6匹敌，在图像和文档理解方面保持竞争力。

“文档理解”是涵盖OCR、表格提取以及从截图中提取代码/文本的基准类别。因此，针对您的使用场景（截图 → 代码或文本），**您应该选择MiMo-V2.5（而非Pro）**。

---

## 快速实用总结

- **需要OCR / 图像 → 截图中文本/代码？** → 使用 **MiMo-V2.5**（较小的全模态版本）
- **需要最佳编码智能体，不涉及图像？** → 使用 **MiMo-V2.5-Pro**
- 两者均采用MIT许可证，可在HuggingFace上获取开放权重
- 两者均支持 **100万令牌的上下文窗口**，基于稀疏MoE架构并采用混合注意力机制

若要在本地RTX 4070（12GB）上运行V2.5进行OCR，需要使用量化版本——15B激活参数在4-bit下约需8GB，可行。V2.5-Pro的42B激活参数对于4070来说过大；需使用AMD MI300X。

**参考资料：**

- [MiMo-V2.5官方页面](https://mimo.xiaomi.com/mimo-v2-5/)
- [MiMo-V2.5-Pro官方页面](https://mimo.xiaomi.com/mimo-v2-5-pro/)
- [XiaomiMiMo/MiMo-V2.5 on HuggingFace](https://huggingface.co/XiaomiMiMo/MiMo-V2.5)
- [Decrypt: MiMo-V2.5概述](https://decrypt.co/365184/xiaomi-mimo-2-5-pro-ai-see-hear-act-one-model)