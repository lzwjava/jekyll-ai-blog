---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Fix for isomp:// Protocol Links"
translated: false
type: note
---

Here is the summary again:

---

## 🔍 Decoded `isomp://` URI

The base64 payload decoded to:

```
[GATEWAY_IP] 12025 mstsc [UUID] rdp [TARGET_IP]
```

| Field | Value |
| ------- | ------- |
| SSO Gateway | `xxx.xxx.x.xx` |
| Gateway Port | `12025` |
| Protocol | **RDP** (Remote Desktop / mstsc) |
| Session UUID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| Target Server | `xxx.xxx.x.xxx` |

---

## ❌ Problem

The `isomp://` protocol handler was **missing from Windows Registry**, so clicking any `isomp://` link did nothing. The IsompSSO client (`sso.exe`) could not launch automatically.

---

## ✅ Fix Applied

Registered the `isomp://` protocol in Windows Registry:

**`.reg` file created at:** `C:\Program Files\IsompSSO\register_isomp.reg`

**Registry keys added:**

- `HKCR\isomp` → `URL:IsompSSO Protocol`
- `HKCR\isomp\shell\open\command` → `"C:\Program Files\IsompSSO\sso.exe" "%1"`

This tells Windows to pass any `isomp://` URL to `sso.exe`.

---

## 🔧 RDP File Adjustment

In your saved `Default.rdp` file, changed:

| Before | After |
|--------|-------|
| `prompt for credentials:i:0` | `prompt for credentials:i:1` |

This allows the credentials dialog to appear if automatic authentication fails.

---

## ✅ Result

After registering the protocol, `sso.exe` successfully:

1. Received the `isomp://` URL
2. Decoded the base64 payload
3. Authenticated through the SSO gateway using the session UUID
4. Launched **mstsc.exe** (Remote Desktop) to connect to the target server

All `isomp://` links will now work automatically going forward.
