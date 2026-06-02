---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using Proxy with Camoufox Fetch
translated: false
type: note
---

Question: How to use a proxy with npx camoufox-js fetch to speed up the slow download in China?

Answer:

Here is how to make the Camoufox download go through your proxy (this is the most reliable way when you are in China and the direct download is extremely slow).

### 1. Best and Simplest Method: Set Environment Variables (Recommended)

Before running the fetch command, set the proxy environment variables in your terminal:

**For most proxies (HTTP/HTTPS proxy):**

```bash
export HTTP_PROXY=http://your-proxy-ip:port
export HTTPS_PROXY=http://your-proxy-ip:port
```

**If your proxy requires username and password:**

```bash
export HTTP_PROXY=http://username:password@your-proxy-ip:port
export HTTPS_PROXY=http://username:password@your-proxy-ip:port
```

**Example with a common local proxy like Clash/V2Ray (port 7890):**

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
```

Then run the fetch command:

```bash
npx camoufox-js fetch
```

You can combine them in one line:

```bash
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch
```

### 2. If You Want to Force Re-download

```bash
HTTP_PROXY=http://127.0.0.1:7890 HTTPS_PROXY=http://127.0.0.1:7890 npx camoufox-js fetch --force
```

### 3. Make It Permanent (Optional)

Add the export lines to your shell profile so they apply every time:

- For zsh (most Mac users): `echo 'export HTTP_PROXY=http://127.0.0.1:7890' >> ~/.zshrc`
- Then run `source ~/.zshrc`

### 4. Alternative: Use npm config (sometimes helps with npx)

```bash
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890
npx camoufox-js fetch
```

**Important Tips:**

- Make sure your proxy/VPN is **running and connected** before setting these variables.
- Many China users use Clash, V2Ray, or Shadowsocks on port 7890 or 1080.
- Use `http://` even for SOCKS5 proxies in most cases (some tools convert it automatically).
- After the download finishes successfully, you can unset the variables if you want:

  ```bash
  unset HTTP_PROXY HTTPS_PROXY
  ```

### 5. Check If Proxy Is Working

Before running the big download, test with a small command:

```bash
HTTP_PROXY=http://127.0.0.1:7890 curl -I https://www.google.com
```

If it returns headers quickly, the proxy is working for downloads.

Try the environment variable method first — it works for most users facing the same slow download issue with Camoufox in China. Let me know the exact proxy you are using (e.g., port and type) if it still doesn't work, and I can give more specific commands.

References:

- <https://www.mintlify.com/jo-inc/camofox-browser/installation> (mentions setting HTTP_PROXY for camoufox-js fetch)
- <https://github.com/daijro/camoufox/issues/342> (users discuss using ENV HTTP_PROXY / HTTPS_PROXY for fetch)
- General Node.js proxy behavior with environment variables
