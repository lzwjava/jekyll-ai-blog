---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Git Push 输出数字详解
translated: true
type: note
---

**Question:** Explain these numbers in this git push output

**Answer:**

这是当你向 GitHub（或其他 Git remote）发送新 commits 时，`git push` 输出的典型内容。以下是每一行和每个数字的具体含义：

```text
Delta compression using up to 8 threads
```

Git 正在使用 **delta compression**（通过存储相对于其他对象的增量，而不是完整副本）来压缩你要发送的数据。
它决定使用多达 **8 个 CPU threads** 来并行执行此压缩操作。

```text
Compressing objects: 100% (4/4), done.
```

Git 压缩了 **4** 个对象（通常是 commits + trees + blobs）。
所有 4 个对象都已成功压缩 → **100% (4/4)**。

```text
Writing objects: 100% (4/4), 2.44 KiB | 2.44 MiB/s, done.
```

Git 将 **4** 个对象写入到待发送的 packfile 中。
这些对象的总大小（压缩后）= **2.44 KiB**
在本地创建 pack 期间的写入速度 = **2.44 MiB/s**

```text
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
```

- **Total 4**：共有 4 个对象被发送
- **delta 2**：其中 2 个对象是以 deltas（相对于其他对象的变更）形式存储的
- **reused 0**：没有从本地 repository 现有的 packfiles 中复用任何对象
- **pack-reused 0 (from 0)**：也没有从之前发送过的 packfiles 中复用任何内容

```text
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
```

在 **GitHub 端**：

- 你发送的 pack 中包含 **2** 个 delta 对象
- GitHub 成功应用/重构了这些 deltas (**100%**)
- 它使用了 GitHub 上已存在的 **2 local objects** 作为基准来应用这些 deltas

```text
Transferred: sent 6904, received 4540 bytes, in 18.9 seconds
```

本次 push 过程中的总网络流量：

- 你向 GitHub **sent**（发送）了 **6904 bytes**
- 你从 GitHub **received**（接收）了 **4540 bytes**（主要是状态消息、refs 更新确认、capability negotiation 等）
- 整个操作耗时 **18.9 seconds**

```text
Bytes per second: sent 364.8, received 239.9
```

有效传输速度（在本例中非常低）：

- 上传速度 ≈ **364.8 bytes/second** (~2.9 kbit/s)
- 下载速度 ≈ **239.9 bytes/second** (~1.9 kbit/s)

```text
To github.com:lzwjava/blog-source.git
```

最后一行显示了你 push 到的远程 repository。

### 快速总结 —— 到底发送了什么？

- 你 push 了 **4 个新对象**（可能包括 1–3 个 commits + tree(s) + 也许一两个小文件）
- 压缩后的大小 ≈ **2.44 KiB**
- 实际产生的网络流量约为 **6.9 KB**（包括协议开销 protocol overhead、sideband data 等）
- push 过程花费了 **将近 19 秒** → 连接速度非常慢（约 3 kbit/s 上传速度）

这种输出通常出现在以下情况：

- 你正在 push 非常小的变更
- 你的网络连接非常慢、高延迟或被限速
- 或者你在很长一段时间后第一次向 repository 进行 push（涉及大量的 negotiation）

**References:**

- [Git Internals - Transfer Protocols](https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols)
- [Git push output explained (stackoverflow)](https://stackoverflow.com/questions/2251588/git-push-output-explained)
