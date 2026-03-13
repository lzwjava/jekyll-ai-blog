---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot OAuth 令牌流程指南
translated: true
type: note
---

**问题：** 如何实现 GitHub Copilot 的 OAuth 设备流来获取 GitHub token，然后通过 `copilot_internal/v2/token` 交换为 Copilot API token，并使用该 token 调用 Copilot LLM API — 特别是在企业环境中，用户必须通过 GitHub 授权？

---

**答案：**

## 概述：双 Token 流程

系统使用两种不同的 token 类型：用于用户身份的 **GitHub OAuth token**，以及通过交换 GitHub token 获取的短期 **Copilot token** — 在整个会话中自动刷新。

这里是完整流程：

```
User runs app
  → GitHub Device Flow (user visits URL, enters code)
  → GitHub returns gho_xxx OAuth token
  → Exchange OAuth token with /copilot_internal/v2/token
  → Receive short-lived Copilot token
  → Call Copilot LLM API with Bearer <copilot_token>
```

---

## 步骤 1：GitHub OAuth 设备流

Copilot API 内部仅向来自 VSCode 的 OAuth token 暴露。VSCode 有自己的设备流认证，使用自己的 `client_id`。关键洞察是使用 VSCode 的 Client ID 来启动设备流并获取 `gho_xxx` OAuth app token。

VSCode 用于设备流的 Client ID 是：**`01ab8ac9400c4e429b23`**

### Python 实现

```python
import requests
import time

GITHUB_CLIENT_ID = "01ab8ac9400c4e429b23"  # VSCode's client ID

def get_device_code():
    """Step 1: Request a device code from GitHub"""
    resp = requests.post(
        "https://github.com/login/device/code",
        headers={"Accept": "application/json"},
        json={
            "client_id": GITHUB_CLIENT_ID,
            "scope": "read:user"
        }
    )
    resp.raise_for_status()
    data = resp.json()
    # data contains: device_code, user_code, verification_uri, expires_in, interval
    print(f"\n➡️  Visit: {data['verification_uri']}")
    print(f"➡️  Enter code: {data['user_code']}\n")
    return data

def poll_for_access_token(device_code, interval=5):
    """Step 2: Poll until user authorizes"""
    while True:
        time.sleep(interval)
        resp = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            json={
                "client_id": GITHUB_CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )
        data = resp.json()

        if "access_token" in data:
            print("✅ GitHub OAuth token obtained.")
            return data["access_token"]  # gho_xxx token
        elif data.get("error") == "authorization_pending":
            print("⏳ Waiting for user authorization...")
        elif data.get("error") == "slow_down":
            interval += 5  # respect GitHub's rate limit
        elif data.get("error") == "expired_token":
            raise Exception("Device code expired. Please restart.")
        else:
            raise Exception(f"OAuth error: {data}")
```

---

## 步骤 2：将 GitHub Token 交换为 Copilot Token

使用 GitHub OAuth token 调用 `https://api.github.com/copilot_internal/v2/token`，并带上适当的 editor headers 来接收 Copilot 特定的 API token。

```python
def get_copilot_token(github_token: str, account_type: str = "enterprise") -> dict:
    """
    Exchange GitHub OAuth token for a Copilot API token.
    account_type: 'individual' | 'business' | 'enterprise'
    """
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/json",
        "editor-version": "vscode/1.85.1",
        "editor-plugin-version": "copilot/1.155.0",
        "user-agent": "GithubCopilot/1.155.0",
        "Copilot-Integration-Id": "vscode-chat",
    }

    resp = requests.get(
        "https://api.github.com/copilot_internal/v2/token",
        headers=headers
    )
    resp.raise_for_status()
    token_data = resp.json()
    # token_data: { "token": "tid=...", "expires_at": <unix_ts>, "refresh_in": <seconds> }
    print(f"✅ Copilot token obtained, expires in {token_data['refresh_in']}s")
    return token_data
```

> **企业注意：** 对于企业账户，必须正确发送额外的 headers 如 `editor-version`、`editor-plugin-version`、`Copilot-Integration-Id` 和 `user-agent`，否则 API 会拒绝请求。

---

## 步骤 3：自动刷新 Copilot Token

系统实现了主动 token 刷新，在过期前 60 秒缓冲：`refreshInterval = (refresh_in - 60) * 1000`。失败的刷新会被记录并重新抛出，以防止静默失败。

