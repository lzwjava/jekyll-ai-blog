---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 安装 Python 3.11 和 pip3.11
translated: true
type: note
---

看起来你在 Ubuntu 系统上安装了多个 Python 和 pip 版本，现在想要安装 **Python 3.11** 及其对应的 **pip (pip3.11)**。以下是具体步骤：

---

### **1. 安装 Python 3.11**

首先更新软件包列表并安装 Python 3.11：

```bash
sudo apt update
sudo apt install python3.11
```

验证安装：

```bash
python3.11 --version
```

---

### **2. 为 Python 3.11 安装 pip**

Ubuntu 默认软件源可能不包含 Python 3.11 的 `pip`。你可以通过以下步骤安装：

#### **方案 A：通过 apt 安装（如果可用）**

```bash
sudo apt install python3.11-venv python3.11-dev python3-pip
```

如果 `python3-pip` 安装的是其他版本的 pip，请改用**方案 B**。

#### **方案 B：使用 ensurepip 安装**

```bash
python3.11 -m ensurepip --upgrade
```

这将专门为 Python 3.11 安装 pip。

#### **方案 C：使用 get-pip.py 安装**

如果以上方法无效，可使用官方 `get-pip.py` 脚本：

```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

---

### **3. 验证 pip3.11 安装**

检查 `pip3.11` 是否可用：

```bash
pip3.11 --version
```

你应该看到类似输出：

```
pip 23.x.x from /usr/local/lib/python3.11/site-packages/pip (python 3.11)
```

---

### **4. （可选）创建虚拟环境**

为避免 Python 版本冲突，可以创建虚拟环境：

```bash
python3.11 -m venv myenv
source myenv/bin/activate
```

此时虚拟环境内的 `pip` 将使用 Python 3.11。

---

### **命令汇总表**

| 命令 | 用途 |
| --------- | --------- |
| `sudo apt update` | 更新软件包列表 |
| `sudo apt install python3.11` | 安装 Python 3.11 |
| `python3.11 -m ensurepip --upgrade` | 为 Python 3.11 安装 pip |
| `pip3.11 --version` | 验证 pip 安装 |
| `python3.11 -m venv myenv` | 创建虚拟环境 |

---
