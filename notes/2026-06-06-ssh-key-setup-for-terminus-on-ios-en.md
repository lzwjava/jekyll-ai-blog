---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Key Setup for Terminus on iOS
translated: false
type: note
---

Question: How do I set up Terminus on iOS with Tailscale to avoid password prompts every time?

Answer:

The password prompt happens because **Terminus is using password authentication instead of SSH key authentication**. Each session requires manual auth. Fix this by setting up key-based auth.

## Setup: Key-Based Auth in Terminus + Tailscale

### Step 1: Generate SSH key (on your workstation, not iOS)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/terminus_ios -C "terminus@ios"
# Don't set passphrase (or Terminus will prompt for it)
```

### Step 2: Add public key to server

```bash
cat ~/.ssh/terminus_ios.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Verify on your workstation first:
```bash
ssh -i ~/.ssh/terminus_ios user@192.168.1.36  # Should NOT ask password
```

### Step 3: Import key into Terminus (iOS)

1. **Copy private key to iOS** (easiest: AirDrop or email to yourself)
   ```bash
   cat ~/.ssh/terminus_ios | pbcopy  # macOS: copy to clipboard
   ```

2. **In Terminus app:**
   - Settings → SSH Keys → Add Key
   - Paste the **private key** content
   - Name it: `terminus_ios`
   - Save

3. **Create host config:**
   - Hosts → Add
   - Host: `workstation` (or Tailscale IP like `100.x.x.x`)
   - User: `your_username`
   - Port: `22`
   - Auth: Select `terminus_ios` key
   - Save

### Step 4: Connect via Tailscale

In Terminus, use your **Tailscale IP** (e.g., `100.97.x.x`) instead of LAN IP:

```
ssh user@100.97.x.x
```

Or if Tailscale DNS works, use the machine name:
```
ssh user@lzw.tail123456.ts.net
```

---

## Why It's Still Asking for Password

**Common reasons:**

1. **Key not selected in Terminus host config** — verify "Auth" is set to your key, not "Password"
2. **Private key format mismatch** — Terminus prefers OpenSSH format (check key header: `-----BEGIN OPENSSH PRIVATE KEY-----`)
3. **Server not reloaded `authorized_keys`** — SSH daemon caches; restart if needed:
   ```bash
   sudo systemctl restart sshd  # Linux
   ```
4. **Permissions wrong on server** — must be:
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

---

## Terminus + Tailscale Workflow (Practical)

Once configured:

```bash
# From iOS Terminus, just tap the host
# Or if using command mode:
ssh workstation
# Connects instantly, no password

# Ctrl+C works for interrupt
# Long-press menu for more options (copy, paste, etc.)
```

**Pro tip:** Set `StrictHostKeyChecking=no` in Terminus if Tailscale IPs rotate (though they shouldn't):
```bash
# In Terminus advanced settings, add to SSH config:
Host *.tail123456.ts.net
    StrictHostKeyChecking=accept-new
```

---

## Why No Password Every Time?

Once the key is in `authorized_keys`, SSH performs **public-key authentication** — the iOS client proves it has the private key without transmitting it. Server verifies using the public key. Handshake completes, session opens. No password needed.

**Performance note:** Tailscale routes through your network efficiently; iOS↔workstation via Tailscale is nearly as fast as direct SSH.
