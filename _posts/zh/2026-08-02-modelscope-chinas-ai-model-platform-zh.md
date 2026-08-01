---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ModelScope：中国的人工智能模型平台
translated: true
type: note
---

## 问题：ModelScope (modelscope.cn) 简介

## 回答

ModelScope 基本上是**中国的 Hugging Face Hub + Colab + Model API 平台**，由阿里巴巴达摩院/阿里云创建。它的目标是让 AI 模型更容易被发现、运行、微调、评估和部署。（[GitHub][1]）

网站：

[ModelScope](https://modelscope.cn/?utm_source=chatgpt.com)

核心概念：

```
Model-as-a-Service (MaaS)

        Models
          |
          v
     ModelScope Hub
          |
  ---------------------
  |         |          |
Inference  Fine-tune  Deploy
  |         |          |
Apps      Training    API
```

（[GitHub][1]）

## 1. Model Hub（类似 Hugging Face）

最大的部分是 Model Repository。

你可以找到：

* LLMs

  * Qwen family
  * DeepSeek
  * GLM
  * MiniCPM
  * Llama variants

* Vision models

  * image generation
  * OCR
  * detection
  * segmentation

* Speech models

  * ASR
  * TTS

* Multimodal models

类似于：

```
Hugging Face Hub

      vs

ModelScope ModelHub
```

ModelScope 提供 model cards、versions、downloads 和 community sharing。（[ModelScope][2]）

示例：

```bash
pip install modelscope
```

下载模型：

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    "Qwen/Qwen2.5-7B-Instruct"
)

print(model_dir)
```

然后可以配合以下工具使用：

* transformers
* vLLM
* llama.cpp
* custom inference

---

## 2. Dataset Hub

类似于 Hugging Face Datasets。

包含：

* NLP datasets
* CV datasets
* speech datasets
* multimodal datasets

示例：

```
Dataset
   |
   |
train.py
   |
   v
Fine-tune LLM
```

可用于：

* SFT
* LoRA
* QLoRA
* evaluation datasets

（[ModelScope][2]）

---

## 3. Training / Fine-tuning

ModelScope 提供以下相关工具：

* model training
* evaluation
* fine-tuning

尤其是：

* LLM fine-tuning
* instruction tuning
* parameter-efficient tuning

例如：

```
Qwen-7B

     +
     
your company data

     |
     v

LoRA adapter

     |
     v

domain assistant
```

（[ModelScope][3]）

---

## 4. Notebook / GPU Environment

ModelScope 还提供在线 Notebook。

可以理解为：

```
Google Colab

        +
        
AI model marketplace
```

你可以直接在平台上运行实验，无需准备自己的机器。（[ModelScope][2]）

---

## 5. ModelScope Library

Python SDK 提供了统一的 API。

以前你可能需要：

```python
# different APIs for every model
model_a.load()
model_b.load()
model_c.load()
```

ModelScope 尝试提供统一的接口：

```python
from modelscope import pipeline

pipe = pipeline(
    task="text-generation",
    model="Qwen/Qwen2.5-7B-Instruct"
)

result = pipe("Explain CUDA kernels")
```

一个接口适用于多种模型。

（[GitHub][1]）

---

## 6. 与 Hugging Face 的关系

简单对比：

|                | Hugging Face              | ModelScope                         |
| -------------- | ------------------------- | ---------------------------------- |
| 公司           | Hugging Face              | Alibaba                            |
| 主要用户       | 全球 AI 社区              | 中国+全球                          |
| 模型           | 庞大                      | 庞大                               |
| 数据集         | 强大                      | 强大                               |
| LLM 生态       | 强大                      | 强大（尤其是 Qwen 生态）           |
| GPU Notebook   | Spaces/Colab 集成         | 内置 Notebook                      |
| 中文模型       | 可用                      | 通常是优先支持                     |

（[Hugging Face][4]）

---

## 7. 对于构建 LLM 基础设施的人（你的方向）

ModelScope 值得关注，因为它位于整个技术栈之上：

```
                 Application
                     |
                  Agent
                     |
                 vLLM
                     |
             Transformers
                     |
              Model weights
                     |
             ModelScope Hub
                     |
              Dataset / Eval
```

你可以利用它来：

### 探索模型

```bash
modelscope download \
  --model Qwen/Qwen2.5-7B-Instruct
```

### 微调

```
Qwen
 |
 + LoRA
 |
 + private data
 |
 v
specialized model
```

### 部署

```
ModelScope model
        |
        v
vLLM server
        |
        v
OpenAI-compatible API
```

考虑到你当前的工作（nanoGPT、nano-vLLM、Qwen 实验），了解 ModelScope 是值得的，因为它代表了 AI 生态中的模型分发层：

```
Linux        -> package managers
GitHub       -> source code
Docker Hub   -> containers
Hugging Face -> AI models
ModelScope   -> AI models + China ecosystem + services
```

参考：

* [ModelScope Docs](https://modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AF%BC%E5%87%BA?utm_source=chatgpt.com)
* [ModelScope GitHub](https://github.com/modelscope/modelscope?utm_source=chatgpt.com)
* [Alibaba Cloud launches ModelScope](https://www.alibabagroup.com/en-US/document-1525026652642344960?utm_source=chatgpt.com)

[1]: https://github.com/modelscope/modelscope?utm_source=chatgpt.com "GitHub - modelscope/modelscope: ModelScope: bring the notion of Model-as-a-Service to life. · GitHub"
[2]: https://www.modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E5%BA%93%E4%BB%8B%E7%BB%8D?utm_source=chatgpt.com "Docs · ModelScope"
[3]: https://modelscope.cn/docs/%E6%A8%A1%E5%9E%8B%E7%9A%84%E5%AF%BC%E5%87%BA?utm_source=chatgpt.com "Docs · ModelScope"
[4]: https://huggingface.co/modelscope?utm_source=chatgpt.com "modelscope (modelscope)"
