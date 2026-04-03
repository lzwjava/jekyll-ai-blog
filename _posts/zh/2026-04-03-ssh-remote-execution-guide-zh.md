---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH远程执行指南
translated: true
type: note
---

### 发生了什么

1. **你提供了SSH凭证** —— 主机 `213.173.110.xxx`，端口 22775，用户 root
2. **首次尝试失败** —— 远程主机上没有SSH密钥，因此认证被拒绝
3. **你手动添加了密钥** —— 通过 `echo` 将密钥写入远程主机的 `authorized_keys`
4. **第二次尝试成功** —— 成功连接并获取了硬件报告
5. **安装了 emacs-nox** —— 通过SSH执行 `apt-get update && apt-get install -y`，因其耗时较长而在后台运行

### 我的工作方式

- 我通过**本服务器**的shell执行命令
- 对于远程机器，我从这里发起SSH连接 —— 与任何终端操作无异
- 长时间任务在后台运行，完成后我会轮询获取结果
- 没有魔法 —— 仅仅是 `ssh + command` 管道传递

### 操作模式

```
ssh -p <端口号> root@213.173.110.xxx "命令"
```

这就是全部秘诀。想在那个机器上做更多操作，尽管开口。🦞