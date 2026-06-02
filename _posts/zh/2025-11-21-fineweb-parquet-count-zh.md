---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: FineWeb数据集Parquet文件数量
translated: true
type: note
---

**FineWeb** 数据集（HuggingFaceFW/fineweb 上的 15T+ 词元英文版本）总共包含**约 35,000 至 50,000** 个 `.parquet` 文件。

### 详细说明

- 它包含 **96** 个独立的 Common Crawl 快照（数据转储，例如 `CC-MAIN-2013-20`、`CC-MAIN-2024-10` 等）。
- 每个数据转储都存储在 `/data/` 下的独立子目录中，并分割成许多分片的 `.parquet` 文件，命名格式为 `000_00000.parquet`、`000_00001.parquet`……（零填充，顺序编号）。
- 每个数据转储的 parquet 文件数量因其大小而异：
  - 较小/较早的数据转储（如您脚本中的 `CC-MAIN-2013-20` 示例）通常有 **约 200–1,000** 个文件。
  - 较大的近期数据转储每个可以有**数千个**文件。
- 虽然没有单一官方公布的总数，但根据社区估算以及从数据转储大小/词元计数进行的计算，**所有 96 个数据转储的总文件数 consistently 约为 35k–50k** 个 parquet 文件（完整数据集未压缩时约为 45–53 TB）。

您的脚本下载的是非常小的 `CC-MAIN-2013-20` 数据转储中的第 11 到第 20 个分片（10 个文件），而该数据转储本身的总分片数远多于此——仅该数据转储就有数百个分片。

如果您想获得确切的数量，可以使用 Hugging Face Hub API（例如，使用 `huggingface_hub.list_repo_files`）以编程方式计算，但上述大致数字是人们通常在下载或处理完整数据集时使用的。

[FineWeb 数据集卡片](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
[FineWeb 数据树（示例数据转储）](https://huggingface.co/datasets/HuggingFaceFW/fineweb/tree/main/data)
