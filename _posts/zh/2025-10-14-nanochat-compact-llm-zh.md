---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: NanoChat紧凑型全栈大语言模型
translated: true
type: note
---

### 什么是 NanoChat？

NanoChat 是一个紧凑的全栈大语言模型（LLM）系统实现，类似于 ChatGPT，构建在单一、极简的代码库中，易于修改且依赖极少。由 Andrej Karpathy（以其在 AI 领域的贡献而闻名，如 nanoGPT）创建，它旨在在 affordable 的硬件上（如单个 8xH100 GPU 节点）运行完整的 LLM 流程——从分词和预训练到微调、评估、推理，甚至包括一个简单的 Web UI 用于与模型聊天。

它被定位为“100 美元能买到的最佳 ChatGPT”，作为预算友好的 LLM 开发（总成本低于 1000 美元）的基准。这使其成为 Eureka Labs 即将推出的 LLM101n 课程的毕业项目，强调简单性而非复杂配置。

### 主要特性

- **端到端流程**：用约 2000 行代码处理所有内容（依赖项文件 `uv.lock` 很小）。在约 24 美元/小时的 8xH100 设置上，约 4 小时训练出一个性能不错的模型，计算量为 4e19 FLOPs。
- **类 ChatGPT 的 UI**：训练完成后，启动 Web 服务器即可像使用真正的 ChatGPT 一样与模型交互。
- **评估报告**：自动生成 `report.md`，包含在 ARC-Challenge、GSM8K、HumanEval、MMLU 等任务上的基准分数。例如，一个 100 美元运行的示例显示了各阶段（BASE、MID、SFT、RL）的逐步改进：

| 指标           | BASE   | MID    | SFT    | RL     |
|----------------|--------|--------|--------|--------|
| CORE           | 0.2219 | -      | -      | -      |
| ARC-Challenge  | -      | 0.2875 | 0.2807 | -      |
| ARC-Easy       | -      | 0.3561 | 0.3876 | -      |
| GSM8K          | -      | 0.0250 | 0.0455 | 0.0758 |
| HumanEval      | -      | 0.0671 | 0.0854 | -      |
| MMLU           | -      | 0.3111 | 0.3151 | -      |
| ChatCORE       | -      | 0.0730 | 0.0884 | -      |

（总时间：完整运行约 3 小时 51 分钟。）

- **硬件灵活性**：可在 Ampere 8xA100（较慢）、单 GPU（带自动梯度累积）或低 VRAM 设置上运行（通过调整批次大小）。使用原生 PyTorch；可通过调整适配其他设备。
- **数据源**：从 Hugging Face 数据集（如 FineWeb 和 SmolTalk）中获取数据。
- **额外功能**：包括测试（例如，用于基于 Rust 的分词器），并且易于打包整个代码库（约 330KB）以便与其他 LLM 一起查询。

它受到 Karpathy 早期 nanoGPT 项目和 modded-nanoGPT 的启发，但扩展为完整的聊天体验。

### 如何开始

最快的方法是使用 `speedrun.sh` 脚本，它在 8xH100（例如，通过 Lambda Labs）上端到端处理 100 美元级别的模型：

1. 启动一个 8xH100 实例并克隆代码库。
2. 运行：

    ```
    bash speedrun.sh
    ```

    （或在 screen 会话中运行以记录日志：`screen -L -Logfile speedrun.log -S speedrun bash speedrun.sh`。使用 Ctrl+A+D 分离并 tail 日志。）

3. 完成后（约 4 小时），激活环境（`source .venv/bin/activate`）并启动 UI 服务：

    ```
    python -m scripts.chat_web
    ```

    打开本地 URL（例如 <http://your-ip:8000）与您的模型聊天。检查> `report.md` 查看结果。

对于更大的模型（例如，300 美元级别，约 12 小时，在某些分数上超越 GPT-2），编辑 `speedrun.sh` 以下载更多数据分片并调整深度/批次大小。运行测试如 `python -m pytest tests/test_rustbpe.py -v -s`。

它是 MIT 许可的，并开放贡献以推动微型模型的进一步发展。有关详细指南，请查看代码库的 Discussions 部分。

[nanoChat GitHub 代码库](https://github.com/karpathy/nanochat)
