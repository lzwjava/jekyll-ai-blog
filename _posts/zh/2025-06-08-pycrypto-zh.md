---
audio: false
generated: true
lang: zh
layout: post
title: 构建pycrypto时出错
translated: true
type: note
---

该错误是因为 `pycrypto` 包需要 Python 头文件 `longintrepr.h`，该文件属于 Python 开发头文件。您的 Python 3.13 环境中缺少此文件。解决方法如下：

### 解决方案

1. **安装 Python 开发头文件**
   为您的操作系统安装 Python 3.13 开发包。在 Ubuntu/Debian 上运行：

   ```bash
   sudo apt-get install python3.13-dev
   ```

2. **重新安装 `pycrypto`**
   安装头文件后，重试安装：

   ```bash
   pip install pycrypto
   ```

---

### 替代建议

**选项 1：将 `pycrypto` 替换为 `pycryptodome`（推荐）**
`pycrypto` 已弃用且无人维护。切换到维护中的分支 `pycryptodome`，它 API 兼容：

```bash
pip uninstall pycrypto
pip install pycryptodome
```

**选项 2：使用旧版 Python**
如果兼容性允许，使用 Python ≤3.9（已知 `pycrypto` 可在该版本运行）：

```bash
# 使用 pyenv 示例
pyenv install 3.9.18
pyenv local 3.9.18
pip install -r requirements.txt
```

---

### 问题原因

- `longintrepr.h` 是 Python 内部头文件，用于整数表示。它包含在 Python 开发包中，但标准安装不包含。
- Python 3.13 可能存在结构性变更，导致像 `pycrypto`（最后更新于 2014 年）这样的旧包无法兼容。
- 弃用警告表明 `pycrypto` 使用了过时的构建方法，新版 `pip` 不再支持。

### 预防措施

1. **避免使用 `pycrypto`**：密码学需求请使用 `pycryptodome`。
2. **固定 Python 版本**：对于遗留项目，在 Docker/Venv 等环境中使用 Python ≤3.9。
3. **检查依赖**：使用 `pip check` 识别不兼容的包。

---

您列出的包（`aliyunsdkcore`, `aliyun-python-sdk-ecs`, `alibabacloud_vpc20160428` 等）都不直接依赖 **`pycrypto`**。

但如果您看到 `pycrypto` 被安装，可能是某个包的**间接依赖**。要检查哪个包需要 `pycrypto`，请运行：

```bash
pip show pycrypto
```

或

```bash
pipdeptree | grep -i pycrypto
```

### 可能原因

1. **过时或弃用的安全相关包**（尽管您列表中没有包明确要求 `pycrypto`）。
2. **来自某个包的遗留依赖**，例如 `paramiko`（SSH）或 `google-auth`，但这些包通常已切换到 `pycryptodome`。

### 推荐操作

1. **将 `pycrypto` 替换为 `pycryptodome`**（现代且维护中的分支）：

   ```bash
   pip uninstall pycrypto
   pip install pycryptodome
   ```

   某些包接受 `pycryptodome` 作为直接替代。

2. **强制重新安装依赖**以确保没有隐藏链接：

   ```bash
   pip install --upgrade --force-reinstall -r requirements.txt
   ```

3. **如果 `pycrypto` 仍然存在**，请审核您的环境：

   ```bash
   pipdeptree --warn silence | grep -i crypto
   ```

### 关键要点

您列出的包不直接依赖 `pycrypto`，但可能有其他隐藏依赖。使用 `pipdeptree` 隔离问题将明确罪魁祸首。如果没有关键包需要它，**直接移除 `pycrypto`**——它已弃用且可能存在安全隐患。

---

根据您的日志，您**明确列出的包**都不直接依赖 `pycrypto`。但某个依赖项存在**间接依赖**。以下是识别和解决方法：

### 1. 识别问题包

运行此命令查找哪个顶层包需要 `pycrypto`：

```bash
pipdeptree --warn silence | grep -i pycrypto
```

### 2. 您技术栈中的常见嫌疑包

根据您的包列表，最可能的候选者是：

- **`paramiko`**（被 `hcloud`、`tigeropen` 或云 SDK 使用）
- **`google-auth`**（被 Google Cloud 包使用）
- **`boto`**（旧版 AWS 库）
- **`ansible`**（如果被间接使用）

### 3. 即时解决方案：替换 `pycrypto`

由于 `pycrypto` 已弃用且在 Python 3.13 上无法运行，将其替换为维护中的分支：

```bash
pip uninstall pycrypto
pip install pycryptodome
```

### 4. 如果依赖仍然存在

强制重新安装所有包并进行依赖检查：

```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### 5. 验证安装

检查 `pycryptodome` 是否满足依赖：

```bash
python -c "from Crypto import Random; print('Success')"
```

### 问题原因

- `pycrypto` 是旧包的常见加密依赖（最后更新：2014 年）
- Python 3.13 移除了 `pycrypto` 依赖的内部头文件如 `longintrepr.h`
- 现代替代方案如 `cryptography`（您正在安装）不使用 `pycrypto`

最快解决方案是**步骤 3**——将 `pycrypto` 替换为 API 兼容的 `pycryptodome`。这既解决了编译问题，又保持了兼容性。
