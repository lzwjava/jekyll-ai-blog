---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot OAuth 令牌交换指南
translated: true
type: note
---

**Session ID:** ses_31a545494ffe4t0ZoluyhjdboW
**Created:** 3/13/2026, 1:29:18 PM
**Updated:** 3/13/2026, 1:33:28 PM

---

## User

hi

---

## Assistant (Build · google/gemini-3-flash-preview · 1.7s)

你好！今天我能如何帮助你？

_Thinking:_

[REDACTED]

---

## User

change to such flow , **Question:** How do I implement GitHub Copilot's OAuth device flow to get a GitHub token, then exchange it for a Copilot API token via `copilot_internal/v2/token`, and use that token to call the Copilot LLM API — particularly in an enterprise environment where the user must authorize via GitHub?

---

**Answer:**

## 概述：双令牌流程

系统使用两种不同的令牌类型：用于用户身份的 **GitHub OAuth token**，以及通过交换 GitHub token 获得的短期 **Copilot token** — 在整个会话中自动刷新。

完整流程如下：

```
User runs app
  → GitHub Device Flow (user visits URL, enters code)
  → GitHub returns gho_xxx OAuth token
  → Exchange OAuth token with /copilot_internal/v2/token
  → Receive short-lived Copilot token
  → Call Copilot LLM API with Bearer <copilot_token>
```

---

## 步骤 1：GitHub OAuth Device Flow

Copilot API 内部仅向来自 VSCode 的 OAuth token 暴露。VSCode 使用自己的 device flow 认证和自己的 `client_id`。关键洞察是使用 VSCode 的 Client ID 来启动 device flow 并获取 `gho_xxx` OAuth app token。

用于 device flow 的 VSCode Client ID 是：**`01ab8ac9400c4e429b23`**

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

使用 GitHub OAuth token 调用 `https://api.github.com/copilot_internal/v2/token`，并带上正确的 editor headers，以接收 Copilot 特定的 API token。

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

> **企业注意事项：** 对于企业账户，必须正确发送额外的 headers 如 `editor-version`、`editor-plugin-version`、`Copilot-Integration-Id` 和 `user-agent`，否则 API 会拒绝请求。

---

## 步骤 3：自动刷新 Copilot Token

系统实现了在到期前 60 秒缓冲的主动 token 刷新：`refreshInterval = (refresh_in - 60) * 1000`。刷新失败将被记录并重新抛出，以防止静默失败。

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

| Concern | Detail |
|---|---|
| **Account type** | 传递 `--account-type enterprise` 标志或在配置中设置。企业使用相同的 `/v2/token` 端点，但可能有策略限制。 |
| **Token persistence** | Token 文件存储在 `~/.local/share/copilot-api/github_token`，权限为 `0o600`，以防止未经授权访问。 |
| **Re-auth** | 删除保存的 token 文件以强制进行新的 device flow 授权。 |
| **Non-interactive / CI** | 对于非交互环境，设置 `COPILOT_GITHUB_TOKEN`、`GH_TOKEN` 或 `GITHUB_TOKEN` 环境变量，系统将自动使用而无需提示。 |
| **Enterprise SSO** | 如果您的组织使用 SAML SSO，用户必须在 GitHub 网站上初始 device flow 登录后，还为组织授权 OAuth app。 |

---

## 关键端点总结

| Endpoint | Purpose |
|---|---|
| `POST https://github.com/login/device/code` | 获取 device code + user code |
| `POST https://github.com/login/oauth/access_token` | 轮询获取 `gho_xxx` OAuth token |
| `GET https://api.github.com/copilot_internal/v2/token` | 交换为 Copilot token |
| `POST https://api.githubcopilot.com/chat/completions` | 调用 LLM (OpenAI 兼容) |

**References:**

- [ericc-ch/copilot-api DeepWiki — Authentication Flow](https://deepwiki.com/ericc-ch/copilot-api/3.1-authentication-flow)
- [B00TK1D/copilot-api — api.py reference implementation](https://github.com/B00TK1D/copilot-api/blob/main/api.py)
- [Erick Christian's blog — Reverse engineering Copilot API](https://ericc-ch.github.io/blog/reverse-engineering-copilot-api/)
- [LiteLLM — GitHub Copilot provider docs](https://docs.litellm.ai/docs/providers/github_copilot)
- [GitHub Docs — Authenticating Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)

---

## Assistant (Build · google/gemini-3-flash-preview · 3.1s)

我将探索代码库以了解当前实现，并整合请求的 GitHub Copilot OAuth 流程。

_Thinking:_

[REDACTED]

**Tool: bash**

**Input:**

```json
{
  "description": "Lists all files in the repository to understand the project structure.",
  "command": "ls -R"
}
```

**Output:**

```
dist
eslint.config.js
index.html
node_modules
package-lock.json
package.json
public
README.md
src
tsconfig.app.json
tsconfig.json
tsconfig.node.json
vite.config.ts

./dist:
assets
favicon.svg
icons.svg
index.html

./dist/assets:
index-C0Geh5OG.css
index-pNVnKZfE.js

./node_modules:
@babel
@eslint
@eslint-community
@humanfs
@humanwhocodes
@jridgewell
@oxc-project
@rolldown
@types
@typescript-eslint
@vitejs
acorn
acorn-jsx
ajv
ansi-styles
argparse
balanced-match
baseline-browser-mapping
brace-expansion
browserslist
callsites
caniuse-lite
chalk
color-convert
color-name
concat-map
convert-source-map
cross-spawn
csstype
debug
deep-is
detect-libc
electron-to-chromium
escalade
escape-string-regexp
eslint
eslint-plugin-react-hooks
eslint-plugin-react-refresh
eslint-scope
eslint-visitor-keys
espree
esquery
esrecurse
estraverse
esutils
fast-deep-equal
fast-json-stable-stringify
fast-levenshtein
