---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rsync与SCP速度对比
translated: true
type: note
---

问题：rsync 的传输速度是否比 scp 慢？

答案：

通常不会——尤其对于你正在做的事情而言。在快速网络上进行一次性批量复制时，两者速度大致相当，因为两者都受 SSH 加密算法的 CPU 限制，而非协议本身。rsync 会在开始时增加少量滚动校验和/文件列表开销，因此在局域网中传输单个超大文件时，scp 可能略胜一筹。但这只是极特殊情况。

对于你的场景（`.git` 包、仓库、任何可断点续传或重复传输的内容），rsync 完胜：

- **可断点续传。** `rsync --partial --append-verify` 能在连接断开后恢复传输。scp 则从头开始。当传输 5GB 文件，速度在 400KB/s 到 12MB/s 波动时，仅此一点就至关重要。
- **增量传输。** 再次运行 rsync 时只发送变化的块。再次运行 scp 则会重新传输全部内容。
- **跳过未变化的文件。** 对目录复制（而非单个包）尤为重要。

为什么你的传输感觉慢——不是 rsync 的问题，而是另外两个原因：

1. **SSH 加密算法的 CPU 瓶颈。** 在较旧的机器上，默认加密算法会限制速度。可强制使用快速算法：

   ```bash
   rsync -a --info=progress2 \
     -e 'ssh -c aes128-gcm@openssh.com -o Compression=no' \
     src/ user@host:dst/
   ```

   `aes128-gcm` 利用了 AES-NI 硬件加速；`Compression=no` 很重要，因为 git 包已经压缩过，gzip 压缩只会白白消耗 CPU。

2. **Git 包不压缩。** 确保你**没有**使用 `-z` 选项。你遇到的 `400KB/s` 低速度很可能是远程机器在处理不可压缩数据时因压缩而导致的 CPU 瓶颈。

对于 `.git` 目录而言，最快的方法通常是完全跳过文件遍历：

```bash
# 让 git 自行打包/传输——通常比 rsync 和 scp 都快
git clone --bare user@host:/path/to/repo.git
# 对于已有的检出，可以创建 bundle：
git bundle create linux.bundle --all   # 然后 rsync 这个单一的 .bundle 文件
```

bundle 是单个连续文件，因此能以线路速率传输，没有每个对象的开销，并且作为整体可以轻松实现断点续传。

总结：rsync 不是瓶颈。关闭压缩，固定使用 GCM 加密算法，对于 git 场景，优先使用 `git bundle` + 传输，而不是直接遍历包文件。
