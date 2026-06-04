---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing VSCode Proxy Authentication Prompts
translated: false
type: note
---

**Question:** Why does VSCode keep showing proxy dialogs even after configuring proxy settings in an enterprise environment?

**Answer:**

VSCode's proxy handling is fragmented across multiple layers, and misconfiguring any one causes the repeated prompts. Here's what's actually happening and how to fix it properly.

## The Root Problem

VSCode doesn't just have one proxy setting — different components handle proxies independently:
1. **VSCode itself** (Electron)
2. **Node.js processes** (extensions, language servers)
3. **Git** (for source control)
4. **Extensions** (may have their own proxy logic)

If you only configure one layer, the others fail and prompt for credentials.

## The Right Way to Configure Proxy

### 1. **VSCode Settings** (`settings.json`)

```json
{
  "http.proxy": "http://<PROXY_HOST>:<PORT>",
  "https.proxy": "http://<PROXY_HOST>:<PORT>",
  "http.proxyStrictSSL": false,
  "http.proxyAuthorization": true,
  "http.proxySupport": "override"
}
```

Key detail: if your proxy requires authentication, **don't embed credentials in settings.json**. VSCode will prompt once and cache them in its credential store.

### 2. **Environment Variables** (critical for Node/Git)

Set these before launching VSCode:

```bash
export HTTP_PROXY="http://<PROXY_HOST>:<PORT>"
export HTTPS_PROXY="http://<PROXY_HOST>:<PORT>"
export NO_PROXY="localhost,127.0.0.1"
export NODE_TLS_REJECT_UNAUTHORIZED=0  # Only if self-signed certs
```

If using proxy with auth:

```bash
export HTTP_PROXY="http://<USER>:<PASSWORD>@<PROXY_HOST>:<PORT>"
export HTTPS_PROXY="http://<USER>:<PASSWORD>@<PROXY_HOST>:<PORT>"
```

**Better approach** — use a proxy that doesn't require embedding credentials (NTLM/domain auth handled by OS), or store credentials in `~/.netrc`:

```
machine <PROXY_HOST>
login <USER>
password <PASSWORD>
```

Then launch VSCode:

```bash
code  # Picks up env vars and .netrc
```

### 3. **Git Configuration**

Enterprise environments often have Git proxying issues separately:

```bash
git config --global http.proxy "http://<PROXY_HOST>:<PORT>"
git config --global https.proxy "http://<PROXY_HOST>:<PORT>"
git config --global http.sslVerify false
```

Or if your enterprise uses NTLM/domain auth:

```bash
git config --global http.proxy "http://<DOMAIN>\\<USER>:<PASSWORD>@<PROXY_HOST>:<PORT>"
```

### 4. **For Corporate HTTPS Inspection (MITM Proxies)**

If your enterprise inspects HTTPS traffic (man-in-the-middle), import the corporate CA certificate:

```bash
# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/corporate-ca.crt

# Linux
sudo cp /path/to/corporate-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Windows (PowerShell)
Import-Certificate -FilePath "C:\path\to\corporate-ca.crt" -CertStoreLocation "Cert:\CurrentUser\Root"
```

Then VSCode can safely verify SSL with `"http.proxyStrictSSL": true`.

### 5. **Disable Proxy for Specific Hosts** (if needed)

```json
{
  "http.proxyAuthorization": true,
  "http.noProxy": "*.internal.company.com,localhost,127.0.0.1,192.168.x.x"
}
```

## Debugging Checklist

If popups persist:

1. **Check what VSCode actually sees:**
   ```bash
   code --verbose 2>&1 | grep -i proxy
   ```

2. **Verify environment variables are loaded:**
   ```bash
   env | grep -i proxy
   ```

3. **Test the proxy directly:**
   ```bash
   curl -x http://<PROXY_HOST>:<PORT> https://api.github.com
   ```

4. **Disable extensions** (some override proxy logic) — reload VSCode in Safe Mode via Command Palette.

5. **Clear cached credentials:**
   - macOS: Keychain → remove VSCode entries
   - Linux: `~/.config/Code/User/globalStorage` → delete credential cache
   - Windows: Credential Manager → remove VSCode entries

## The Nuclear Option

If the above fails and you're on a workstation you control, use a local proxy tunnel (easier to debug):

```bash
# Use a local SOCKS proxy or tinyproxy
# Forward all traffic through your corporate proxy
tinyproxy -r <PROXY_HOST> -p 8888

# Then in VSCode:
# "http.proxy": "http://127.0.0.1:8888"
```

This isolates VSCode from enterprise proxy complexity and gives you a single control point.

---

**References:**

- [VSCode HTTP Proxy Settings](https://code.visualstudio.com/docs/setup/network)
- [Node.js Proxy Configuration](https://nodejs.org/en/docs/guides/nodejs-behind-a-corporate-proxy/)
