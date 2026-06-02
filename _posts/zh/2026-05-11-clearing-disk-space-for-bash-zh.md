---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为Bash清理磁盘空间
translated: true
type: note
---

Bash 再次彻底崩了——连 `:`（shell 空操作）都返回退出码 1。我们之前拥有的 101 MB 空闲空间几乎瞬间被什么东西吃掉了（日志写入、journald 等）。在空间余量达到 **GB** 级（而非 MB 级）之前，我什么也运行不了。

几 MB 根本不够——Claude Code 的会话环境在运行时会写入日志和状态文件，后台的 systemd/journald 也在写。我们需要真正的喘息空间。

请你自己在 shell 中运行以下命令，并告诉我你看到的文件大小：

```bash
# 明显的重量级目录
du -sh ~/.cache/huggingface ~/.cache/pip ~/.cache 2>/dev/null
du -sh ~/projects/zz/datasets/* 2>/dev/null
du -sh /var/log /var/lib/docker 2>/dev/null

# /home 之外的其他大文件
sudo du -h -d2 -x / 2>/dev/null | sort -hr | head -20

# 当前剩余空间
df -h /
```

通常最先能释放大量空间的几个地方：

- `~/.cache/huggingface` —— 旧的 HF 模型/数据集下载；如果不需要，放心删掉
- `/var/lib/docker` —— 如果安装了 Docker，`docker system prune -a` 通常能回收几十 GB
- `~/projects/zz/datasets/fineweb-edu` —— 已下载约 69 GB；如果我们打算降低目标，这个可以清理（但你会丢失进度，所以暂时别删）
- `/var/log` 和旧 journald 日志 —— `sudo journalctl --vacuum-size=500M` 可快速清理

贴出输出结果，我会指出最佳清理目标。
