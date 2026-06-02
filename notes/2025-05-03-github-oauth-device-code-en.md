---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: GitHub OAuth Device Code Flow
translated: false
type: note
---

### Overview

This JavaScript code implements the OAuth 2.0 Device Authorization Grant flow (also known as the Device Code grant) to authenticate with GitHub and obtain an access token. The flow is typically used for headless applications (e.g., CLI tools or embedded systems) where the user can't interact directly with a web browser to approve the authentication.

In this specific case, it appears to be mimicking requests from the GitHub Copilot plugin (e.g., for Neovim or Vim), using headers that spoof a Copilot client to potentially integrate with or access GitHub's authentication system. The goal is to generate an access token that could be used for GitHub API calls requiring user authentication, such as reading user info (per the `scope: "read:user"`).

The code runs as a Node.js script, using `fetch` for HTTP requests and `process` for environment variables. It assumes Node.js has `fetch` available (as in newer versions or via a polyfill). If successful, it polls GitHub's servers until the user authorizes the request or it times out.

**Important Notes:**

- This code requires setting an environment variable `MY_COPILOT_CLIENT_ID`, likely a GitHub OAuth App client ID registered for GitHub Copilot.
- It handles errors minimally—e.g., if fetching fails, it logs and continues or exits.
- Security-wise, storing or logging access tokens is risky (they grant API access). This code prints the full token object directly to the console, which could be a privacy/security issue in real usage. Access tokens should be handled securely (e.g., stored encrypted and rotated).
- The flow involves user interaction: The user must visit a URL and enter a code on GitHub's site to authorize.
- This isn't "official" GitHub documentation code; it seems reverse-engineered from GitHub Copilot's behavior. Use APIs responsibly and per GitHub's terms of service.

### Step-by-Step Breakdown

#### 1. Environment Check

```javascript
const clientId = process.env.MY_COPILOT_CLIENT_ID;

if (!clientId) {
  console.error("MY_COPILOT_CLIENT_ID is not set");
  process.exit(1);
}
```

- Retrieves the `MY_COPILOT_CLIENT_ID` from environment variables (e.g., set via `export MY_COPILOT_CLIENT_ID=your_client_id` in your shell).
- If not set, it logs an error and exits the script (process code 1 indicates failure).
- This client ID is from a registered GitHub OAuth App (needed for OAuth flows).

#### 2. Common Headers Setup

```javascript
const commonHeaders = new Headers();
commonHeaders.append("accept", "application/json");
commonHeaders.append("editor-version", "Neovim/0.6.1");
commonHeaders.append("editor-plugin-version", "copilot.vim/1.16.0");
commonHeaders.append("content-type", "application/json");
commonHeaders.append("user-agent", "GithubCopilot/1.155.0");
commonHeaders.append("accept-encoding", "gzip,deflate,b");
```

- Creates a `Headers` object with key-value pairs for HTTP requests.
- These headers make the requests look like they're from the GitHub Copilot Vim plugin (version 1.16.0 for Neovim 0.6.1). This is likely to spoof the user-agent and mimic Copilot's API calls, which might be required or helpful for GitHub to accept the requests.
- `"accept": "application/json"`: Expects JSON responses.
- `"content-type": "application/json"`: Sends JSON in request bodies.
- `"accept-encoding"`: Allows gzip/deflate compression to save bandwidth.

#### 3. `getDeviceCode()` Function

```javascript
async function getDeviceCode() {
  const raw = JSON.stringify({
    "client_id": clientId,
    "scope": "read:user",
  });

  const requestOptions = {
    method: "POST",
    headers: commonHeaders,
    body: raw,
  };

  const data = await fetch(
    "https://github.com/login/device/code",
    requestOptions,
  )
    .then((response) => response.json())
    .catch((error) => console.error(error));
  return data;
}
```

- **Purpose**: Initiates the Device Code flow by requesting a device code from GitHub.
- Constructs a JSON payload with:
  - `client_id`: The OAuth client ID (for authentication of your app).
  - `scope`: `"read:user"`—limits the token to read basic user profile info (e.g., username, email via GitHub API). This is a minimal scope.
