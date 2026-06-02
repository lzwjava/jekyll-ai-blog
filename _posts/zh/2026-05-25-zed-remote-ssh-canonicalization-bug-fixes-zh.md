---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed远程SSH规范化错误修复
translated: true
type: note
---

找到了根本原因。从 Zed 日志中：

```
ERROR [worktree] failed to canonicalize root path "/mnt/data/deepseek-v4-inference":
canonicalizing "/mnt/data/deepseek-v4-inference": No such file or directory (os error 2)
```

Zed 远程服务器可以看到该路径（它尝试监视该路径），但无法对其进行 **canonicalize**（规范化）。这是 Zed 在 SSH 远程连接中的一个已知问题。请按顺序尝试以下修复方法：

**修复 1：在远程端调整 inotify 限制**（修复次要问题）：

```bash
ssh lzw@192.168.1.36 "echo 'fs.inotify.max_user_watches=524288' | sudo tee -a /etc/sysctl.conf && sudo sysctl -p"
```

**修复 2：删除旧的远程服务器并让 Zed 重新下载**：

```bash
ssh lzw@192.168.1.36 "rm -rf ~/.zed_server/"
```

然后在 Zed 中重新打开项目——它将重新上传服务器二进制文件。

**修复 3：尝试通过 CLI 而不是 URL 打开**：

```bash
zed ssh://lzw@192.168.1.36//mnt/data/deepseek-v4-inference/
```

注意主机名后的双斜杠 `//`——某些 Zed 版本需要这样来正确解析绝对路径。

**修复 4：如果以上方法均无效，可使用 VS Code Remote SSH 作为临时解决方案**：

```bash
code --remote ssh-remote+lzw@192.168.1.36 /mnt/data/deepseek-v4-inference
```

要我立即在远程端执行修复 1 和修复 2 吗？
