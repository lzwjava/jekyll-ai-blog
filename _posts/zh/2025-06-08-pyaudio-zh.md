---
audio: false
generated: true
lang: zh
layout: post
title: PortAudio与pyaudio
translated: true
type: note
---

该错误出现是因为 **pyaudio** 需要 PortAudio 开发头文件才能编译，而您的系统中缺少这些文件。以下是解决方法：

### 分步解决方案

1. **安装 PortAudio 开发头文件**（pyaudio 必需）：

```bash
sudo apt update && sudo apt install portaudio19-dev
```

2. **安装 Python 开发工具**（如果尚未安装）：

```bash
sudo apt install python3-dev
```

3. **重新尝试安装**：

```bash
pip install -r requirements.local.txt
```

### 如果仍遇到 pycrypto 相关问题

pycrypto 软件包已过时，可能存在兼容性问题。请通过修改 `requirements.local.txt` 将其替换为 **pycryptodome**：

1. 打开需求文件：

```bash
nano requirements.local.txt
```

2. 将 `pycrypto` 替换为：

```
pycryptodome
```

3. 保存并重新运行安装：

```bash
pip install -r requirements.local.txt
```

### 解决原理

- `portaudio19-dev` 提供编译 pyaudio 所需的缺失 PortAudio 头文件
- `python3-dev` 包含必要的 Python 开发头文件
- `pycryptodome` 是已废弃 pycrypto 的维护版替代品

### pycrypto 备用方案（如需保留）

若必须使用 pycrypto，请先安装编译依赖：

```bash
sudo apt install build-essential libgmp-dev
pip install pycrypto
```

但请注意 pycrypto 与新版本 Python 存在兼容性问题。

完成以上步骤后，所有软件包应能正确安装。关于旧版构建的 DEPRECATION 警告属于提示信息，不会阻止安装——这表明这些软件包未来需要迁移至 PEP 517 构建标准。