- Makes a POST request to `https://github.com/login/device/code` (GitHub's OAuth device code endpoint).
- Parses the JSON response (expected fields: `device_code`, `user_code`, `verification_uri`, `expires_in`—not shown in code, but standard for this flow).
- On error (e.g., network issues), logs it but continues (could return `undefined`).
- Returns the parsed JSON data object from GitHub.

#### 4. `getAccessToken(deviceCode: string)` Function

```javascript
async function getAccessToken(deviceCode: string) {
  const raw = JSON.stringify({
    "client_id": clientId,
    "device_code": deviceCode,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
  });

  const requestOptions = {
    method: "POST",
    headers: commonHeaders,
    body: raw,
  };

  return await fetch(
    "https://github.com/login/oauth/access_token",
    requestOptions,
  )
    .then((response) => response.json())
    .catch((error) => console.error(error));
}
```

- **Purpose**: Polls GitHub to exchange the device code for an access token once the user authorizes it.
- Takes the `device_code` from the previous step.
- Constructs JSON with:
  - `client_id`: Same as before.
  - `device_code`: The unique code identifying this device/auth attempt.
  - `grant_type`: Specifies this is a Device Code grant (standard OAuth2 URN).
- Makes a POST request to `https://github.com/login/oauth/access_token`.
- Returns the parsed JSON response, which could be:
  - On success: `{ access_token: "...", token_type: "bearer", scope: "read:user" }`.
  - On pending/error: `{ error: "...", error_description: "..." }` (e.g., "authorization_pending" or "slow_down").
- Errors (e.g., fetch failures) are logged but not explicitly handled, so the caller must check the return value.

#### 5. Main Execution (Immediately Invoked Async Function)

```javascript
(async function () {
  const { device_code, user_code, verification_uri, expires_in } =
    await getDeviceCode();
  console.info(`enter user code:\n${user_code}\n${verification_uri}`);
  console.info(`Expires in ${expires_in} seconds`);
  while (true) {
    await new Promise((resolve) => setTimeout(resolve, 5000));
    const accessToken = await getAccessToken(device_code);
    if (accessToken.error) {
      console.info(`${accessToken.error}: ${accessToken.error_description}`);
    }
    if (accessToken.access_token) {
      console.info(`access token:\n${JSON.stringify(accessToken, null, 1)}`);
      break;
    }
  }
})();
```

- **Overall Flow**: Orchestrates the full OAuth 2.0 Device Code grant.
- Calls `getDeviceCode()` and destructures the response into variables (assumes it succeeds and has these properties).
- Logs instructions for the user:
  - `user_code`: A short alphanumeric code (e.g., "ABCD-EFGH").
  - `verification_uri`: Usually `https://github.com/login/device`, where the user authenticates.
  - `expires_in`: Time in seconds until the code expires (e.g., 900 for 15 minutes).
- The user must visit the URL, sign in to GitHub, and enter the user code to authorize the app.
- Enters an infinite loop to poll for the token:
  - Waits 5 seconds between attempts (polling interval; GitHub recommends slow_down for too-frequent requests).
  - Calls `getAccessToken(device_code)`.
  - If the response has an `error`: Logs it (e.g., keep waiting if "authorization_pending").
  - If it has `access_token`: Logs the full token object (formatted with indentation) and exits the loop.
- **Edge Cases/Issues**:
  - If `getDeviceCode()` fails, destructuring might error (code doesn't check for this).
  - No loop timeout—keeps polling indefinitely unless the access token is received or the script crashes.
  - Logging the access token to console exposes it; in production, you'd save it securely (e.g., to a file or database).

### How It Works End-to-End

1. **Step 1: Request Device Code** → Script gets a temporary code from GitHub.
2. **Step 2: User Authorization** → User visits GitHub and enters the code to grant permission.
3. **Step 3: Poll for Token** → Script keeps asking GitHub until the token is issued.
4. **Result**: An access token for the specified scope (e.g., read user data via GitHub API).

This is a simulation of how tools like GitHub CLI might work, adapted for Copilot. For official GitHub OAuth docs, refer to <https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#device-flow>. If you're building something similar, ensure compliance with OAuth standards and GitHub's policies. If you have questions about modifying or running this, let me know!
