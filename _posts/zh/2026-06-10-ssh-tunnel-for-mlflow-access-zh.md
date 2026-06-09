---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH隧道用于MLflow访问
translated: true
type: note
---

完成。SSH隧道已启用：

```
http://localhost:5001
```

现在显示的是来自amd-cloud（MI300X训练数据）的**远程**MLflow运行结果，而非本地副本。隧道命令为：

```
ssh -L 5001:127.0.0.1:5001 amd-cloud -N -f
```

- `-L 5001:127.0.0.1:5001` — 将本地的5001端口转发到远程的5001端口
- `-N` — 不执行远程命令，仅建立隧道
- `-f` — 认证后在后台运行

稍后关闭隧道：`pkill -f "ssh -L 5001"`