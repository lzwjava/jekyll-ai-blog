---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停用Python虚拟环境指南
translated: true
type: note
---

问题：如何退出 Python 虚拟环境并返回到默认的系统 Python？

答案：

要退出/停用虚拟环境，只需运行：

```bash
deactivate
```

运行 `deactivate` 后，你的提示符会从 `(venv) lzw@to:...` 变回 `lzw@to:...`，并且你将再次使用系统 Python。

---

**验证你是否已返回系统 Python：**

```bash
which python3
python3 --version
```

---

**在你的情况中**，由于 venv 是用未安装的 Python 3.13 构建的，停用后你可以显式地使用可用的系统 Python 运行命令：

```bash
PYTORCH_ALLOC_CONF=expandable_segments:True \
python3.11 -u train.py config/train_fineweb_gpt3.py 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

或者如果系统上的 `python3` 指向 3.11 或 3.12，直接使用 `python3` 即可。

---

**可选 — 使用正确的 Python 版本重新创建 venv：**

如果你想正确修复 venv 而不是直接使用系统 Python：

```bash
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # 重新安装依赖
```