```python
import threading

copilot_token_cache = {"token": None, "expires_at": 0}

def refresh_copilot_token_loop(github_token: str):
    """Background thread: auto-refresh Copilot token before expiry"""
    while True:
        token_data = get_copilot_token(github_token)
        copilot_token_cache["token"] = token_data["token"]
        copilot_token_cache["expires_at"] = token_data["expires_at"]

        refresh_in = token_data.get("refresh_in", 1500)
        sleep_seconds = max(refresh_in - 60, 30)  # refresh 60s before expiry
        print(f"🔄 Next Copilot token refresh in {sleep_seconds}s")
        time.sleep(sleep_seconds)

def start_token_refresh_daemon(github_token: str):
    thread = threading.Thread(
        target=refresh_copilot_token_loop,
        args=(github_token,),
        daemon=True
    )
    thread.start()
```

---

## 步骤 4：调用 Copilot LLM API

```python
def call_copilot_llm(prompt: str, model: str = "gpt-4o") -> str:
    copilot_token = copilot_token_cache["token"]
    if not copilot_token:
        raise Exception("Copilot token not available yet.")

    headers = {
        "Authorization": f"Bearer {copilot_token}",
        "Content-Type": "application/json",
        "editor-version": "vscode/1.85.1",
        "editor-plugin-version": "copilot/1.155.0",
        "Copilot-Integration-Id": "vscode-chat",
        "user-agent": "GithubCopilot/1.155.0",
        "OpenAI-Intent": "conversation-panel",
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 1000,
        "stream": False,
    }

    resp = requests.post(
        "https://api.githubcopilot.com/chat/completions",
        headers=headers,
        json=body
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
```

---

## 步骤 5：完整编排 — 主入口点

```python
import os

GITHUB_TOKEN_FILE = os.path.expanduser("~/.copilot_github_token")

def load_or_auth_github_token() -> str:
    """Load saved token or run device flow"""
    if os.path.exists(GITHUB_TOKEN_FILE):
        with open(GITHUB_TOKEN_FILE) as f:
            token = f.read().strip()
            if token:
                print("✅ Loaded saved GitHub token.")
                return token

    # Run device flow
    device_data = get_device_code()
    github_token = poll_for_access_token(
        device_data["device_code"],
        interval=device_data.get("interval", 5)
    )

    # Persist token securely (chmod 600)
    with open(GITHUB_TOKEN_FILE, "w") as f:
        f.write(github_token)
    os.chmod(GITHUB_TOKEN_FILE, 0o600)

    return github_token

def main():
    github_token = load_or_auth_github_token()

    # Get initial Copilot token
    token_data = get_copilot_token(github_token)
    copilot_token_cache["token"] = token_data["token"]
    copilot_token_cache["expires_at"] = token_data["expires_at"]

    # Start background refresh
    start_token_refresh_daemon(github_token)

    # Now call the LLM
    answer = call_copilot_llm("What is GitHub Copilot?")
    print("🤖 Copilot says:", answer)

if __name__ == "__main__":
    main()
```

---

## 企业注意事项

| 关注点 | 详情 |
|---|---|
| **账户类型** | 传递 `--account-type enterprise` 标志或在配置中设置。企业环境使用相同的 `/v2/token` 端点，但可能有政策限制。 |
| **Token 持久化** | Token 文件存储在 `~/.local/share/copilot-api/github_token`，权限为 `0o600` 以防止未经授权的访问。 |
| **重新授权** | 删除保存的 token 文件以强制进行新的设备流授权。 |
| **非交互式 / CI** | 对于非交互式环境，设置 `COPILOT_GITHUB_TOKEN`、`GH_TOKEN` 或 `GITHUB_TOKEN` 环境变量，系统会自动使用而无需提示。 |
| **企业 SSO** | 如果您的组织使用 SAML SSO，用户必须在 GitHub 网站上初始设备流登录后，也为组织授权 OAuth app。 |

---

## 关键端点总结

| 端点 | 用途 |
|---|---|
| `POST https://github.com/login/device/code` | 获取设备代码 + 用户代码 |
| `POST https://github.com/login/oauth/access_token` | 轮询获取 `gho_xxx` OAuth token |
| `GET https://api.github.com/copilot_internal/v2/token` | 交换为 Copilot token |
| `POST https://api.githubcopilot.com/chat/completions` | 调用 LLM (OpenAI 兼容) |

**参考资料：**

- [ericc-ch/copilot-api DeepWiki — 认证流程](https://deepwiki.com/ericc-ch/copilot-api/3.1-authentication-flow)
- [B00TK1D/copilot-api — api.py 参考实现](https://github.com/B00TK1D/copilot-api/blob/main/api.py)
- [Erick Christian 的博客 — 逆向工程 Copilot API](https://ericc-ch.github.io/blog/reverse-engineering-copilot-api/)
- [LiteLLM — GitHub Copilot 提供商文档](https://docs.litellm.ai/docs/providers/github_copilot)
- [GitHub 文档 — 认证 Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)