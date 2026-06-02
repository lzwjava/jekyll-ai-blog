---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从磁盘已满中恢复
translated: true
type: note
---

## 我为何走到这一步

我当时正在为一个小规模的 GPT-3 消融实验下载 **FineWeb-Edu** 数据集——约 176 个 parquet 分片，目标总量约 400 GB，使用的是 `scripts/download/plan_and_download_fineweb_gpt3.py` 脚本。该脚本支持断点续传：分片状态保存在 `progress.json` 中，部分下载使用 HTTP Range 头，因此 Ctrl-C 后可以从 `.part` 文件精确恢复字节级进度。

下载到 **第 33 个分片**（`CC-MAIN-2014-10/train-00004`）时开始失败：

```
[34/176] data__CC-MAIN-2014-10__train-00005-of-00014.parquet
  attempt 1/3 failed: [Errno 28] No space left on device
  attempt 2/3 failed: [Errno 28] No space left on device
  attempt 3/3 failed: [Errno 28] No space left on device
RuntimeError: giving up on ...
```

磁盘**完全满了**。不是"空间不足"——Claude Code 自己都无法启动 bash 子进程，因为运行框架需要 `mkdir` 一个会话环境目录，而当时可用字节数确实是**零**。

## 诊断过程

清理出一小块空间后（删除了崩溃分片残留的 `.part` 文件——这么做是安全的，因为 `progress.json` 中仍将其标记为 `pending`，所以没有实际进度丢失），我终于能运行 `df -h` 和 `lsblk`：

```
/dev/nvme0n1p2  916G  868G  1.7G 100% /      ← Samsung 980 启动盘，濒临存满
sda             1.8T  空盘，无分区           ← WD Blue 机械硬盘，闲置未用
```

**解决方案就摆在眼前。** 那块 2 TB 的 WD Blue 机械硬盘已物理安装，内核可见为 `/dev/sda`，但没有分区表——从未被使用过。

NVMe 上的 868 GB 大致分配如下：

- `~/projects/` — 518 GB（数据集、模型权重、llama.cpp、imagenet、coco……）
- `~/.cache/huggingface` — 69 GB
- `/var/lib/docker` — 43 GB
- `~/projects/blog-source/fineweb_test_dump` — 88 GB 陈旧的实验输出
- 当前的 FineWeb-Edu 下载 — 72 GB

明显可迁移的数据远超 400 GB。

## 如何给 HDD 分区

GPT 标签，单个 ext4 分区覆盖整个磁盘——一行脚本即可完成，无需交互式 `fdisk` 提示：

```bash
sudo parted /dev/sda --script mklabel gpt mkpart primary ext4 0% 100%
sudo partprobe /dev/sda
```

为什么用 `parted` 而不是 `fdisk`：可脚本化，默认使用 GPT（对于大于 2 TB 的磁盘和现代 UEFI 系统很重要），无需 `n / p / 1 / Enter / Enter / w` 的繁琐操作。

`partprobe` 告知内核重新读取分区表，无需重启。通过 `lsblk /dev/sda` 验证——`sda1` 已出现。

## 如何格式化

```bash
sudo mkfs.ext4 -L data /dev/sda1
```

普通 ext4，标签设为 `data`，这样以后如果需要可以通过 `LABEL=data` 引用它。耗时约 30 秒，因为 mke2fs 会先对整个设备执行 `DISCARD` 操作（在机械硬盘上是空操作，但无害）。

## 如何挂载

```bash
sudo mkdir -p /mnt/data
sudo mount /dev/sda1 /mnt/data
sudo chown $USER:$USER /mnt/data
```

挂载点设在 `/mnt/data`——路径简短，位于系统级别（不深埋在 `/home` 下），`chown` 后每次写入无需 `sudo`。

## 如何永久生效

没有 fstab 条目，重启后挂载就会消失。使用 **UUID** 而非设备名称（`/dev/sda` 在添加新磁盘后可能会变化）：

```bash
UUID=$(sudo blkid -s UUID -o value /dev/sda1)
echo "UUID=$UUID  /mnt/data  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab
sudo mount -a   # 验证这一行；此处出错会阻止系统启动
```

`noatime` 跳过每次读取的时间戳写入——对于数据集读取场景有微小增益，因为训练过程中每个 parquet 文件会被反复访问。`mount -a` **必不可少**——它能在*现在*捕获拼写错误，方便修复，而不是等到启动时机器进入紧急模式。

最终状态：1.8 TB 文件系统，1.7 TB 可用空间，重启后持久存在。

## 如何移动进行中的下载

用户希望进行**干净的移动**，而非创建符号链接。下载脚本在 `progress.json` 中写入相对于 `--output-dir` 的路径，因此只要相对目录树保持不变且工作目录匹配，脚本就能透明地恢复：

```bash
cd ~   # 不要移动你当前所在的目录
mv ~/projects/zz /mnt/data/zz
cd /mnt/data/zz
```

72 GB，NVMe → SATA 机械硬盘，持续写入约 150 MB/s = 约 8 分钟。跨文件系统的 `mv` 实际上是 `cp` + `rm`，因此源 NVMe 空间只在最后阶段才会释放。

之后验证：33 个 parquet 分片完整无损，`progress.json` 一同迁移，`git status` 仍正常工作（`.git` 随目录树一起移动）。可从 `/mnt/data/zz` 重新运行下载器，它将从第 34 个分片继续。

## 我遇到的坑

**Claude 运行框架在会话启动时会固定工作目录。** 当我将 `~/projects/zz` `mv` 到 `/mnt/data/zz` 时，我当前的工作目录在我脚下消失了，后续每次 `Bash` 调用都返回 `Path "/home/lzw/projects/zz" does not exist`——即使是 `df -h` 这样的简单命令也不行。解决办法是从新目录重新启动 Claude Code（`cd /mnt/data/zz && claude`）。这不是 bug，只是会话启动方式的一个结果。如果你在会话中途移动项目目录，值得了解这一点。

## 下次我会怎么做

1. **在开始数百 GB 的下载*之前*检查 `lsblk`**，而不是之后。30 秒的检查就能从一开始将下载路由到 `/mnt/data`。
2. **为下载器添加磁盘空间预检查。** 很简单：在每个分片前，`shutil.disk_usage(output_dir).free` 与预期分片大小加余量进行比较；如果空间不足则给出明确提示，而不是让 `urllib` 中途抛出 `Errno 28`。
3. **全局设置 `HF_HOME`**，写在 `~/.bashrc` 或 `~/.profile` 中，指向 `/mnt/data/hf_cache`——这样这台机器上的所有 HuggingFace 工具默认都会写到这里。仅此一项就能防止 `~/.cache/huggingface` 膨胀到 69 GB。
4. **在安装时挂载大数据磁盘，而不是在恐慌时。** `/data` 挂载点这种事情应该放在初始机器设置清单中，与 `git config` 和 SSH 密钥并列。

## 模式总结

```
sudo parted /dev/sdX --script mklabel gpt mkpart primary ext4 0% 100%
sudo mkfs.ext4 -L <label> /dev/sdX1
sudo mkdir -p /mnt/<name> && sudo mount /dev/sdX1 /mnt/<name>
sudo chown $USER:$USER /mnt/<name>
echo "UUID=$(sudo blkid -s UUID -o value /dev/sdX1)  /mnt/<name>  ext4  defaults,noatime  0  2" \
  | sudo tee -a /etc/fstab
sudo mount -a
```

六个命令。五分钟搞定。困难的部分不是 Linux 操作——而是注意到那块一直闲置在那里的 2 TB 备用硬盘。
