---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全盘分析与迁移计划
translated: true
type: note
---

了解全局情况。**仅分析——未做任何更改。**

## 磁盘

| 设备                          | 容量      | 状态                                                             |
| ----------------------------- | --------- | ---------------------------------------------------------------- |
| `nvme0n1`（三星 980）         | 931 GB    | 引导/根分区，已满（使用 868 GB）                                 |
| `sda`（西数蓝盘 2 TB HDD）    | 1.82 TB   | **空，无分区表，未挂载** ← 你的逃生舱口                          |

HDD 已物理安装并可见。只需要分区+格式化+挂载。你粘贴的博客推荐指南在步骤上是正确的——指南中的 `/dev/sdb` 在这台机器上是 `/dev/sda`。

## 868 GB 的去向

按优先级排列的主要消耗者：

| 路径                                            | 大小       | 说明                                                          | 结论                                                |
| ----------------------------------------------- | ---------- | ------------------------------------------------------------- | --------------------------------------------------- |
| `~/projects/blog-source/fineweb_test_dump`      | **88 GB**  | 之前的 FineWeb 实验转储                                       | 很可能是**无用数据**——确认后删除                     |
| `~/.cache/huggingface`                          | **69 GB**  | Hugging Face 数据集/模型缓存                                  | **移至 HDD**，设置 `HF_HOME`                        |
| `~/projects/zz/datasets`                        | **72 GB**  | 当前运行的 fineweb-edu（进行中）                              | **移至 HDD**，不丢失进度                            |
| `~/projects/llama.cpp`                          | 73 GB      | 几乎肯定是内部的模型文件                                      | **移至 HDD**                                        |
| `~/projects/imagenet`                           | 64 GB      | 数据集                                                        | **移至 HDD**                                        |
| `/var/lib/docker`                               | **43 GB**  | Docker 镜像/卷                                                | 如果不需要，运行 `docker system prune -a`           |
| `~/projects/coco`                               | 38 GB      | 数据集                                                        | **移至 HDD**                                        |
| `~/projects/llama`                              | 31 GB      | 模型权重                                                      | **移至 HDD**                                        |
| `~/projects/nanoGPT`、`llama2.c`                | 各 26 GB   | 内部的数据集/权重                                             | **移至 HDD**                                        |
| `~/qDownloads`                                  | 14 GB      | qBittorrent 电影（老友记、沙丘、奥本海默、这个杀手不太冷、林肯公园） | 已看过的删除                                        |
| `~/.cache/pip`                                  | 13 GB      | pip wheel 缓存                                                | 安全执行 `pip cache purge`                          |
| `~/projects/blog-source/.venv`                  | 7.6 GB     | 某个项目的虚拟环境                                            | 可重建                                              |
| `~/.ollama`                                     | 8.4 GB     | Ollama 模型                                                   | 移动或删除                                          |

总计超过 400 GB 的明确可迁移数据，它们全都错误地放在了错误的磁盘上。

## 操作方案（你来执行，我不动任何东西）

### 步骤 1 — 设置 HDD（一次性操作，约 5 分钟）

```bash
# 1. 将整个磁盘分区为 GPT，单个 ext4 分区
sudo parted /dev/sda --script mklabel gpt mkpart primary ext4 0% 100%

# 2. 格式化
sudo mkfs.ext4 -L data /dev/sda1

# 3. 在你的 home 下创建挂载点以保持路径简短
sudo mkdir -p /mnt/data
sudo mount /dev/sda1 /mnt/data
sudo chown $USER:$USER /mnt/data

# 4. 使其持久化
echo "UUID=$(sudo blkid -s UUID -o value /dev/sda1)  /mnt/data  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab

# 5. 验证
df -h /mnt/data    # 应显示约 1.8 TB 可用
```

> 为什么用 `parted` 而非 `fdisk`：可单行脚本化，默认 GPT（对 >2 TB 和现代系统重要），无交互提示。
> 为什么用 `noatime`：跳过每次读取的时间戳写入——对数据集读取略有性能提升。

