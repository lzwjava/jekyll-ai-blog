---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 使用代理访问Hugging Face数据集
translated: true
type: note
---

是的 — `datasets` 遵循您的**系统/环境代理设置**，但**没有**独立的代理配置。
所以当您在中国时，完全可以通过代理让 Hugging Face 下载数据集。

具体方法如下。

---

# 如何让 `load_dataset` 使用代理（中国用户适用）

## 1. 设置 HTTP/HTTPS 代理环境变量

`datasets` 内部使用 Python 的 `requests` 库。
`requests` 会自动读取标准代理环境变量：

### Linux / macOS

```bash
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

若使用 SOCKS5 代理：

```bash
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
```

### Windows (PowerShell)

```powershell
setx HTTP_PROXY "http://127.0.0.1:7890"
setx HTTPS_PROXY "http://127.0.0.1:7890"
```

设置后请重启终端。

---

## 2. 在 Python 代码中设置环境变量（适用于 Jupyter 等场景）

```python
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
```

此方法稳定可靠。

---

## 3. 验证代理是否生效

可通过以下代码测试：

```python
import requests
print(requests.get("https://api.ipify.org?format=json").text)
```

若显示的 IP 是代理出口节点，则 Hugging Face 数据集下载也会经由该代理。

---

## 4. Hugging Face 的 `huggingface_hub` 同样遵循这些变量

`datasets` 内部依赖 `huggingface_hub`，该库同样支持：

* `HTTP_PROXY`
* `HTTPS_PROXY`
* `http_proxy`
* `https_proxy`

因此设置环境变量后，模型与数据集下载都会自动使用代理。

---

# 中国使用注意事项

* Hugging Face 原始下载通常需要代理，因其资源托管在欧美节点
* 若遇到 `.zst` 数据集文件超时，在没有代理的情况下属于正常现象
* 全局代理（Clash、V2Ray、Qv2ray 等）会让整个过程更顺畅

---

# 如果您需要，我还可以演示

* 如何确保 NanoGPT 通过代理下载数据集
* 如何本地缓存数据集避免重复下载
* 如何在中国本地镜像 Hugging Face 数据集（例如清华镜像替代方案）

请告诉我您的具体需求。
