---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在中国使用hf-mirror.com
translated: true
type: note
---

### 了解 hf-mirror.com
hf-mirror.com 是由社区维护的 Hugging Face Hub（huggingface.co）官方镜像站，专为帮助中国（包括广州）用户突破网络限制、更快下载 AI 模型/数据集而设计。它完整复制了原站仓库结构，因此您无需直接访问速度缓慢或常被屏蔽的原站，即可获取 GPT-2 等模型或 WikiText 等数据集。由于您经常使用 Clash 代理，请注意 hf-mirror.com 部署在国内，通常无需代理即可访问——它专门针对中国境内的直接使用进行了优化。如果您已通过 Clash 代理流量，可以选择直连 hf-mirror.com（避免不必要的跳转）或继续通过代理访问。

### 基础设置：使用镜像站
关键在于设置 `HF_ENDPOINT` 环境变量指向镜像站。这对 Hugging Face 工具（如 `transformers` 库、`huggingface-cli` 或 `hfd` 下载器）全局有效。请务必在导入库或开始下载**之前**完成此设置。

#### 1. 设置环境变量
- **Linux/macOS（永久生效）**：添加到 `~/.bashrc` 或 `~/.zshrc`：
  ```
  echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.bashrc
  source ~/.bashrc
  ```
- **Windows（PowerShell，永久生效）**：执行一次：
  ```
  [System.Environment]::SetEnvironmentVariable('HF_ENDPOINT', 'https://hf-mirror.com', 'User')
  ```
  然后重启终端。
- **临时生效（所有系统）**：在命令前添加：
  ```
  HF_ENDPOINT=https://hf-mirror.com your_command_here
  ```

这样即可在不修改代码的情况下将所有 Hugging Face 下载重定向到镜像站。

#### 2. 安装必要工具
- 安装 Hugging Face Hub CLI（用于下载）：
  ```
  pip install -U huggingface_hub
  ```
- 如需更高速下载，可安装 `hfd`（基于 aria2 的多线程下载器）：
  ```
  wget https://hf-mirror.com/hfd/hfd.sh  # 或通过浏览器下载
  chmod +x hfd.sh
  ```

#### 3. 下载模型或数据集
- **使用 huggingface-cli**（支持断点续传）：
  ```
  # 下载模型（如 GPT-2）
  huggingface-cli download gpt2 --resume-download --local-dir ./gpt2

  # 下载数据集（如 WikiText）
  huggingface-cli download --repo-type dataset wikitext --resume-download --local-dir ./wikitext
  ```
- **使用 hfd**（速度更快，特别适合大文件）：
  ```
  # 模型下载
  ./hfd.sh gpt2

  # 数据集下载
  ./hfd.sh wikitext --dataset
  ```
- **在 Python 代码中**（例如使用 transformers 库）：
  ```python
  import os
  os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # 在导入前设置

  from transformers import AutoModel, AutoTokenizer
  model = AutoModel.from_pretrained('gpt2')  # 自动从镜像站下载
  tokenizer = AutoTokenizer.from_pretrained('gpt2')
  ```
  运行命令：`HF_ENDPOINT=https://hf-mirror.com python your_script.py`

#### 4. 处理受限/需登录模型
部分模型（如 Llama-2）需要 Hugging Face 账户和访问令牌：
- 在 huggingface.co 登录（若网站被屏蔽请使用 Clash 代理）。
- 在 https://huggingface.co/settings/tokens 生成令牌。
- 使用以下命令下载：
  ```
  huggingface-cli download --token hf_YourTokenHere meta-llama/Llama-2-7b-hf --resume-download --local-dir ./Llama-2-7b-hf
  ```
  或使用 hfd：
  ```
  ./hfd.sh meta-llama/Llama-2-7b-hf --hf_username your_username --hf_token hf_YourTokenHere
  ```

### 与 Clash 代理集成
由于 hf-mirror.com 是国内镜像站，理论上无需 Clash 即可直连（直连速度更快）。但若仍需代理（例如为保持流量统一），可配置 Clash 将 hf-mirror.com 流量路由至指定代理组。Clash 无需特殊“HF”配置——其代理是系统全局的。

#### Clash 快速配置提示
- 确保 Clash 正在运行并设置为系统代理（在 Clash 中：进入“常规”>启用“系统代理”）。
- **推荐方案：直连 hf-mirror.com**：编辑 Clash 配置文件（通常位于 Clash 文件夹下的 `config.yaml`），添加规则直连镜像站：
  ```
  rules:
    # ... 现有规则 ...
    - DOMAIN-SUFFIX,hf-mirror.com,DIRECT  # 绕过代理直连
    # ... 其余规则 ...
  ```
  在 Clash 中重载配置（配置集 > 重载）。
- **如需代理**：若希望经 Clash 代理，无需特殊规则——流量将遵循默认规则（如 `MATCH,Proxy`）。可通过开启/关闭 Clash 访问 hf-mirror.com 测试效果。
- 下载时：在系统代理生效的终端中运行命令（Clash 会自动处理）。若使用 Python，`requests` 等库（被 transformers 使用）会遵循 Clash 设置的 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量（例如 HTTP 端口为 `http://127.0.0.1:7890`）。
- 测试：尝试下载小型模型（如 `distilbert-base-uncased`）。若速度慢，可尝试为 hf-mirror.com 流量关闭 Clash。

### 故障排除
- **下载仍指向 huggingface.co？** 确保在导入任何 HF 库**之前**设置 `HF_ENDPOINT`（重启 notebook/终端）。
- **速度缓慢？** 使用支持多线程的 `hfd` 配合 aria2。或检查网络——广州用户使用 hf-mirror.com 通常可达 10-50MB/s。
- **数据集报错？** 部分数据集含自定义脚本，需手动将基地址改为 `https://hf-mirror.com`。
- **Windows 特定问题**：若使用 Anaconda，请在 base 环境中设置环境变量。
- 如需自建本地镜像站（实现完全控制），可参考 Olah 或 hf-mirror-site 等开源工具，但建议先从公共镜像站入手。

此配置应能保障稳定下载。若遇具体错误，请提供输出信息以获取进一步帮助！

### 参考资源
- [HF-Mirror 官方指南](https://hf-mirror.com/)
- [Hugging Face Hub 端点文档](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables#huggingface_hub_constants.HF_ENDPOINT)
- [hfd 下载器](https://hf-mirror.com/hfd/hfd.sh)
- [Clash 配置规则](https://github.com/Dreamacro/clash/wiki/Configuration#rules)
- [Stack Overflow：中国境内下载指南](https://stackoverflow.com/questions/77388822/how-to-download-huggingface-bert-base-uncased-in-china)
