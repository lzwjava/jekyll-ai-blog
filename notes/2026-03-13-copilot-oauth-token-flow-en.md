---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot OAuth Token Flow Guide
translated: false
type: note
---

**Question:** How do I implement GitHub Copilot's OAuth device flow to get a GitHub token, then exchange it for a Copilot API token via `copilot_internal/v2/token`, and use that token to call the Copilot LLM API — particularly in an enterprise environment where the user must authorize via GitHub?

---

**Answer:**

## Overview: The Two-Token Flow

The system uses two distinct token types: a **GitHub OAuth token** for user identity, and a short-lived **Copilot token** obtained by exchanging the GitHub token — refreshed automatically throughout the session.

Here is the full flow:

```
User runs app
  → GitHub Device Flow (user visits URL, enters code)
  → GitHub returns gho_xxx OAuth token
  → Exchange OAuth token with /copilot_internal/v2/token
  → Receive short-lived Copilot token
  → Call Copilot LLM API with Bearer <copilot_token>
```

---

## Step 1: GitHub OAuth Device Flow

The Copilot API internals are only exposed to OAuth tokens from VSCode. VSCode has its own device flow authentication with its own `client_id`. The key insight is to use VSCode's Client ID to initiate the device flow and get a `gho_xxx` OAuth app token.

VSCode's Client ID used for device flow is: **`01ab8ac9400c4e429b23`**

### Python Implementation

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

## Step 2: Exchange GitHub Token for Copilot Token

Use the GitHub OAuth token to call `https://api.github.com/copilot_internal/v2/token` with proper editor headers to receive the Copilot-specific API token.

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

> **Enterprise Note:** For enterprise accounts, additional headers like `editor-version`, `editor-plugin-version`, `Copilot-Integration-Id`, and `user-agent` must be sent correctly, otherwise the API rejects the request.

---

## Step 3: Auto-Refresh the Copilot Token

The system implements proactive token refresh with a 60-second buffer before expiration: `refreshInterval = (refresh_in - 60) * 1000`. Failed refreshes are logged and re-thrown to prevent silent failures.

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

## Step 4: Call the Copilot LLM API

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

## Step 5: Full Orchestration — Main Entry Point

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

## Enterprise Considerations

| Concern | Detail |
| --- | --- |
| **Account type** | Pass `--account-type enterprise` flag or set in your config. Enterprise uses the same `/v2/token` endpoint but may have policy restrictions. |
| **Token persistence** | Token file stored at `~/.local/share/copilot-api/github_token` with `0o600` permissions to prevent unauthorized access. |
| **Re-auth** | Delete the saved token file to force a new device flow authorization. |
| **Non-interactive / CI** | For non-interactive environments, set `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `GITHUB_TOKEN` environment variable, and the system uses it automatically without prompting. |
| **Enterprise SSO** | If your org uses SAML SSO, the user must also authorize the OAuth app for the org after initial device flow login on GitHub's website. |

---

## Summary of Key Endpoints

| Endpoint | Purpose |
| --- | --- |
| `POST https://github.com/login/device/code` | Get device code + user code |
| `POST https://github.com/login/oauth/access_token` | Poll for `gho_xxx` OAuth token |
| `GET https://api.github.com/copilot_internal/v2/token` | Exchange for Copilot token |
| `POST https://api.githubcopilot.com/chat/completions` | Call the LLM (OpenAI-compatible) |

**References:**

- [ericc-ch/copilot-api DeepWiki — Authentication Flow](https://deepwiki.com/ericc-ch/copilot-api/3.1-authentication-flow)
- [B00TK1D/copilot-api — api.py reference implementation](https://github.com/B00TK1D/copilot-api/blob/main/api.py)
- [Erick Christian's blog — Reverse engineering Copilot API](https://ericc-ch.github.io/blog/reverse-engineering-copilot-api/)
- [LiteLLM — GitHub Copilot provider docs](https://docs.litellm.ai/docs/providers/github_copilot)
- [GitHub Docs — Authenticating Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
