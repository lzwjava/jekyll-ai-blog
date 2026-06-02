---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: GitHub Copilot Authentication Flow
translated: false
type: note
---

Good question — GitHub Copilot’s authentication flow is basically a standard **OAuth2 device code grant**, but with some GitHub-specific tokens layered on top for the Copilot service itself. Let me break it down step by step:

---

### 1. **Device Flow (`/login/device/code`)**

* When you first log in, the Copilot client (e.g., VS Code extension, JetBrains plugin, or CLI) calls GitHub’s OAuth endpoint:

  ```
  POST https://github.com/login/device/code
  ```

* It sends along the **client\_id** (specific to GitHub Copilot).
* GitHub responds with:

  * `device_code` (internal code used for polling),
  * `user_code` (the one you see and enter in your browser),
  * `verification_uri` (the URL you visit to enter the code),
  * `interval` (how often the client should poll).

---

### 2. **Polling for Access Token**

* The Copilot client then polls:

  ```
  POST https://github.com/login/oauth/access_token
  ```

* It includes the `device_code` and `client_id`.
* Once you’ve approved in your browser, GitHub returns:

  * `access_token` (a **GitHub OAuth token** scoped for Copilot usage),
  * `token_type=bearer`,
  * `expires_in` (lifetime).

This `access_token` is a **normal GitHub OAuth2 token**.

---

### 3. **Exchanging for `copilot_internal` Token**

* The Copilot client cannot call Copilot APIs directly with the GitHub OAuth token.
* Instead, it exchanges it with the Copilot service:

  ```
  POST https://api.github.com/copilot_internal/v2/token
  Authorization: Bearer <GitHub OAuth access_token>
  ```

* The response is:

  ```json
  {
    "token": "<copilot_internal token>",
    "expires_at": "...",
    "user": { ... }
  }
  ```

* This **`copilot_internal` v2 token** is what the Copilot client uses to talk to the **Copilot inference service** (e.g., `https://copilot-proxy.githubusercontent.com`).

---

### 4. **Using the `copilot_internal` Token**

* All subsequent completions or chat requests are authenticated with:

  ```
  Authorization: Bearer <copilot_internal token>
  ```

* This token has a short lifetime (usually \~1 hour) and is tied to your GitHub account + Copilot subscription status.
* The client refreshes it periodically by re-exchanging the GitHub OAuth access token.

---

✅ **In summary:**

* `/login/device/code` → gives you a code to authenticate in browser.
* `/login/oauth/access_token` → gives you a GitHub OAuth token.
* `/copilot_internal/v2/token` → exchanges that for a short-lived Copilot token, which is the *real* credential used for completions.

---

Would you like me to also draw the **exact request/response examples** (with headers and sample JSON) so you can see what the payloads look like in practice?
