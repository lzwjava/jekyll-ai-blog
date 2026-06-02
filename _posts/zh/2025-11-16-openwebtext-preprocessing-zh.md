---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenWebText数据集预处理脚本
translated: true
type: note
---

### 概述

该Python脚本用于处理包含OpenWebText数据集的大型文本文件（这是一个网络抓取文本语料库，类似于用于训练GPT-2等模型的数据）。其目标是：

- 将原始文本分割成可管理的"文档"（文本块）
- 创建Hugging Face的`Dataset`对象以便于处理
- 使用TikToken中的GPT-2字节对编码（BPE）分词器对文本进行分词（忽略特殊标记并添加文本结束标记）
- 将数据集分割为训练集（99.95%）和验证集（0.05%）
- 使用NumPy的内存映射数组将分词后的数据保存为紧凑的二进制文件（`train.bin`和`val.bin`）。这些文件存储token ID序列（作为16位整数），以便在机器学习训练期间高效加载

该脚本针对多核系统效率进行了优化，在分词时使用多进程处理。其设计灵感来自Flash Attention代码库中的数据加载模块（代码中已链接），该模块处理语言模型训练的类似预处理。注意：OpenWebText数据量巨大（约40GB未压缩），但本脚本假设已预下载本地的`openwebtext.txt`文件。输出文件小得多：`train.bin`约17GB（90亿个token），`val.bin`约8.5MB（440万个token）。

脚本开始时打印代理设置（可能是为了调试任何隐式下载时的网络问题，尽管此处没有显式下载）。默认使用8个工作进程进行分词。

### 逐步分解

#### 1. 导入和初始设置

```python
import os
import tarfile
from tqdm import tqdm
import numpy as np
import tiktoken
from huggingface_hub import hf_hub_download
from datasets import load_dataset # huggingface datasets
import datasets

print("HTTP_PROXY:", os.getenv("HTTP_PROXY"))
print("HTTPS_PROXY:", os.getenv("HTTPS_PROXY"))

# .map()调用中的工作进程数
# 建议使用约CPU核心数//2的值
num_proc = 8

# load_dataset()调用中的工作进程数
# 最佳数值可能与上面的num_proc不同，因为它还取决于网络速度
# 但通常比1更好
num_proc_load_dataset = num_proc

enc = tiktoken.get_encoding("gpt2")

datasets.logging.set_verbosity_info()
```

- **目的**：导入用于文件处理（`os`、`tarfile`）、进度条（`tqdm`）、数值操作（`numpy`）、分词（`tiktoken`）和Hugging Face工具（`huggingface_hub`、`datasets`）的库
- **代理打印**：记录HTTP/HTTPS代理的环境变量，在脚本遇到网络限制时很有用（例如用于下载分词器模型，尽管TikToken内部处理此问题）
- **工作进程**：设置`num_proc=8`用于分词中的并行处理（大约一半CPU核心数以保持平衡）。`num_proc_load_dataset`与其匹配但此处未使用（来自灵感代码的遗留，该代码从Hugging Face加载）
- **编码器**：加载GPT-2 BPE分词器（`enc`）。这将文本转换为整数token ID（0–50,256范围）
- **日志记录**：将Hugging Face数据集日志记录设置为"info"级别，以便在处理期间获得详细输出

`if __name__ == '__main__':`保护确保主逻辑仅在脚本直接执行时运行（而不是导入时）

#### 2. 读取和分割文本文件

