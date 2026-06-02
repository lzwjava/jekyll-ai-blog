---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: OpenWebText数据集下载指南
translated: true
type: note
---

### 问题分析

`RepositoryNotFoundError` (401 客户端错误) 确认了 Hugging Face 上**不存在**名为 `openwebtext` 的仓库。这就是下载失败的原因——HF 在 `https://huggingface.co/openwebtext` 找不到该仓库。"Invalid username or password" 部分是 HF 认证层的通用回退消息，但此处无关紧要，因为该仓库根本不存在。OpenWebText（您尝试访问的数据集）是 GPT-2 时代的公共语料库，但并未作为标准仓库托管在 Hugging Face 上。相反，它通过镜像、种子或学术/GitHub 源的直接下载进行分发。

- **OpenWebText 背景**：创建用于复现 GPT-2 论文中使用的数据集（来自 Reddit Pushshift 转储中的 URL，并经过质量过滤）。完整语料库约 40GB 文本，被分割成子集，如 `urlsf_subset00.tar`（14 个压缩包之一，每个约 3-5GB）。这些压缩包包含用于训练 nanoGPT 等模型的原始文本文件。
- 无官方 HF 仓库：经查，在 `openwebtext` 或类似名称下没有完整子集的直接上传（例如，EleutherAI 有相关仓库但不包含原始数据）。HF 主要关注具有许可证的模型/数据集，而 OpenWebText 属于公共领域，但托管在其他地方以避免带宽成本。

### 正确的下载方法

使用**直接 HTTP 下载**或来自稳定镜像的**种子**。最可靠的来源是 Skylion007 的 GitHub 镜像（社区为托管清理后语料库所做的努力）。以下是获取 `urlsf_subset00.tar`（以及根据需要获取其他文件）的方法：

1. **从镜像直接下载**（推荐，速度较快）：
   - 基础 URL：`http://skylion007.github.io/OpenWebTextCorpus/`
   - 特定文件：`http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar`
   - 下载命令（使用 `wget` 或 `curl`；如需安装，请运行 `sudo apt install wget`）：

     ```
     cd ~/projects/nanoGPT  # 或您的目标目录
     wget http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar
     ```

     - 这将文件保存为 `./urlsf_subset00.tar`（约 3.3 GB）。这是一个 HTTP 镜像，无需认证，且速度快（直接来自 GitHub Pages）。
     - 对于完整集（所有子集）：从页面列出它们并循环下载，或使用脚本：

       ```bash
       for i in {00..13}; do
         wget http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset${i}.tar
       done
       ```

     - 使用 `curl` 的替代方案（如果 wget 不可用）：

       ```
       curl -O http://skylion007.github.io/OpenWebTextCorpus/urlsf_subset00.tar
       ```

2. **种子下载**（最适合大文件，可恢复且节省带宽）：
   - 所有子集的官方种子：来自原始 Gwern 仓库或 Academic Torrents 的磁力链接。
   - 磁力 URI（复制粘贴到客户端，如 qBittorrent、Transmission 或 `aria2c`）：

     ```
     magnet:?xt=urn:btih:5b1567f9eed6d1d1a5303a2e1f7a8d6b0a9c8d3e&dn=OpenWebTextCorpus
     ```

   - 或直接下载 .torrent 文件：从 [academictorrents.com](https://academictorrents.com/details/5b1567f9eed6d1d1a5303a2e1f7a8d6b0a9c8d3e) 下载或搜索 "OpenWebTextCorpus torrent"。
   - 如需安装种子客户端：
     - Ubuntu/Debian：`sudo apt install qbittorrent-nox`（无头模式）或使用 GUI。
     - 然后运行：`qbittorrent-nox` 并添加磁力链接。
   - 预期结果：将所有 14 个压缩包（总计约 40GB）下载到您选择的目录。如果只需部分，请仅选择 `urlsf_subset00.tar`。

3. **GitHub 克隆（如果您需要仓库结构）**：
   - 语料库元数据在 GitHub 上：`https://github.com/skylion007/OpenWebTextCorpus`
   - 克隆以获取 README/文档（非数据）：

     ```
     git clone https://github.com/skylion007/OpenWebTextCorpus.git
     ```

   - 数据链接在 README 中——指向上述相同的镜像。

### 下载后步骤

- **解压压缩包**：

  ```
  mkdir -p ./openwebtext/subsets
  tar -xvf urlsf_subset00.tar -C ./openwebtext/subsets
  ```

  - 这将解压约 100,000+ 个文本文件（例如 `0.txt`、`1.txt`）到 `./openwebtext/subsets/` 目录。每个文件都是清理后的网页文本。
- **用于 nanoGPT 集成**：
  - NanoGPT（Andrej Karpathy 的仓库）在 book/data 准备中有一个 `openwebtext` 示例。使用其脚本连接/处理文件：

    ```python
    # 来自 nanoGPT 的 data/openwebtext/prepare.py（根据需要调整）
    import os
    import glob

    input_dir = './openwebtext/subsets'
    output_file = './openwebtext/input.txt'

    with open(output_file, 'w') as out:
        for txt_file in sorted(glob.glob(os.path.join(input_dir, '*.txt'))):
            with open(txt_file, 'r') as f:
                out.write(f.read())
    ```

  - 这将创建一个巨大的 `input.txt` 文件用于训练。请注意——完整的 OpenWebText 需要大量存储空间/RAM。
- **验证完整性**：每个压缩包在镜像的 README 中都有 MD5 校验和（例如，对于 subset00：使用 `md5sum urlsf_subset00.tar` 对照提供的哈希值进行检查）。

### 如果问题仍然存在

- **镜像宕机？** 尝试原始 Gwern 源：`https://www.gwern.net/OpenWebTextCorpus`（链接到 AWS S3 或种子）。
- **法律/访问说明**：OpenWebText 属于公共领域（从开放网络爬取），但在使用时请遵守 robots.txt。此处无需 HF 认证。
- **HF 上的替代方案**：如果您需要 HF 托管的类似数据，请查看 `wikitext`、`bookcorpus` 或 `pile` 子集（例如，使用 `hf download` 和 `repo_id="EleutherAI/pile"`）。对于确切的 OpenWebText，请坚持使用镜像。
- **磁盘/速度提示**：这些文件非常大——请使用 SSD，并使用 `du -sh` 或 `htop` 进行监控。如果在中国或受限地区，请使用 VPN 以获得更快的访问速度。

如果下载成功但在解压/处理时遇到错误，或需要 nanoGPT 后续步骤的帮助，请粘贴详细信息！
