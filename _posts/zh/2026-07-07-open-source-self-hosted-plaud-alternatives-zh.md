---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源自托管的Plaud替代方案
translated: true
type: note
---

**问题：** Plaud 可以在哪些方面做得更好？它是开源的吗？有没有一个开源、可自托管的“Plaud”——类似于 Dify/n8n 在各自领域中的地位？

**回答：**

## Plaud 可以在哪些方面做得更好

Plaud 的弱点大多属于结构性问题，而非硬件问题：

1. **订阅锁定，而推理本可自行运行。** 该设备只是一个笨重的录音机——设备本身没有任何 AI 处理能力；音频会传输到 Plaud 应用，而该应用是“整个操作的大脑”。你实际上是在为 Whisper + GPT 的调用支付循环费用，而这些调用按 API 价格计算成本极低。你可以在一个下午就用完整个月的免费转录额度，然后需要购买附加包；年度套餐价格为 79 美元/年，包含每月 1,200 分钟的转录时长，额外的 6,000 分钟包价格为 89 美元。对比一下：通过 Groq Whisper 处理 20 小时音频的一次性成本约为 2.22 美元（0.11 美元/小时），而 Plaud Pro 约为 0.90 美元/小时。这意味着在通用推理服务上的加价率约为 8 倍。

2. **封闭的生态系统 / 不支持自带 API 密钥、无本地处理流程。** 你可以从 Plaud 设备上传录音，但奇怪的是却不能从手机或笔记本电脑上传——尽管 Plaud 提供了桌面和移动应用。没有官方方法将其指向你自己的 Whisper 端点或你自己的 LLM。

3. **准确性不透明。** Plaud 未公布任何关于转录准确性的统计数据或细节。

4. **隐私问题。** 你的原始会议音频会通过其云端（Azure）传输。对于你的目标客户——银行、香港企业——这通常是一个绝对的禁区。这恰恰是你的咨询服务可以利用的差距。

5. **不支持实时转录。** 因为这是一个物理录音机，所以无法进行实时转录——你需要上传并等待，而且蓝牙同步速度很慢（传输一个 70 分钟的录音需要 10 多分钟；WiFi 则快得多）。

## Plaud 是开源的吗？

不是。固件、应用和云端处理流程都是专有的。这个领域的大多数产品都是商业化的；目前还没有广泛可用的、匹配 Plaud 易用性的开源硬件录音机。其护城河在于精心打磨的硬件 + 应用用户体验，而不是 AI 本身。

## 开源/自托管格局（“录音机领域的 Dify/n8n”）

**软件层（与 Plaud 设备配合使用）：**

* **Riffado**（原名 OpenPlaud）——最接近你描述的工具。一个开源（AGPL-3.0 协议）的自托管 Plaud 设备配套应用：使用 Docker Compose 堆栈，连接到你的 Plaud 账户，自带 AI 提供商。可在你的笔记本电脑、NAS 或 VPS 上运行，可接入 OpenAI、Groq 或 Ollama——或通过 Transformers.js Whisper 在浏览器中免费转录——存储到本地磁盘、R2、B2 或 S3，并导出为 JSON、TXT、SRT、VTT 格式。这简直就是“针对 Plaud 的 Dify”：保留硬件，替换云端。
* **Applaud**——一个自托管的 Plaud 替代品：从 iCloud/Google Drive 同步音频，使用 insanely-fast-whisper（支持 CUDA 和 MPS）进行转录，使用你选择的模型（包括本地 Ollama）进行摘要生成，生成抽认卡和问答。在配备 RTX 4070 的机器上运行良好。

**完全开源硬件 + 软件：**

* **Omi (BasedHardware)**——真正的开源竞争对手。完全开源：可穿戴设备 + Flutter 移动应用 + macOS 应用 + Python 后端，支持实时转录、摘要、行动项和记忆聊天。其后端是你已经熟悉的一套技术栈：Python/FastAPI、Firebase、Pinecone、Redis、Deepgram/Speechmatics/Soniox 语音转文字、兼容 OpenAI 的 API、LangChain、Silero VAD。注意事项：他们的参考部署依赖云服务（Deepgram、Firestore），因此“自托管”意味着将这些服务替换为 whisper.cpp/faster-whisper + Postgres——可行，但需要实际工作。

**DIY 最大化方案：** ESP32-S3 / XIAO 开发板 + I2S MEMS 麦克风 + BLE 连接 -> 手机/服务器 -> 在你的 4070 上运行 faster-whisper -> 本地 LLM 摘要。Omi 的固件仓库是实现此方案的参考实现。

## 处理流程可轻易复现

整个 Plaud 的“AI”后端只需约 25 行代码，即可在你的 4070 工作站上运行：

```python
# pip install faster-whisper openai
from faster_whisper import WhisperModel
from openai import OpenAI
import sys

model = WhisperModel("large-v3", device="cuda", compute_type="float16")
segments, info = model.transcribe(sys.argv[1], vad_filter=True)
transcript = "\n".join(f"[{s.start:.0f}s] {s.text}" for s in segments)

llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # 或 DeepSeek API
resp = llm.chat.completions.create(
    model="qwen3:14b",
    messages=[
        {"role": "system", "content": "生成：1) 摘要 2) 关键决策 3) 带负责人的行动项。"},
        {"role": "user", "content": transcript},
    ],
)
print(resp.choices[0].message.content)
```

添加 pyannote 用于说话人分离，你就拥有了与 Plaud 相当的功能集，只是缺少硬件部分。在 fp16 精度下，large-v3 模型可以轻松适配 12GB 显存。

## 给你的战略建议

这个市场中的空白直接对应了你第一阶段的理论：企业（尤其是金融行业，正是你的银行业背景所在）需要会议智能，但无法将音频发送到 Plaud/Otter 等云端。一个自托管、本地化的“Plaud 后端”——通用录音机或 Omi 硬件 + faster-whisper + 本地 MoE 模型用于摘要 + 基于转录档案的 RAG 系统——对于粤港澳大湾区和香港客户来说，是一个清晰的咨询业务机会。Riffado 使用的 AGPL 许可证也暗示了可行的商业模式：开放核心 + 每月 5 美元托管版本。硬件已经商品化；可防御的层面是私有推理流程和“搜索我说过的一切”记忆系统——而这正是智能体领域，是你的主场。

**参考资料：**

* [Riffado (原名 OpenPlaud) — GitHub](https://github.com/openplaud/openplaud)
* [Riffado — 定价/架构](https://openplaud.com/)
* [Applaud — 自托管的 Plaud 替代品](https://github.com/landoncrabtree/applaud)
* [Omi — BasedHardware 开源 AI 可穿戴设备](https://github.com/BasedHardware/omi)
* [Plaud 替代品分析 (Notta)](https://www.notta.ai/en/blog/plaud-alternatives)
* [Plaud Note 实际使用问题 (BlueDot)](https://www.bluedothq.com/blog/plaud-alternatives)
