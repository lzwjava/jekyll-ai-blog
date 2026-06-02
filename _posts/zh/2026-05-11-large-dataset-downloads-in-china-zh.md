---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中国大型数据集下载
translated: true
type: note
---

问题：在中国，有没有更好的方法下载像 FineWeb 这样的大型数据集，以及如何高效获取如此庞大的数据集？

答案：

在中国下载超大规模数据集（约100B token，数百GB）可能面临网络速度、限制以及 Hugging Face 等国际服务器的稳定性挑战。以下是一些实用方法：

---

### 1. **使用本地镜像或更快的服务器**

* Hugging Face 数据集通常有官方镜像，例如 `hf.co` 的亚洲镜像或 `huggingface-asia` 镜像。
* 你的脚本已支持 `--mirror hf-mirror`，在中国使用该镜像可能会显著提升速度。
* 检查是否有中国大学或开源社区本地托管 FineWeb 的分片数据。

---

### 2. **并行下载**

* 你当前的脚本按顺序下载分片。
* 使用 **`aiohttp`**、**`asyncio`** 或 **`aria2c`** 等工具进行多连接下载。
* 使用 `aria2c` 的示例：

  ```bash
  aria2c -x 16 -s 16 -i urls.txt
  ```

  其中 `urls.txt` 列出所有分片的 URL。这可以充分利用带宽并减少从镜像的下载时间。

---

### 3. **使用靠近镜像的云虚拟机或存储**

* 在 **新加坡、香港或邻近区域** 租用与 HF 镜像有高速连接的云虚拟机，通常比国内家庭网络更快。
* 在云虚拟机上下载数据集，压缩后通过高速传输工具（如 `rclone`、`rsync`）传输到本地机器。

---

### 4. **部分或增量下载**

* 不必一次性下载完整的约100B token（约400 GB），可以先选择部分子集进行实验。
* 你的 `select_shards()` 函数已支持按大小限制。建议从 5-10 个分片（约 20-40 GB）开始本地实验。

---

### 5. **使用数据托管服务**

* 一些中国用户会将数据集重新托管在 **百度云（Pan）**、**阿里云 OSS** 或 **腾讯云 COS** 上。可以在 GitHub 问题或论坛中搜索，有时存在非官方镜像。
* 使用非官方镜像时请注意合法性和许可证合规性。

---

### 6. **优化存储**

* Parquet 分片通常**可压缩**；可考虑下载 `.parquet` 文件并转换为 `.jsonl` 或其他压缩格式以节省空间。
* 你的 `BYTES_PER_TOKEN = 4` 是近似值；实际存储量可能因压缩而减少。

---

### 7. **自动断点续传下载**

* 你的 `download_one()` 函数已通过 `Range` 头支持断点续传下载。在中国使用时，结合重试和指数退避策略对稳定性至关重要。

---

**建议总结：**

1. 使用 `--mirror hf-mirror` 或邻近的亚洲镜像。
2. 考虑多线程下载（aria2 或 asyncio）。
3. 先从部分分片开始。
4. 使用靠近镜像的云虚拟机进行批量下载。
5. 利用断点续传功能避免重复失败。

---

参考资料：

* [Hugging Face 数据集文档](https://huggingface.co/docs/datasets/)
* [aria2 下载工具](https://aria2.github.io/)
* [FineWeb 数据集在 Hugging Face 上](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu)
