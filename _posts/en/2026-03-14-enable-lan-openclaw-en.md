---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enable LAN Access for OpenClaw
translated: false
type: note
---

Question: OpenClaw gateway is bound to `127.0.0.1:18789` and cannot be accessed via `http://192.168.1.36:18789`. Should I rebind it to `0.0.0.0` to allow LAN access?

Answer:

## Root Cause

The log clearly shows:

```
pid 85445 lzw: openclaw-gateway (127.0.0.1:18789)
```

OpenClaw is **only listening on localhost** (`127.0.0.1`), not on the LAN interface. That's why `192.168.1.36:18789` cannot connect — the port is not reachable from outside the machine.

**Yes, you need to bind to `0.0.0.0`** to allow LAN access. Since you are on a private home network (`192.168.1.x`) and UFW is already restricting to LAN only, this is safe.

---

## Step 1 — Stop the Gateway First

```bash
openclaw gateway stop
# or
systemctl --user stop openclaw-gateway.service
```

Verify it stopped:

```bash
ss -tlnp | grep 18789
# should return nothing
```

---

## Step 2 — Set the Bind Address to `0.0.0.0`

```bash
openclaw config set server.host 0.0.0.0
```

Or manually edit the config file:

```bash
nano ~/.openclaw/openclaw.json
```

Add or update the `server` block:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 18789
  }
}
```

---

## Step 3 — Start Gateway Again

```bash
openclaw gateway start
```

Verify it is now listening on `0.0.0.0`:

```bash
ss -tlnp | grep 18789
```

You should now see:

```
LISTEN  0.0.0.0:18789   ...   openclaw-gateway
```

instead of `127.0.0.1:18789`.

---

## Step 4 — Confirm UFW Still Protects It

Since you are binding to `0.0.0.0`, double check UFW only allows your LAN:

```bash
sudo ufw status numbered
```

Make sure you have this rule (from previous step):

```
ALLOW IN    192.168.1.0/24    18789
```

If not, add it:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 18789
sudo ufw reload
```

---

## Step 5 — Test from Your Main PC

Open browser on your main computer and go to:

```
http://192.168.1.36:18789
```

Or test with curl from your main PC:

```bash
curl http://192.168.1.36:18789
```

---

## Security Summary

| Binding | Accessible From | Safe? |
|---|---|---|
| `127.0.0.1` | Localhost only | ✅ Most secure, but you can't access from LAN |
| `0.0.0.0` + UFW LAN rule | Your home LAN only | ✅ Safe for home use |
| `0.0.0.0` + no UFW | Anyone including internet | ❌ Dangerous |

Your setup with `0.0.0.0` + UFW rule `192.168.1.0/24` is **perfectly safe** for a home network.