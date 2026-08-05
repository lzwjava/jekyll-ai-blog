---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 笔记本共享：认证方式取决于类型
translated: true
type: note
---

问题：如果你分享一个Jupyter notebook，其他人是否需要密码或SSH才能访问？

答案：取决于你分享的*是什么*——“分享notebook”实际上涵盖了两件截然不同的事情。

**1. 分享`.ipynb`文件（静态）** —— 是的，完全不需要认证
```bash
# 仅仅是文件——包含单元格和输出结果的JSON
cat notebook.ipynb | head -20
```
任何人都可以在GitHub预览、`nbviewer`、VS Code或`jupyter nbconvert --to html notebook.ipynb`中打开它。它只是一个快照，没有内核，没有执行，也不需要密码。这就是大多数人所说的“分享一个notebook”的意思。

**2. 分享*实时*服务器（交互式）** —— 认证仍然适用，除非你明确移除

默认情况下Jupyter绑定到localhost并需要token：
```bash
jupyter notebook --no-browser
# http://localhost:8888/?token=abc123...
```

要让别人*不通过SSH隧道*就能访问，你需要暴露端口：
```bash
jupyter notebook --ip=0.0.0.0 --port=8888
```
但它仍然需要token/密码，除非你把认证也去掉：
```bash
jupyter notebook --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=''
```
最后一组命令就是人们通常所说“不需要密码”的情况——但如果你在不够信任的网络上这样做，这是一个极其糟糕的主意，因为任何能访问该端口的人都能在你的机器上执行任意代码（这实际上就是连到你的电脑上运行代码）。

**3. Colab / Kaggle / 托管式 notebook** —— “分享”按钮会生成一个链接，认证由平台登录（例如Google账户）处理，不需要SSH。你不需要暴露自己的机器。

因此：静态文件——不需要认证，正确。实时内核——仍然需要*某种*屏障（token、密码或平台登录），除非你故意关闭了它，那就是用“网络上的任何人都能控制你的机器”来换取便利。

如果你是为了远程GPU计算，比起`--ip=0.0.0.0` + 去掉token更安全的做法仍然是用SSH端口转发：
```bash
ssh -L 8888:localhost:8888 user@remote-gpu-host
```
这样服务器在远程端仍然绑定在localhost，token保持完整，你通过隧道访问而不是公要开暴露端口。

参考资料：
- [Jupyter Notebook 安全文档](https://jupyter-notebook.readthedocs.io/en/stable/security.html)