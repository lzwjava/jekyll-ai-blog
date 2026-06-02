---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face 登录认证说明
translated: true
type: note
---

**问题：** 当您运行 `huggingface-cli login` 或 `huggingface_hub.login()` 时，Hugging Face Hub 的身份验证流程是如何工作的？

**答案：**

该流程包含三个部分：令牌生成、本地存储和凭据集成。

## 令牌生成

您访问 <https://huggingface.co/settings/tokens> 生成一个个人访问令牌。HF 会提供一个字符串（在您的例子中为 `test1`），它充当类似 OAuth 的凭据——这是一个 Bearer 令牌，用于验证对 `huggingface.co` 的 API 请求。

## 存储策略

当您运行 `huggingface-cli login`（或调用 `from huggingface_hub import login; login(token="test1")`）时，该库会：

1. **保存到缓存** → `~/.cache/huggingface/stored_tokens`（明文存储，但在 Unix 系统上仅用户可读）
2. **注册到 git 凭据助手** → 使用系统的凭据管理器（macOS 上为 `osxkeychain`，Linux 上为 `pass` 或 `manager-core`）

```python
# huggingface_hub 内部执行的操作（简化后）：
import os
from pathlib import Path

token_cache = Path.home() / ".cache" / "huggingface" / "stored_tokens"
token_cache.parent.mkdir(parents=True, exist_ok=True)
token_cache.write_text(token)  # 存储明文

# 然后注册到 git 凭据助手
os.system(f"git credential approve <<< 'protocol=https\\nhost=huggingface.co\\nusername=git\\npassword={token}'")
```

git 凭据助手是关键所在——它意味着您的令牌可以与任何使用 git 凭据系统的工具集成（包括 `huggingface_hub` 自身在克隆私有仓库时的 git 操作）。

## 请求流程

当您之后与 HF 交互时（例如 `from_pretrained()`、API 调用），该库：

1. **从缓存加载令牌**，或向 git 凭据助手请求
2. **将其作为 Bearer 令牌注入 HTTP 头部**：

   ```
   Authorization: Bearer test1
   ```

3. **HF API 在服务端验证令牌**，并返回模型元数据、权重，或拒绝访问

## 为什么需要两种存储方式？

- **`~/.cache/huggingface/`** → 速度快，无需调用凭据助手子进程
- **Git 凭据助手** → 存储安全（macOS/Windows 上加密），与基于 git 的工作流程集成（通过 HTTPS 使用 `git clone` 克隆私有仓库）

该库在加载时会同时检查两者——优先使用凭据助手（如果可用），否则回退到缓存文件。

## 安全注意事项

- 令牌以明文形式存储在 `~/.cache/huggingface/`，但仅限您的用户访问（权限 mode 600）
- 凭据助手更安全（macOS 上静态加密）
- 令牌提供对您账户的写入权限（基于您生成时设置的权限）

这比 OAuth 2.0 流程更简单——HF 仅使用无状态 Bearer 令牌认证，这就是为什么一个静态令牌可以在任何地方使用。
