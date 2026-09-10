---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从无审查到AI代理
translated: true
type: note
---

问题：**一旦你拥有一个未经审查/开源权重的模型，你实际应该用它做什么？**

答案：

有趣的部分**不仅仅是移除拒绝层**。真正的价值在于你现在控制了整个推理+训练流程。

我会把它当作一个小型研究/产品循环：

```text
未经审查的模型
      ↓
基准评估
      ↓
发现失败模式/能力
      ↓
SFT / LoRA / 偏好微调
      ↓
工具使用 + 智能体循环
      ↓
与 Qwen / Llama 等模型进行基准测试
      ↓
打包成有用的本地产品
```

### 1. 首先：明确“未经审查”的真正含义

对相同的提示词运行：

```text
原始模型
    vs
未经审查的模型
```

测量：

* 拒绝率
* 指令遵循能力
* 编码性能
* 推理能力
* 幻觉
* 上下文保持
* 工具调用
* 多语言行为
* 基准分数

不要假设“未经审查”=“更好”。通常模型只是一个具有不同行为偏好的微调版本。

### 2. 然后检查模型

对于 Hugging Face 模型：

```bash
git clone <MODEL_REPO>
cd <MODEL_REPO>

find . -maxdepth 2 -type f | sort
```

查看：

```text
config.json
tokenizer_config.json
generation_config.json
*.safetensors
README.md
```

特别注意：

```json
architectures
model_type
hidden_size
num_hidden_layers
num_attention_heads
num_key_value_heads
intermediate_size
torch_dtype
```

这告诉你实际运行的是什么。

### 3. 本地运行

例如：

```bash
pip install -U transformers accelerate torch
```

然后：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "<MODEL_ID>"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
)

prompt = "解释 TCP 拥塞控制的工作原理。"

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

out = model.generate(
    **inputs,
    max_new_tokens=512,
    temperature=0.7,
)

print(tokenizer.decode(out[0], skip_special_tokens=True))
```

然后，在你关心吞吐量时，切换到 **vLLM/SGLang**。

### 4. 真正有趣的事情：构建你自己的智能体

这是未经审查的模型比聊天机器人更有趣的地方。

给它：

```text
LLM
 ├── shell
 ├── 文件系统
 ├── Python
 ├── 浏览器
 ├── GPU 检查
 ├── git
 └── 你自己的 API
```

然后：

```text
用户
 ↓
LLM
 ↓
工具调用
 ↓
观察结果
 ↓
LLM
 ↓
工具调用
 ↓
...
 ↓
答案
```

对于你的场景，你可以创建一个**本地 GPU 修复智能体**：

```text
GPU
 ↓
nvidia-smi / lspci
 ↓
MATS/MODS 输出
 ↓
示波器测量
 ↓
照片
 ↓
LLM
 ↓
假设
 ↓
下一步测量
 ↓
LLM
 ↓
诊断
```

这比单纯向一个未经审查的模型提问有趣得多。

### 5. 然后微调它

使用你自己的高质量示例：

```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

从 LoRA/QLoRA 开始：

```text
基础模型
    +
你的数据
    ↓
适配器
    ↓
专用模型
```

你可能感兴趣的专业化方向：

* 编码智能体
* Linux/GPU 调试
* CUDA 工程
* 硬件修复推理
* 中英文技术知识
* 自主 CLI 智能体
* 长时间运行的研究智能体

### 6. 构建评估框架

这可能是下一步中杠杆率最高的。

不再使用：

```text
“我觉得这个模型很好。”
```

而是构建：

```bash
./eval.py \
    --model qwen \
    --model my-uncensored \
    --tasks coding,reasoning,agent,gpu
```

并生成：

```text
                     Qwen     我的模型
编码                 82        84
推理                 71        76
工具使用             78        91
拒绝率               35%       4%
GPU 诊断             41        67
```

现在你是在做**模型工程**，而不仅仅是下载模型。

### 重要的思维模型

一个未经审查的模型本质上是：

> **一个可控的实验基础，你拥有策略行为的控制权。**

最强的工作流程是：

```text
开放权重
    ↓
理解架构
    ↓
基准测试
    ↓
收集失败案例
    ↓
训练
    ↓
评估
    ↓
智能体化
    ↓
部署
```

而且因为你已经在使用 CLI 智能体、GPU、训练和推理基础设施，我个人建议直接转向**“未经审查的模型 + 本地工具 + 自主 CLI 智能体”**，而不是再建一个聊天界面。

接下来，我可以帮你用 vLLM/SGLang 在 Python 中构建一个简单的 `未经审查模型 → 工具调用 CLI 智能体`。
