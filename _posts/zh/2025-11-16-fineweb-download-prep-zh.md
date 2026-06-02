---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: FineWeb数据集下载与预处理
translated: true
type: note
---

### 下载 Parquet 文件

您提供的 URL 指向 FineWeb 数据集（CommonCrawl 数据的清洗子集）中的特定 Parquet 文件。该文件（来自 `CC-MAIN-2013-20` 转储的 `000_00000.parquet`）包含约 100 万行英文网页文本，每行都包含一个已经为语言模型训练预处理的 `text` 列（已去除 HTML、去重，并通过 Trafilatura 等工具进行质量过滤）。

下载方式：
- 使用 Hugging Face CLI：`huggingface-cli download HuggingFaceFW/fineweb data/CC-MAIN-2013-20/000_00000.parquet --local-dir ./fineweb_data`
- 或通过 Python 使用 `huggingface_hub`：
  ```python
  from huggingface_hub import hf_hub_download

  file_path = hf_hub_download(
      repo_id="HuggingFaceFW/fineweb",
      filename="data/CC-MAIN-2013-20/000_00000.parquet",
      local_dir="./fineweb_data"
  )
  print(f"下载至: {file_path}")
  ```
这将把约 500MB 的文件保存到本地（例如 `./fineweb_data/data/CC-MAIN-2013-20/000_00000.parquet`）。

如需完整转储（数百个文件），请按照数据集文档使用 `snapshot_download`，但建议先从此单个文件开始测试。

### 提取文本

FineWeb 的 `text` 列是可直接用于训练的纯文本——无需解析 HTML 或原始 HTML。使用 `pandas` 或 `pyarrow` 高效加载数据。方法如下：

1. **安装依赖项**（如需要）：`pip install pandas pyarrow datasets`（假设您已为 NanoGPT 设置环境）。

2. **加载 Parquet 文件并提取文本**：
   ```python
   import pandas as pd
   import os

   # 下载文件的路径
   parquet_path = "./fineweb_data/data/CC-MAIN-2013-20/000_00000.parquet"

   # 加载 Parquet 文件（对大文件高效）
   df = pd.read_parquet(parquet_path, columns=['text'])  # 仅加载文本列以节省内存

   # 将所有文本提取到列表中（如内存受限可迭代处理）
   texts = df['text'].tolist()  # 约 100 万个字符串的列表

   # 可选：基础清洗（FineWeb 已清洗过，但可标准化空白字符）
   import re
   def clean_text(text):
       if pd.isna(text):  # 跳过空值（FineWeb 中罕见）
           return ''
       text = re.sub(r'\s+', ' ', text.strip())  # 合并空白字符
       return text if len(text) > 10 else ''  # 过滤过短文本

   cleaned_texts = [clean_text(t) for t in texts if t]  # 应用过滤器

   print(f"已提取 {len(cleaned_texts)} 个文本样本")
   print("示例:", cleaned_texts[0][:200] + "...")  # 预览首段文本
   ```

   - **内存提示**：该文件约 100 万行，每段文本约 1-5k 字符。在 16GB 内存的机器上可正常加载。对于更大转储，使用 `pyarrow` 分块读取：
     ```python
     import pyarrow.parquet as pq

     table = pq.read_table(parquet_path, columns=['text'])
     texts = table['text'].to_pylist()
     ```

   - **流式传输方案**（无需完整下载）：使用 `datasets` 库迭代读取而不全量加载：
     ```python
     from datasets import load_dataset

     # 以流式模式加载特定转储
     dataset = load_dataset("HuggingFaceFW/fineweb", name="CC-MAIN-2013-20", split="train", streaming=True)

     texts = []
     for i, sample in enumerate(dataset):
         if i >= 100000:  # 测试时限制数量
             break
         texts.append(sample['text'])

     # 按上述方法清洗
     ```

### 准备 NanoGPT 训练数据

NanoGPT 需要单个文本文件（如 `input.txt`），其中包含用特殊标记（如 `"<|endoftext|>"`）分隔的拼接文档。按以下方式格式化提取的文本：

```python
# 从上述步骤获取 cleaned_texts 后
with open('input.txt', 'w', encoding='utf-8') as f:
    for text in cleaned_texts:
        f.write(text + "\n<|endoftext|>\n")  # NanoGPT 默认分隔符

print("已保存至 input.txt – 准备进行 NanoGPT 训练！")
```

- **为何采用此格式？** NanoGPT 的 `data.py` 脚本将读取 `input.txt`，使用分词器（如 GPT-2）进行编码，并创建训练/验证分割。每个文档以 `"<|endoftext|>"` 结尾以避免跨文档上下文干扰。
- **自定义选项**：
  - 按长度过滤：在写入前添加 `if 100 < len(text.split()) < 10000:` 以保留中等长度文档。
  - 测试子集：使用 `cleaned_texts[:10000]` 进行快速万样本测试。
  - 训练命令：准备好 `input.txt` 后，在 NanoGPT 中运行 `python train.py`（如需调整 `--dataset=input.txt`）。

此单个文件可提供约 50-100 亿个词元——非常适合微调。如需更多数据，可下载额外 Parquet 文件进行拼接。如遇内存问题或需要 NanoGPT 配置帮助，请提供具体细节！

**参考**：[FineWeb 数据集卡片](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
