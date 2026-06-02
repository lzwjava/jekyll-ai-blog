---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复数据集划分错误
translated: true
type: note
---

该错误出现的原因是您的本地数据集文件（`/home/lzw/projects/nanoGPT/data/openwebtext_local/openwebtext.txt`）仅包含1个样本（可能只有单行内容或近似空文件），但脚本尝试以 `test_size=0.1` 的比例将其分割为训练/测试集。这将分配约0.1个样本给测试集（四舍五入为1个样本），导致训练集为0，而 `datasets.train_test_split()` 会拒绝这种情况以避免训练集为空。

### 快速解决方案
1. **使用更大/更完整的数据集**：
   - nanoGPT的OpenWebText预处理预期需要大量语料（数百万文档）。您的本地 `openwebtext.txt` 似乎不完整——可能只是占位符或下载失败。
   - 下载合适的OpenWebText样本或子集：
     - 克隆OpenWebText仓库：`git clone https://github.com/jcpeterson/openwebtext.git` 到 `data/openwebtext_local/` 目录
     - 或使用Hugging Face的预处理版本：安装 `datasets` 库（`pip install datasets`），然后修改 `prepare.py` 通过 `load_dataset("openwebtext", split="train")` 加载数据而非本地文件
     - 测试时可创建包含至少10+行示例文本的多行虚拟文件（例如重复多行"Hello world."）以通过分割检查

2. **修改 `prepare.py` 中的分割逻辑**（约第50行）：
   - 如果必须使用此微型文件进行调试，可修改分割参数：
     ```python
     # 原始代码（会报错）：
     split_dataset = dataset.train_test_split(test_size=0.1, seed=2357, shuffle=True)

     # 方案A：完全跳过分割（无测试集，全部用于训练）：
     split_dataset = {"train": dataset}  # 或设置 test_size=0

     # 方案B：针对n=1情况使用更小的test_size（例如0，或处理微型数据集）：
     if len(dataset) <= 1:
         split_dataset = {"train": dataset}
     else:
         split_dataset = dataset.train_test_split(test_size=0.1, seed=2357, shuffle=True)
     ```
   - 重新运行：`python data/openwebtext_local/prepare.py`

3. **验证数据集大小**：
   - 在 `prepare.py` 的分割代码前添加打印语句（约第45行）：
     ```python
     print(f"数据集大小: {len(dataset)}")
     ```
   - 再次运行确认——应输出 `1`。如果文件为空/损坏，请重新生成或检查文件权限/编码（要求UTF-8编码）

### nanoGPT推荐后续步骤
- 完整训练请遵循nanoGPT官方数据准备指南：参考[nanoGPT说明文档](https://github.com/karpathy/nanoGPT#data)下载/准备Shakespeare或OpenWebText数据集。OpenWebText需要较大存储空间（约40GB未压缩）
- 若为本地测试，可切换至内置Shakespeare数据集（更小且无需外部下载）：编辑 `prepare.py` 加载 `load_dataset("tiny_shakespeare")` 或使用nanoGPT的 `data/shakespeare_char/prepare.py`
- 确保依赖项完整：`pip install datasets torch`（及nanoGPT的 `requirements.txt` 中的其他依赖）

如果您能提供 `prepare.py` 的更多代码或文件内容，我可以提供修补版本。
