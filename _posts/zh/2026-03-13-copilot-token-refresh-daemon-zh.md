---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot 令牌自动刷新守护进程
translated: true
type: note
---

**会话 ID:** ses_31a4979a7ffe9rU42KDzISEti3
**创建时间:** 3/13/2026, 1:41:10 PM
**更新时间:** 3/13/2026, 1:41:26 PM

---

## 用户

like this , import threading

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
    thread.start()  , import os

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
    main()  , also add refresh token logic 

---

## 助手 (Build · google/gemini-3-flash-preview · 16.3s)

_思考：_

**分析认证策略**

我目前专注于剖析提供的代码片段，以理解提议的认证流程，特别是“refresh token logic”。我的即时任务是找出如何最好地将这些部分整合成一个连贯的 Python 脚本，该脚本可靠地管理 GitHub Copilot 认证，重点关注 token 刷新机制的稳健性。


**优化 Copilot Token 管理**

我现在专注于将提供的 refresh token logic 整合到一个全面的 Copilot 认证结构中。我的重点是合成一个完整的 Python 实现，该实现应包含所有必要部分，如 GitHub token 处理和 Copilot token 交换。我还在添加特别请求的功能，并处理返回 access token 的逻辑。

我将实现一个 Python 脚本，整合 GitHub Device Flow 进行认证，处理 Copilot token 交换，并维护后台刷新循环，如请求所述。

### 实现计划

1.  **认证流程**：使用 GitHub 的 OAuth API 实现 `get_device_code` 和 `poll_for_access_token`。
2.  **Token 交换**：实现 `get_copilot_token` 以将 GitHub OAuth token 交换为临时的 Copilot 会话 token。
3.  **LLM 交互**：实现 `call_copilot_llm` 以演示使用缓存 token 与 Copilot API 的交互。
4.  **后台刷新**：整合您提供的 `threading` 逻辑，以无限期保持 Copilot token 有效。

我将从创建 `copilot_proxy.py` 脚本开始。

#### `copilot_proxy.py`

```python
import os
import time
import json
import threading
import requests

# Constants
GITHUB_TOKEN_FILE = os.path.expanduser("~/.copilot_github_token")
DEVICE_CODE_URL = "https://github.com/login/device/code"
ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
COPILOT_TOKEN_URL = "https://api.github.com/copilot_internal/v2/token"
COPILOT_CHAT_URL = "https://api.githubcopilot.com/chat/completions"
CLIENT_ID = "Iv1.b507a3d205f504c4"  # GitHub CLI Client ID

# Global Cache
copilot_token_cache = {"token": None, "expires_at": 0}

def get_device_code():
    """Request a device code from GitHub"""
    response = requests.post(
        DEVICE_CODE_URL,
        headers={"Accept": "application/json"},
        data={"client_id": CLIENT_ID, "scope": "read:user"}
    )
    response.raise_for_status()
    data = response.json()
    print(f"🔗 Please visit: {data['verification_uri']}")
    print(f"🔢 Enter code: {data['user_code']}")
    return data

def poll_for_access_token(device_code, interval):
    """Poll GitHub for the access token after user authorization"""
    print("⏳ Waiting for authorization...")
    while True:
        response = requests.post(
            ACCESS_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": CLIENT_ID,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
            }
        )
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        
        error = data.get("error")
        if error == "authorization_pending":
            time.sleep(interval)
        elif error == "slow_down":
            time.sleep(interval + 5)
        else:
            raise Exception(f"Failed to get token: {data.get('error_description')}")

def get_copilot_token(github_token):
    """Exchange GitHub token for a Copilot session token"""
    response = requests.get(
        COPILOT_TOKEN_URL,
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/json",
        }
    )
    response.raise_for_status()
    return response.json()

def refresh_copilot_token_loop(github_token: str):
    """Background thread: auto-refresh Copilot token before expiry"""
    while True:
        try:
            token_data = get_copilot_token(github_token)
            copilot_token_cache["token"] = token_data["token"]
            copilot_token_cache["expires_at"] = token_data["expires_at"]

            refresh_in = token_data.get("refresh_in", 1500)
            # Refresh 60s before expiry, but at least every 30s
            sleep_seconds = max(refresh_in - 60, 30)
            print(f"🔄 Next Copilot token refresh in {sleep_seconds}s")
            time.sleep(sleep_seconds)
        except Exception as e:
            print(f"❌ Token refresh failed: {e}")
            time.sleep(10)  # Retry soon on failure

def start_token_refresh_daemon(github_token: str):
    thread = threading.Thread(
        target=refresh_copilot_token_loop,
        args=(github_token,),
        daemon=True
    )
    thread.start()

def load_or_auth_github_token() -> str:
    """Load saved token or run device flow"""
    if os.path.exists(GITHUB_TOKEN_FILE):
        with open(GITHUB_TOKEN_FILE) as f:
            token = f.read().strip()
            if token:
                # Basic validation: check if token still works
                try:
                    get_copilot_token(token)
                    print("✅ Loaded saved GitHub token.")
                    return token
                except:
                    print("⚠️ Saved token invalid. Re-authenticating...")

    device_data = get_device_code()
    github_token = poll_for_access_token(
        device_data["device_code"],
        interval=device_data.get("interval", 5)
    )

    with open(GITHUB_TOKEN_FILE, "w") as f:
        f.write(github_token)
    os.chmod(GITHUB_TOKEN_FILE, 0o600)
    return github_token

def call_copilot_llm(prompt: str):
    """Make a request to the Copilot Chat API using the cached token"""
    if not copilot_token_cache["token"]:
        raise Exception("Copilot token not available")

    response = requests.post(
        COPILOT_CHAT_URL,
        headers={
            "Authorization": f"Bearer {copilot_token_cache['token']}",
            "Content-Type": "application/json",
            "Editor-Version": "vscode/1.80.0",
        },
        json={
            "messages": [{"role": "user", "content": prompt}],
            "model": "gpt-4"
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    try:
        github_token = load_or_auth_github_token()

        # Get initial Copilot token
        token_data = get_copilot_token(github_token)
        copilot_token_cache["token"] = token_data["token"]
        copilot_token_cache["expires_at"] = token_data["expires_at"]

        # Start background refresh
        start_token_refresh_daemon(github_token)

        # Demonstration
        print("🤖 Calling Copilot LLM...")
        answer = call_copilot_llm("What is GitHub Copilot?")
        print(f"\n🤖 Copilot says:\n{answer}")
        
        # Keep main thread alive to see refreshes if needed
        print("\n(Script will stay active for 2 minutes to show refresh logic...)")
        time.sleep(120)

    except KeyboardInterrupt:
        print("\n👋 Exiting...")

if __name__ == "__main__":
    main()
```

此实现包括：
- **Device Flow 认证**：使用 GitHub CLI Client ID 获取 OAuth token。
- **持久化**：将 GitHub token 保存到 `~/.copilot_github_token`，并设置受限权限。
- **线程刷新**：定期更新短暂的 Copilot 会话 token（通常在 25-30 分钟后过期）。
- **LLM 集成**：一个可工作的 `call_copilot_llm` 函数，使用 Copilot API 所需的 VS Code editor headers。

您可以运行此脚本进行认证，并在 CLI 应用程序中使用 Copilot。

_思考：_

[REDACTED]

---