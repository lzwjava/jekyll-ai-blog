---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 通过Hugging Face下载OpenWebText子集
translated: true
type: note
---

您提到的数据集托管在 Hugging Face 平台，仓库 ID 为 `Skylion007/openwebtext`。其中特定文件 `subsets/urlsf_subset00.tar` 可公开访问（无需认证），您可以使用 Hugging Face CLI 工具（`huggingface-cli`）进行下载。具体操作如下：

### 环境准备
- 若未安装 Hugging Face Hub CLI，请先执行：
  ```
  pip install huggingface_hub
  ```
- （可选）如果您的系统已将 `huggingface-cli` 命令简写为 `hf`，可直接使用该缩写。否则请使用完整的 `huggingface-cli` 前缀。

### 下载命令
在终端中运行：
```
huggingface-cli download Skylion007/openwebtext subsets/urlsf_subset00.tar --local-dir ./openwebtext
```
- 该命令会将文件下载至 `./openwebtext/subsets/urlsf_subset00.tar`（如不存在 `subsets` 子目录则会自动创建）
- 文件体积较大（约 1.5 GB，为 tar 压缩包格式），请确保磁盘空间充足且网络连接稳定
- 若希望直接下载至当前目录（不保留仓库目录结构），可添加 `--repo-type dataset` 参数（此处已隐含指定）或调整 `--local-dir` 参数

### Python 脚本方案（替代方案）
若倾向使用 Python 脚本（通过 `huggingface_hub` 库）：
```python
from huggingface_hub import hf_hub_download

# 下载至当前目录
hf_hub_download(
    repo_id="Skylion007/openwebtext",
    filename="subsets/urlsf_subset00.tar",
    local_dir="./openwebtext",  # 可选参数：指定基础目录
    repo_type="dataset"
)
```
请先安装该库：`pip install huggingface_hub`

### 注意事项
- 这是 OpenWebText（大型网络语料库）的子集。下载完成后需解压 tar 文件（例如执行 `tar -xvf subsets/urlsf_subset00.tar`）
- 若下载失败（如因网络问题），请重试或使用 `--cache-dir` 参数指定自定义缓存路径
- 如需完整数据集或其他子集，请访问仓库页面：https://huggingface.co/datasets/Skylion007/openwebtext

若遇到错误，请提供终端输出以便排查问题！
