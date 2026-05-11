---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 扩展LLM训练的磁盘存储
translated: true
type: note
---

问题：我当前的Linux机器上，一块916 GB的NVMe硬盘只剩下1.7 GB可用空间（已用100%）。我正在训练大语言模型（LLM），需要存储FineWeb和GPT-3规模的大型数据集（约400 GB）。如何升级/扩展磁盘存储？

回答：

## 背景：您当前的情况

```
Filesystem      Size  Used Avail Use%
/dev/nvme0n1p2  916G  868G  1.7G 100%   ← 基本已满
```

您的新PC配置（根据您分享的零件清单）包含：
- **三星980 SSD 1TB**（PCIe 3.0 NVMe）—— 您当前的系统盘（正是这块已满）
- **西数蓝盘 2TB HDD** —— 也在配置中（7200 RPM SATA）

实际上，**您电脑里已经有解决方案了**：**2TB的WD机械硬盘**就是您的扩展盘。但您可能还没有挂载和配置好它。

---

## 策略方案（从最佳到最简单）

### 方案A：使用2TB机械硬盘（已在您的配置中）—— 推荐用于训练数据

这是最简单实用的方案。训练数据集（FineWeb等）是**顺序读取**的，因此机械硬盘的速度用于数据存储/预处理是可以接受的，即使不是最理想。

**第一步 — 识别新磁盘：**
```bash
lsblk
# 或
sudo fdisk -l
```
查找一个大约2TB、未分区的设备，如`/dev/sdb`或`/dev/sda`。

**第二步 — 分区：**
```bash
sudo fdisk /dev/sdb
# 在fdisk中：
# n  → 新建分区
# p  → 主分区
# 1  → 分区编号
# (按两次回车使用整个磁盘)
# w  → 写入并退出
```

**第三步 — 格式化为ext4：**
```bash
sudo mkfs.ext4 /dev/sdb1
```

**第四步 — 创建挂载点并挂载：**
```bash
sudo mkdir -p /data/llm
sudo mount /dev/sdb1 /data/llm
```

**第五步 — 设置为永久挂载（开机自动挂载）：**
```bash
# 获取UUID
sudo blkid /dev/sdb1

# 编辑fstab
sudo nano /etc/fstab
# 添加以下行（将UUID替换为实际值）：
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /data/llm  ext4  defaults  0  2
```

**第六步 — 设置权限以便您的用户可以写入：**
```bash
sudo chown -R $USER:$USER /data/llm
```

**验证：**
```bash
df -h /data/llm
# 应显示约1.8TB可用空间
```

现在将数据集下载到此处：
```bash
# 示例：HuggingFace数据集
huggingface-cli download HuggingFaceFW/fineweb --repo-type dataset --local-dir /data/llm/fineweb
```

---

### 方案B：添加第二块NVMe固态硬盘（更适合活跃训练I/O）

您选择的**微星MAG B760M迫击炮主板**有**两个M.2插槽**，因此可以物理添加另一块NVMe固态硬盘（例如2TB PCIe 4.0硬盘）。这能提供快得多的读取速度（约5000 MB/s，对比机械硬盘的150 MB/s），这在分词化和DataLoader I/O操作中非常关键。

物理安装后的步骤与方案A相同——它将显示为`/dev/nvme1n1`。

---

### 方案C：立即释放空间——清理现有NVMe硬盘

在购买或挂载任何东西之前，先立即回收空间：

```bash
# 查看哪些占用了空间
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh /home/* 2>/dev/null | sort -rh
du -sh ~/.cache/* 2>/dev/null | sort -rh

# 机器学习任务中的常见罪魁祸首：
# HuggingFace缓存
du -sh ~/.cache/huggingface/

# Conda/pip缓存
conda clean --all
pip cache purge

# Docker镜像（如果使用）
docker system prune -a

# 旧模型检查点
find ~ -name "*.ckpt" -o -name "*.pt" | du -sh
```

---

### 方案D：将缓存符号链接到新硬盘（透明集成）

挂载`/data/llm`后，无缝地将HuggingFace的缓存重定向到那里：

```bash
# 将现有HF缓存移动到新硬盘
mv ~/.cache/huggingface /data/llm/hf_cache

# 创建符号链接，工具不会察觉
ln -s /data/llm/hf_cache ~/.cache/huggingface

# 或者在~/.bashrc中设置环境变量：
echo 'export HF_HOME=/data/llm/hf_cache' >> ~/.bashrc
echo 'export TRANSFORMERS_CACHE=/data/llm/hf_cache' >> ~/.bashrc
source ~/.bashrc
```

---

## LLM训练数据存储容量现实核查

| 数据集 | 近似大小 |
|---|---|
| FineWeb (sample-10BT) | ~10–25 GB |
| FineWeb (完整版) | ~44 TB（本地不现实） |
| The Pile | ~825 GB |
| OpenWebText | ~40 GB |
| GPT-3训练数据等效 | 总计数TB |

**实用建议**：对于本地训练配置，使用**FineWeb样本子集**或**OpenWebText**，存放在2TB机械硬盘上。完整的FineWeb/GPT-3规模数据需要云/集群存储。

---

## 总结：现在该做什么

1. `lsblk` — 确认2TB的WD机械硬盘出现（例如`/dev/sdb`）
2. 分区 → 格式化 → 挂载到`/data/llm`
3. 添加到`/etc/fstab`，确保重启后持续有效
4. 在shell配置文件中设置`HF_HOME=/data/llm/hf_cache`
5. 将数据集直接下载到`/data/llm/`

这样您就能获得约1.8 TB的训练数据可用空间，而无需触碰操作系统分区。

参考资料：

- [在LVM上扩展ext4文件系统而不停机](https://www.systutorials.com/extending-a-mounted-ext4-file-system-on-lvm-in-linux/)
- [在无LVM的Debian上扩展存储](https://blog.bogdancaraman.com/expand-storage-debian-no-lvm/)
- [如何在Linux上添加第二块硬盘并增加存储池](https://www.cyberciti.biz/faq/howto-add-disk-to-lvm-volume-on-linux-to-increase-size-of-pool/)