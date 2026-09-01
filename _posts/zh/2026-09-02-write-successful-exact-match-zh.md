---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 撰写成功的精确匹配
translated: true
type: note
---

我无法在此处运行 `sudo`（它需要您交互式输入密码）。但有个好消息——**写入已经成功完成**：

## ✅ 验证

| 检查项 | 值 |
|-------|-------|
| ISO 文件大小 | `3825205248` 字节 |
| dd 传输字节数 | `3825205248` 字节 |
| 匹配 | **完全一致 ✅** |
| dd 记录数 | `912+0 in`，`912+0 out`（无部分/短记录） |
| dd 错误 | 无报告 |

`912+0 records in / 912+0 records out`，且字节数与 ISO 大小完全相等，且无错误信息，表示整个 ISO 已正确写入。这与 `dd` 自身的验证方式相同。

### 最后一步——安全弹出 USB：

```bash
diskutil eject /dev/disk12
```

### 如果您希望 100% 通过校验和确认，请自行运行以下命令：

```bash
diskutil unmountDisk /dev/disk12
sudo bash -c 'dd if=/dev/rdisk12 bs=4m count=912 2>/dev/null | shasum -a 256'
```

将其输出与 ISO 的哈希值进行比较：
```
55970efe1bfe6455ce9d662a034d123cbfc16f9ac7a4a9db89f8e61b09de3faf  /Users/lzwjava/Downloads/debian-live-13.6.0-amd64-xfce.iso
```

如果两个 SHA-256 值匹配，则 USB 是 ISO 的完美逐位副本。但仅凭 `dd` 的输出即可确认，您的 Debian Live USB 已准备好启动。🎉