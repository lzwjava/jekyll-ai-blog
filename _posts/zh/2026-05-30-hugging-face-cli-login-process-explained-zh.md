---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face CLI 登录过程详解
translated: true
type: note
---

以下是 `hf auth login` 的工作流程，通过代码追踪如下：

## 入口点

运行 `hf auth login` 会调用 `src/huggingface_hub/cli/auth.py:61` 中的 CLI 命令：

```python
@auth_cli.command("login", ...)
def auth_login(token, add_to_git_credential, force):
    login(token=token, add_to_git_credential=add_to_git_credential, skip_if_logged_in=not force)
```

这会调用 `_login.py:59` 中的 `login()`。由于你没有传入 `--token`，`token=None`，因此它检测到你处于终端（而非笔记本）环境，并调用 `interpreter_login()`。

## 步骤 1：提示输入 token（`_login.py:236-272`）

`interpreter_login()` 执行你看到的操作：

1. 打印 ASCII 风格的 HF 标志
2. 调用 `getpass()` 以不可见方式读取 token（“Enter your token (input will not be visible)”）
3. 调用 `typer.confirm("Add token as git credential?")` —— 即 `[y/N]` 提示
4. 调用 `_login(token, add_to_git_credential)`

## 步骤 2：通过 HF API 验证 token（`_login.py:370-394`）

`_login()` 执行 3 件事：

```python
def _login(token, add_to_git_credential):
    # 1. 拒绝组织 token
    if token.startswith("api_org"):
        raise ValueError(...)

    # 2. 调用 HF API 进行验证——whoami(token) 访问 https://huggingface.co/api/whoami-v2
    token_info = whoami(token)
    permission = token_info["auth"]["accessToken"]["role"]  # "read" 或 "write"
    logger.info(f"Token 有效（权限：{permission}）。")

    # 3. 获取 token 的显示名称（例如 "test1"）
    token_name = token_info["auth"]["accessToken"]["displayName"]

    # 4. 将 token 保存到 stored_tokens 文件
    _save_token(token=token, token_name=token_name)

    # 5. 设置为活动 token（写入 token 文件 + 可选 git credential）
    _set_active_token(token_name=token_name, add_to_git_credential=add_to_git_credential)
```

## 步骤 3：token 存储——两个文件（`_auth.py`）

**stored_tokens**——一个多 token 的 INI 文件，位于 `~/.cache/huggingface/stored_tokens`：

```python
# _save_token() 位于 _auth.py:207
def _save_token(token, token_name):
    stored_tokens = get_stored_tokens()     # 解析已有的 INI
    stored_tokens[token_name] = token        # 添加/更新条目
    _save_stored_tokens(stored_tokens)       # 重写 INI 文件
```

文件内容类似：
```ini
[test1]
hf_token = hf_xxxx...

[my-other-token]
hf_token = hf_yyyy...
```

通过 `_write_secret()` 以 `0o600` 文件权限写入（仅拥有者读写）。

**active token**——单个文件，位于 `~/.cache/huggingface/token`：

```python
# _set_active_token() 位于 _login.py:420
def _set_active_token(token_name, add_to_git_credential):
    token = _get_token_by_name(token_name)  # 从 stored_tokens 中查找
    _write_secret(Path(HF_TOKEN_PATH), token)  # 将原始 token 写入 ~/.cache/huggingface/token
```

## 步骤 4：Git 凭据（`_login.py:433-439`）

如果你对“Add token as git credential?”回答了 `y`：

```python
if add_to_git_credential:
    if _is_git_credential_helper_configured():
        set_git_credential(token)
```

这会调用 `git credential approve` 将 token 存储在你系统的 git 凭据管理器中。在 Mac 上，这是 `osxkeychain`（通过 `git-credential-manager`）。这使得对 `huggingface.co` 仓库执行 `git push` 时能自动进行身份验证。

## Token 解析优先级（`_auth.py:53-67`）

当库后续需要 token 时（例如 `hf_hub_download`、`HfApi` 调用）：

```python
def get_token():
    return _get_token_from_google_colab()    # 1. Colab 密钥保管库
        or _get_token_from_environment()      # 2. HF_TOKEN 环境变量
        or _get_token_from_file()             # 3. ~/.cache/huggingface/token 文件
```

环境变量（`HF_TOKEN`）优先级高于文件，Colab 保管库优先级高于两者。

## 你看到的输出逐行解释

```
To log in, `huggingface_hub` requires a token...    # interpreter_login() 打印提示
Enter your token (input will not be visible):       # getpass()
Add token as git credential? [y/N]: y               # typer.confirm()
Token is valid (permission: write).                 # whoami(token) API 调用成功
The token `test1` has been saved to .../stored_tokens  # _save_token() —— INI 文件
Your token has been saved in your configured git credential helpers (...,osxkeychain).
                                                    # set_git_credential() 通过 git credential approve
Your token has been saved to .../token              # _write_secret() 写入活动 token 文件
Login successful.                                   # _login() 返回
The current active token is: `test1`                # 打印来自 API 的 displayName
```