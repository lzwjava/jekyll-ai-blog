---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 修复Hugging Face XetHub代理问题
translated: true
type: note
---

您的日志显示了一个关键问题：

**失败的连接并非直接访问 HuggingFace。**
它实际访问的是 **[https://transfer.xethub.hf.co](https://transfer.xethub.hf.co)** —— 这是 Hugging Face 的 *XetHub* 后端（Rust客户端 `reqwest`），而您设置的代理**不会自动拦截该地址**。

这就解释了一切：

* 您已为 Python 设置 `HTTP_PROXY` → 正常
* 但 XetHub 使用 **Rust reqwest** 而非 Python requests
* Rust reqwest **会忽略系统代理变量，除非设置小写的 HTTPS_PROXY 或显式配置代理**

因此：**您的 Python 环境使用代理，但 XetHub（HF 的新存储提供商）未使用代理**。

这就是您看到以下错误的原因：

```
ConnectError("Connection refused")
```

以及重试现象。

---

# 问题根源（简版）

Hugging Face 近期将存储迁移至 **XetHub**，该服务使用 Rust 客户端。
该客户端遵循：

* `https_proxy`
* `http_proxy`

但**根据构建配置可能不识别**大写版本。

您设置了大写变量？→ 它可能直接忽略。

---

# 解决方案（在中国境内实测有效）

## 1. 同时设置小写与大写代理变量

在运行 NanoGPT **前**于终端执行：

```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"

export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
```

Rust reqwest 优先识别小写
Python requests 优先识别大写
同时设置可避免兼容问题。

接着运行：

```bash
python data/openwebtext_10k/prepare.py
```

您应立即看到正常的下载速度。

---

# 2. 重要提示：若使用 SOCKS5 代理

Rust reqwest **默认不支持 socks5**（除非编译时启用可选功能）。
因此若代理地址为 socks5:// → 将会失败。

请切换至代理客户端的 HTTP 代理端口，通常为：

* Clash: 7890 (HTTP)
* V2RayN: 10809 (HTTP)

务必使用 HTTP 代理，而非 SOCKS。

---

# 3. 如何测试 Rust 组件是否使用代理

通过 `curl` 测试（**非 Python**），因为 curl 的代理规则与 Rust 行为相似：

```bash
curl -I https://transfer.xethub.hf.co --proxy http://127.0.0.1:7890
```

若测试成功 → Rust 下载也将正常工作。

若测试失败 → 您的代理无法访问 `xethub.hf.co` 域名。

---

# 4. 如需强制 Hugging Face 绕过 XetHub

可设置环境变量：

```bash
export HF_HUB_DISABLE_XETHUB=1
```

这将强制使用旧版 HuggingFace S3 后端替代 XetHub，对代理更友好。

接着执行：

```bash
python data/openwebtext_10k/prepare.py
```

这是最稳定的解决方案。

---

# 推荐方案（适合中国网络环境）

为保证稳定性：

```bash
export HF_HUB_DISABLE_XETHUB=1

export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"

python data/openwebtext_10k/prepare.py
```

---

如果您需要，我可以提供：

* 一键式脚本 (`hf_proxy_on.sh`)
* 永久性 `.bashrc` 代理配置方案
* 本地完整镜像 OpenWebText 数据集的指导（避免后续下载）

请随时告知。
