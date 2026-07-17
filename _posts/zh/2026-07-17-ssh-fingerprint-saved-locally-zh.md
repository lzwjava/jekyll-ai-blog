---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH 指纹已本地保存
translated: true
type: note
---

问题：如果在RunPod代理SSH连接时输入"yes"，是否会保存指纹到本地？

答案：是的。每当SSH提示`Are you sure you want to continue connecting (yes/no/[fingerprint])?`并输入`yes`时，都会在本地`~/.ssh/known_hosts`文件中添加一条记录——无论是通过代理（`ssh.runpod.io`）还是直接TCP连接。

记录格式如下：
```
ssh.runpod.io ssh-ed25519 AAAA...<密钥数据>
```

针对代理连接的情况：
- 密钥会以主机名`ssh.runpod.io`为键存储（默认端口22，因此无需添加端口后缀）。
- 由于RunPod代理始终为`ssh.runpod.io`提供相同的**主机密钥**（这是网关机器的密钥，而非您的Pod密钥），这一条`known_hosts`记录将**永久覆盖**您所有的Pod——这正解释了为什么下次连接到不同Pod时不会再次收到提示。

针对直接TCP连接的情况：
- 记录存储格式为`[213.173.99.50]:26246 ssh-ed25519 AAAA...`（因使用非默认端口而采用括号+端口表示法）。
- 该记录仅对应特定的IP:端口。新建Pod → 新IP/端口 → 需要新记录 → 触发新提示。

您可以通过以下命令验证已保存的内容：
```bash
grep runpod ~/.ssh/known_hosts
ssh-keygen -F ssh.runpod.io   # 检查特定主机是否已被信任
```

如果RunPod在基础设施变更等情况下轮换了代理的主机密钥（虽罕见但可能发生），您会收到`REMOTE HOST IDENTIFICATION HAS CHANGED`警告，此时需要删除过期记录：
```bash
ssh-keygen -R ssh.runpod.io
```

参考文档：
- [OpenSSH known_hosts手册](https://man.openbsd.org/ssh#known_hosts)
- [RunPod SSH文档](https://docs.runpod.io/pods/configuration/use-ssh)