### 步骤 2 — 原地移动 FineWeb 下载（进度不丢失）

```bash
# 如果下载器正在运行，先停止
mkdir -p /mnt/data/datasets
mv ~/projects/zz/datasets/fineweb-edu /mnt/data/datasets/
ln -s /mnt/data/datasets/fineweb-edu ~/projects/zz/datasets/fineweb-edu
```

脚本会从 `progress.json` 恢复，且符号链接对它透明。**不要更改 `TARGET_TOKENS`**——你现在有 1.8 TB 了。

### 步骤 3 — 重定向 HuggingFace 缓存（在 `.bashrc` 中添加一行）

```bash
mkdir -p /mnt/data/hf_cache
mv ~/.cache/huggingface/* /mnt/data/hf_cache/ 2>/dev/null
rmdir ~/.cache/huggingface
ln -s /mnt/data/hf_cache ~/.cache/huggingface
# 并使其在清空 ~/.cache 后仍有效
echo 'export HF_HOME=/mnt/data/hf_cache' >> ~/.bashrc
```

我同时推荐符号链接 **和** 环境变量——符号链接覆盖了硬编码 `~/.cache/huggingface` 的工具，环境变量覆盖了读取 `HF_HOME` 的工具。

### 步骤 4 — 移动其他大型项目目录

```bash
mkdir -p /mnt/data/projects
for d in llama.cpp llama imagenet coco nanoGPT llama2.c stable-diffusion-webui; do
  mv ~/projects/$d /mnt/data/projects/
  ln -s /mnt/data/projects/$d ~/projects/$d
done
```

### 步骤 5 — 调查并清理（删除前先确认）

```bash
# 可能已过时，删除前检查：
ls -la ~/projects/blog-source/fineweb_test_dump   # 88 GB — 是否还需要？

# 安全的一行命令：
pip cache purge                                   # 释放约 13 GB
docker system prune -a --volumes                  # 最多释放 43 GB（前提是不需要这些镜像）
sudo journalctl --vacuum-size=500M                # 清理旧的 systemd 日志
```

对于 `~/qDownloads`：这些显然是电影——`沙丘 2`、`奥本海默`、`这个杀手不太冷`、`老友记 S1`、`林肯公园 - 流星圣殿`。总共约 14 GB。删除你已看过的。（如果 qBittorrent 还在做种，先在 qBit 界面中移除，以免它尝试重新创建文件。）

## 对推荐指南的两点澄清

在你粘贴的回答中，有几处对于**这台**机器并不完全正确：

- 它说 `/dev/sdb`——你的机器上 HDD 是 `/dev/sda`（唯一的 SATA 磁盘；NVMe 启动盘在 M.2 总线上，是独立的）。
- 它说 "FineWeb 完整版约 44 TB，本地不实用"——是的，但你的 **400 GB** 目标是 `fineweb-edu` 子集，它完全能放入新的 1.8 TB 硬盘。不要因为存储问题缩小训练规模；HDD 已经解决了。

## 我建议的优先操作顺序

操作顺序：
1. 分区并挂载 HDD（步骤 1）——立即获得 1.8 TB 余量。
2. 通过符号链接移动 `~/projects/zz/datasets/fineweb-edu`（步骤 2）——解除正在进行的下载的阻塞。
3. 移动 Hugging Face 缓存（步骤 3）——释放 NVMe 上 69 GB 空间。
4. 检查 `blog-source/fineweb_test_dump`（步骤 5）——88 GB 很可能可以删除。
5. 其余 `~/projects/*`（步骤 4）可随意移动——这些是数据集/权重，放在 HDD 上用于读密集型工作负载没有问题。

完成步骤 1–4 后，你的 NVMe 将使用约 50%，HDD 上将有约 1.6 TB 空闲空间用于未来的数据集。无需任何物理硬件改动——所有东西已经就位。

需要我写一个脚本来自动完成步骤 1–3，还是你更愿意逐行手动执行？
