---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 运行VLA模型与机器人性能
translated: true
type: note
---

**问题：** 如何运行 VLA（Vision-Language-Action）模型，以及机器人的实际表现如何？

---

**回答：**

## 什么是 VLA 模型？

Vision-Language-Action 模型是一种 AI 系统，它处理摄像头输入、自然语言指令和机器人自身状态，然后输出电机指令——其视觉、语言和动作模块联合训练并在一次前向传播中运行，而不是传统的感知-规划-控制流水线。

三个核心组成部分是：
- **Vision encoder** —— 使用 DINOv2 + SigLIP 等模型处理原始摄像头帧（通常来自多个摄像头）
- **Language backbone** —— 使用预训练的 LLM（如 LLaMA 2、PaliGemma）对指令进行编码，例如“拿起红色方块”
- **Action decoder** —— 将融合后的表示转换为电机指令

---

## 主要 VLA 模型（2026）

以下是当前可用的主要开源模型对比：

| 模型 | 参数 | Action Head | 许可证 | 硬件 |
|-------|-----------|-------------|---------|----------|
| OpenVLA | 7B | Autoregressive tokens | MIT | A100/H100，或 24GB（4-bit 量化） |
| Octo | 27M / 93M | Diffusion policy | MIT | 单张 RTX 4090 |
| pi0 / pi0.5 / pi0.6 | 3.3B | Flow matching | 开放检查点 | 多 GPU 或单张 A100 |
| Gemini Robotics 1.5 | 未公开 | Hybrid cloud+edge | 封闭 | 依赖云端 |
| SmolVLA | 450M | Flow matching | Apache 2.0 | RTX 3060、Jetson 或笔记本 CPU |

---

## 如何运行 VLA 模型

### 选项 1 — 通过 LeRobot 使用 SmolVLA（最简单，可在消费级 GPU 上运行）

使用 HuggingFace 的 LeRobot 框架安装并微调 SmolVLA：

```bash
# Install
git clone https://github.com/huggingface/lerobot.git
cd lerobot
pip install -e .[smolvla]

# Fine-tune on your dataset
python lerobot/scripts/train.py \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=lerobot/svla_so101_pickplace \
  --batch_size=64 \
  --steps=20000 \
  --policy.device=cuda

# Run on a real robot
python -m lerobot.record \
  --robot.type=so101_follower \
  --robot.port=/dev/ttyACM0 \
  --dataset.single_task="Grasp a lego block and put it in the bin."
```

### 选项 2 — OpenVLA（研究基线）

OpenVLA 支持 LoRA 微调和 4-bit 量化。量化版本可在 24GB 的 RTX 4090 上运行。它在 29 个任务上以 16.5 个百分点的任务成功率优势击败了封闭的 RT-2-X 模型，尽管 RT-2-X 拥有 55B 参数，而 OpenVLA 只有 7B。

### 选项 3 — pi0 / openpi（最佳灵巧性）

openpi 仓库包含检查点和一个近似训练流程，并在超过 10,000 小时的机器人数据上进行了预训练。最适合双臂或 contact-rich 任务。

---

## 机器人的实际表现如何？

**优势：**
- VLA 对从未显式训练过的条件的泛化能力更强，因为底层 VLM 骨干在接触机器人演示之前，已经通过网络规模的预训练了解了杯子、毛巾或抽屉的外观。
- pi0 展示了双臂任务，如折叠衣物、打包杂货和组装箱子，其灵巧程度是前所未有的。
- Gemini Robotics 1.5 实现了 motion transfer——在一个机器人平台上训练的技能直接迁移到另一个机器人和人形机器人上，无需重新训练。

**局限性：**
- 任务中途恢复不一致——当抓取在中途滑落或物体移位时，模型会陷入困境，因为大多数演示数据只记录了成功的尝试。
- 让 7B 以上参数的模型在机器人自身硬件上以 10–100Hz 的频率运行，目前基本上仍未解决。大多数部署系统要么连接到边缘服务器，要么将推理与控制分离。
- 当前的 VLA 在训练分布内部泛化良好，但在分布之外性能明显下降。

**选择模型：**
- 消费级 GPU / 业余机械臂 → **SmolVLA**
- 双臂 / 高灵巧任务 → **pi0**
- 研究基线 → **OpenVLA**
- 计算资源受限 → **Octo**
- 前沿专有模型 → **Gemini Robotics 1.5**（不可自托管）

---

**参考文献：**
- [Vision-Language-Action 模型详解（DataCamp，2026 年 9 月）](https://www.datacamp.com/tutorial/vision-language-action-models-explained)
- [HuggingFace / LeRobot 上的 SmolVLA](https://huggingface.co/lerobot/smolvla_base)
- [openpi 仓库 — pi0 检查点](https://github.com/Physical-Intelligence/openpi)
- [OpenVLA 项目页面](https://openvla.github.io/)