```python
if __name__ == '__main__':
    # 读取本地openwebtext.txt文件
    txt_file = os.path.join(os.path.dirname(__file__), 'openwebtext.txt')
    print(f"从本地文件读取: {txt_file}")

    # 读取文本内容
    texts = []
    with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
        # 读取整个文件
        full_text = f.read().strip()

        # 首先尝试通过双换行符分割成文档
        documents = full_text.split('\n\n')

        # 如果只得到一个文档，通过单换行符分割
        if len(documents) <= 1:
            documents = full_text.split('\n')

        # 如果仍然只有一个文档，通过句点加空格分割
        if len(documents) <= 1:
            # 在句点加空格处分割，然后将句子重新连接
            sentences = full_text.split('. ')
            # 将句子分组为每个文档约100句的块
            chunk_size = 100
            for i in range(0, len(sentences), chunk_size):
                chunk = '. '.join(sentences[i:i+chunk_size])
                if chunk.strip():
                    texts.append(chunk.strip() + '.')
        else:
            # 处理从双/单换行符分割得到的文档
            for doc in documents:
                doc = doc.strip()
                if doc:  # 仅添加非空文档
                    texts.append(doc)

        print(f"从文本文件创建了{len(texts)}个文档")
```

- **文件读取**：以UTF-8模式打开`openwebtext.txt`（假设与脚本在同一目录），忽略编码错误。将整个内容读入`full_text`并去除空白字符
- **分割逻辑**：尝试将文本分割为"文档"（逻辑块，如段落或文章）：
  - **主要**：通过双换行符（`\n\n`）分割，这在语料库中分隔文档很常见
  - **回退1**：如果产生≤1个块（例如无双换行符），通过单换行符（`\n`）分割用于基于行的文本
  - **回退2**：如果仍然≤1个块（例如单个文本块），通过`.`（句点+空格）分割成句子，然后将每100个句子分组为一个"文档"块。这防止单个条目过长。为完整性在每个块末尾添加句点
- **输出**：将非空、去除空白字符的文档存储在`texts`列表中。打印创建的总数（例如，子集的10k个示例）
- **为何如此**？OpenWebText是网页的串联，因此分割创建了不仅仅是原始转储的训练示例。这模仿了BookCorpus等数据集的处理方式

#### 3. 创建和分割数据集

```python
    # 从文本创建数据集
    dataset = datasets.Dataset.from_dict({'text': texts})

    # 从10k示例创建训练/验证分割
    split_dataset = dataset.train_test_split(test_size=0.0005, seed=2357, shuffle=True)
    split_dataset['val'] = split_dataset.pop('test') # 将测试分割重命名为val
```

- **数据集创建**：将`texts`列表包装到具有单列`'text'`的Hugging Face `Dataset`中。这使得能够进行高效的并行操作，如映射
- **分割**：使用`train_test_split`分为训练集（99.95%）和测试集（0.05%）。小验证集大小对于巨大数据集是故意的——足够评估而不浪费计算
  - `test_size=0.0005`：0.05%用于验证（例如，从100k中约50个示例）
  - `seed=2357`：固定随机种子以确保可重现性
  - `shuffle=True`：在分割前随机化
- **重命名**：弹出`'test'`并重命名为`'val'`。现在`split_dataset`是具有`'train'`和`'val'`键的字典，每个都是`Dataset`对象

#### 4. 分词函数

```python
    # 现在想要对数据集进行分词。首先定义编码函数（gpt2 bpe）
    def process(example):
        ids = enc.encode_ordinary(example['text']) # encode_ordinary忽略任何特殊标记
        ids.append(enc.eot_token) # 添加文本结束标记，例如gpt2 bpe的50256
        # 注意：我认为eot应该前置而不是追加...嗯。但它被称为"eot"...
        out = {'ids': ids, 'len': len(ids)}
        return out
```

- **目的**：将文本转换为模型输入的token ID
- **`encode_ordinary`**：将文本字符串分词为整数列表（GPT-2词汇表）。忽略文本中的任何非标准标记
- **追加EOT**：在末尾添加文本结束标记（GPT-2的ID 50256）。这在训练期间标记序列边界。（注释指出了前置与追加的潜在争议，但追加在因果LM设置如GPT中很常见）
- **输出**：返回带有`'ids'`（token ID列表）和`'len'`（序列长度，用于后续求和）的字典

#### 5. 应用分词

```python
    # 对数据集进行分词
    tokenized = split_dataset.map(
        process,
        remove_columns=['text'],
        desc="tokenizing the splits",
        num_proc=num_proc,
    )
```

- **映射**：使用并行工作进程（`num_proc=8`）将`process`应用于训练/验证数据集中的每个示例
- **`remove_columns=['text']`**：删除原始文本以节省内存（现在只需要token）
- **进度**：通过`desc`显示进度条。由于编码，此步骤对于大型数据集可能耗时

#### 6. 将分词数据保存到二进制文件

```python
    # 将每个数据集中的所有id连接成一个大文件，可用于训练
    for split, dset in tokenized.items():
        arr_len = np.sum(dset['len'], dtype=np.uint64)
        filename = os.path.join(os.path.dirname(__file__), f'{split}.bin')
        dtype = np.uint16 # （可以这样做因为enc.max_token_value == 50256 < 2**16）
        arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

        # 基于数据集大小使用自适应批处理大小
        total_batches = min(1024, len(dset))
        if total_batches < 1024:
            print(f"对{split}数据集使用{total_batches}个批次（大小：{len(dset)}）")

        idx = 0
        for batch_idx in tqdm(range(total_batches), desc=f'写入{filename}'):
            # 仅当此批次索引对数据集大小有效时处理
            if batch_idx < len(dset):
                # 将样本批处理在一起以加快写入速度
                batch = dset.shard(num_shards=total_batches, index=batch_idx, contiguous=True).with_format('numpy')
                arr_batch = np.concatenate(batch['ids'])
                # 写入mmap
                arr[idx : idx + len(arr_batch)] = arr_batch
                idx += len(arr_batch)
        arr.flush()
```

- **循环分割**：对于`'train'`和`'val'`，通过求和`'len'`字段计算总token数（`arr_len`）
- **内存映射数组**：创建NumPy memmap文件（`train.bin`或`val.bin`）作为uint16整数的可写数组（适合GPT-2的50,256最大token值；比int32节省约50%空间）。形状是1D：`(total_tokens,)`
- **批处理以提高效率**：将数据集分割为最多1024个分片（`total_batches`）以避免一次性将所有内容加载到RAM中。对于小数据集（<1024示例），使用确切数量
  - **`shard`**：将数据集分割为连续批次（此处不洗牌）
  - **`with_format('numpy')`**：将批次转换为NumPy数组以快速连接
- **写入**：连接每个批次的token ID，并从`idx`开始顺序复制到memmap数组中。使用`tqdm`跟踪进度
- **`flush()`**：确保所有数据写入磁盘
- **为何二进制/memmap？** 这些文件巨大但可流式传输。在训练期间，您可以使用`np.memmap('train.bin', dtype=np.uint16, mode='r')`加载它们，而无需将所有内容加载到内存中

#### 7. 输出和使用说明的注释

```python
    # train.bin约17GB，val.bin约8.5MB
    # train有约90亿个token（9,035,582,198）
    # val有约440万个token（4,434,897）

    # 以后读取bin文件，例如使用numpy：
    # m = np.memmap('train.bin', dtype=np.uint16, mode='r')
```

- 这些是完整OpenWebText的示例大小（您的本地文件可能不同）
- **读取提示**：使用memmap进行只读访问。在训练循环中，您可以从平面数组采样随机起始索引并读取固定长度序列（例如1024个token）

### 潜在问题和注意事项

- **内存使用**：对于非常大的文件（40GB+），将完整`openwebtext.txt`读入RAM可能失败。如果需要，考虑流式读取
- **EOT放置**：注释质疑追加与前置EOT；实际上，追加对于自回归模型有效（它在内容之后标记结束）
- **自定义**：假设本地文件；灵感代码从Hugging Face下载，但此版本本地读取（更快，无需认证）
- **依赖**：需要`tiktoken`、`datasets`、`numpy`、`tqdm`。如果缺少，通过pip安装
- **可扩展性**：对于真实的OpenWebText，在具有64GB+ RAM和快速存储（SSD）的机器上运行。10k示例分割表明这可能用于子集

此脚本将原始文本转换为训练就绪的格式，针对像GPT这样的语言模型进行了优化。如果您对修改它有疑问（例如不同的分词器或块大小），请告诉我！
